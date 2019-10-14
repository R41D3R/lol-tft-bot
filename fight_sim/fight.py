import random
import math

import pygame

from fight_sim.board.map import Map
from fight_sim.effects.status_effect import StatusEffect
from fight_sim.effects.shield import Shield
from fight_sim.config import logger
from fight_sim.champ.champs import Golem


class Fight:
    def __init__(self, champ_fabric):
        self.champ_fabric = champ_fabric

        # init
        self.team_bot = None
        self.team_top = None
        self.map = self.board
        self.events = []
        self.aoe = []
        self.now = None
        self.start_of_combat = True
        self.bot_synergy = {}
        self.top_synergy = {}
        self.hextech_tick = None
        self.ranger_tick = None
        self.hextech_disabled_champs = []
        self.selected_champs = []

    @property
    def board(self):
        return Map(cell_radius=50, n_rows=6, n_cols=7, color=(0, 150, 0), space=0)

    @property
    def game_over(self):
        return all(not champ.alive for champ in self.team_top) \
               or all(not champ.alive for champ in self.team_bot)

    @property
    def result(self):
        return [champ for champ in self.team_top if champ.alive is True], \
               [champ for champ in self.team_bot if champ.alive is True]

    @property
    def champions_alive(self):
        return [champ for champ in self.team_top + self.team_bot if champ.alive]

    def new_fight(self, reset=False):
        self.team_top, self.team_bot = self.champ_fabric.get_teams(reset=reset)
        self._check_valid_pos(self.map.n_cols, self.map.n_rows, self.team_bot)
        self._check_valid_pos(self.map.n_cols, self.map.n_rows, self.team_top)

        self.map = self.board
        self.events = []
        self.aoe = []
        self.now = None
        self.start_of_combat = True
        self.bot_synergy = {}
        self.top_synergy = {}
        self.hextech_tick = None
        self.ranger_tick = None
        self.hextech_disabled_champs = []
        self.selected_champs = []

        self._place_champs()

    def make_fight_step(self):
        now = pygame.time.get_ticks()
        self.now = now
        self.map.time = now
        if self.start_of_combat:
            self.start_of_combat = False
            self._set_team_synergies()

            self._trigger_fight_start()
            self.ranger_tick = self.now
        champs = [champ for champ in self.team_bot + self.team_top if champ.alive]
        random.shuffle(champs)

        # @synergy: Hextech
        # enable items after 7 seconds
        if self.hextech_tick:
            if self.now - self.hextech_tick >= 7000:
                self.hextech_tick = None
                for champ in self.hextech_disabled_champs:
                    champ.items += champ.disabled_items

        # @synergy: Ranger
        synergy_name = "Ranger"
        if self.now - self.ranger_tick >= 3000:
            self.ranger_tick = self.now
            rnd_n = random.random()
            if synergy_name in self.bot_synergy:
                n_syn = self.bot_synergy[synergy_name]
                if (n_syn >= 4 and rnd_n <= 0.7) or (n_syn >= 2 and rnd_n <= 0.25):
                    for champ in self.team_bot:
                        if synergy_name in champ.class_:
                            champ.status_effects.append(StatusEffect(self.map, 3, "Ranger", effects=["double_attack_speed"]))
            elif synergy_name in self.top_synergy:
                n_syn = self.top_synergy[synergy_name]
                if (n_syn >= 4 and rnd_n <= 0.7) or (n_syn >= 2 and rnd_n <= 0.25):
                    for champ in self.team_top:
                        if synergy_name in champ.class_:
                            champ.status_effects.append(StatusEffect(self.map, 3, "Ranger", effects=["double_attack_speed"]))

        # AOE
        for aoe in self.aoe:
            aoe.proc()
            if not aoe.active:
                self.aoe.remove(aoe)

        for champ in champs:
            if champ.can_make_turn:
                logger.debug(f"{champ.name} turn")

                if champ.name == "Gangplank":
                    champ.create_new_barrel()

                enemies_alive = self.enemy_champs_alive(champ)
                if len(enemies_alive) == 0:
                    return

                enemy_team = self.enemy_team_visible(champ)  # rework visible
                enemies_in_range = champ.get_enemies_in_range(self)

                # @todo: rework channeling abilites
                # @body: make them interuptable if needed and add can_cast
                if champ.enough_mana_for_sa and champ.can_use_sa:
                    champ.stop_moving(self)

                    # @item: Ionic Spark
                    item_name = "Ionic Spark"
                    n_items_enemy_team = self._enemy_team_item_count(champ, item_name)
                    if n_items_enemy_team > 0:
                        champ.get_damage("true", 125 * n_items_enemy_team, self, origin="item", originator=champ, source="Ionic Spark")

                    champ.special_ability(self, enemies_in_range, enemy_team, enemies_alive, now)
                    champ.sa_counter += 1
                    champ.mana = 0

                    # @synergy: Shapeshifter
                    synergy_name = "Shapeshifter"
                    if champ.sa_counter == 1:
                        if synergy_name in self.top_synergy and synergy_name in champ.class_:
                            n_syn = self.top_synergy[synergy_name]
                            health_bonus = 0
                            if n_syn >= 6:
                                health_bonus = 1
                            elif n_syn >= 3:
                                health_bonus = 0.6
                            if health_bonus > 0:
                                bonus = health_bonus * champ.max_health
                                champ.base_health += bonus
                                champ.heal(bonus, self.map)
                        elif synergy_name in self.bot_synergy and synergy_name in champ.class_:
                            n_syn = self.bot_synergy[synergy_name]
                            health_bonus = 0
                            if n_syn >= 6:
                                health_bonus = 1
                            elif n_syn >= 3:
                                health_bonus = 0.6
                            if health_bonus > 0:
                                bonus = health_bonus * champ.max_health
                                champ.base_health += bonus
                                champ.heal(bonus, self.map)

                    # @item: Seraph's Embrace
                    item_name = "Seraph's Embrace"
                    if champ.item_count(item_name) > 0:
                        n_items = champ.item_count(item_name)
                        champ.get_mana(item_name, 20 * n_items)

                elif champ.are_enemies_in_range:
                    champ.stop_moving(self)
                    if champ.can_use_aa:
                        logger.debug(f"{champ.name} attacks")
                        champ.autoattack(now, self, enemies_in_range)
                    else:
                        logger.debug(f"{champ.name} aa is on cooldown")
                elif champ.can_move:
                    champ.move()

        for champ in self.champions_alive:
            self._activate_aura(champ)
            champ.check_shields(self.now)
            champ.check_status_effects(self.now)
            self._dot_damage(champ)

    def get_champ_from_cell(self, cell):
        for champ in self.team_top + self.team_bot:
            if champ.pos == cell.id:
                return champ
        else:
            return None

    @staticmethod
    def champs_in_area(area, champs):
        champs_in_area = []
        area_ids = [cell.id for cell in area]
        for champ in champs:
            if champ.pos in area_ids:
                champs_in_area.append(champ)
        return champs_in_area

    def enemy_champs_alive(self, champ):
        enemy_team = self.champs_enemy_team(champ)
        return [enemy for enemy in enemy_team if enemy.alive]

    def allie_champs_alive(self, champ):
        allie_team = self.champs_allie_team(champ)
        return [allie for allie in allie_team if allie.alive]

    def enemy_team_visible(self, champ):
        return [enemy for enemy in self.enemy_champs_alive(champ) if enemy.visible]

    def champs_enemy_team(self, champ):
        if champ in self.team_bot:
            return self.team_top
        else:
            return self.team_bot

    def champs_allie_team(self, champ):
        if champ not in self.team_bot:
            return self.team_top
        else:
            return self.team_bot

    def adjacent_enemies(self, champ):
        adjacent_enemies = []
        adjacent_ids = [cell.id for cell in self.map.get_cell_from_id(champ.pos).neighbors]
        for enemy in self.enemy_champs_alive(champ):
            if enemy.pos in adjacent_ids:
                adjacent_enemies.append(enemy)
        return adjacent_enemies

    def adjacent_allies(self, champ):
        adjacent_allies = []
        neighbor_ids = [cell.id for cell in self.map.get_cell_from_id(champ.pos).neighbors]
        for allie in self.champs_allie_team(champ):
            if allie.pos in neighbor_ids:
                adjacent_allies.append(allie)
        return adjacent_allies

    def furthest_enemy_away(self, champ):
        start_cell = self.map.get_cell_from_id(champ.pos)
        furthest_enemy = None
        furthest_enemy_dist = 0
        for enemy in self.champs_enemy_team(champ):
            goal_cell = self.map.get_cell_from_id(enemy.pos)
            dist_to_enemy = self.map.distance(start_cell, goal_cell)
            if furthest_enemy_dist < dist_to_enemy:
                furthest_enemy = enemy
        return furthest_enemy

    def get_n_closest_allies(self, champ, n):
        allies = self.allie_champs_alive(champ)
        ordered_by_distance = sorted(allies, key=lambda allie: self.map.distance_id(champ.pos, allie.pos))
        return ordered_by_distance[:min(n, len(allies))]

    def get_enemy_synergies(self, champ):
        if champ in self.team_bot:
            return self.bot_synergy
        else:
            return self.top_synergy

    def knockback(self, enemy, k_distance, user):
        pass

    def get_enemies_in_area(self, user, area):
        enemies = []
        for cell in area:
            if cell is not None:
                for enemy in self.enemy_champs_alive(user):
                    if cell.id == enemy.pos:
                        enemies.append(enemy)
        return enemies

    def get_ability_area(self, target, champ, hexrange=None):
        area_cell_ids = []
        if hexrange is None:
            if target is None:
                hexrange = 20
            else:
                hexrange = self.map.distance(target.my_cell, champ.my_cell)

        hexrange = int(hexrange)
        if target is None:

            first_direction = champ.direction
            current_cell_id = champ.pos
            for i in range(hexrange):
                current_cell_id = self.map.get_id_in_direction(current_cell_id, first_direction)
                area_cell_ids.append(current_cell_id)
        else:
            target = self._im_target(target.pos, champ.pos)
            current_cell_id = champ.pos

            for i in range(hexrange):
                current_cell_id = self._get_next_cell_id(current_cell_id, target)
                area_cell_ids.append(current_cell_id)
        area = []
        for id_ in area_cell_ids:
            area.append(self.map.get_cell_from_id(id_))
        return area

    def get_direction(self, start, goal):
        if goal is None:
            if self.get_champ_from_cell(self.map.get_cell_from_id(start)).pos in self.team_bot:
                return 0
            else:
                return 3

        degree = abs(self._degree(start, goal))
        turning_degree = math.degrees(math.atan(1 / 1.5))
        # rechts oben
        if goal[0] - start[0] >= 0 and goal[1] - start[1] <= 0:
            if degree < turning_degree:
                return 1
            else:
                return 0
        # links oben
        elif goal[0] - start[0] < 0 and goal[1] - start[1] <= 0:
            if degree < turning_degree:
                return 4
            else:
                return 5
        # rechts unten
        elif goal[0] - start[0] >= 0 and goal[1] - start[1] > 0:
            if degree < turning_degree:
                return 1
            else:
                return 2
        # links unten
        elif goal[0] - start[0] < 0 and goal[1] - start[1] > 0:
            if degree < turning_degree:
                return 4
            else:
                return 3

    def render(self, surface):
        self.map.draw(surface)
        for event in self.events:
            if event.is_active:
                event.draw(surface)
            else:
                self.events.remove(event)

        for top, bot in zip(self.team_top, self.team_bot):
            if bot.alive:
                bot.draw(surface, self, "team_bot")
            if top.alive:
                top.draw(surface, self, "team_top")
        if self.game_over:
            self._draw_winner(surface)

        # show synergies
        font = pygame.font.SysFont("Comic Sans Ms", 25)
        for i, item in enumerate(self.bot_synergy.items()):
            syn_text = font.render(f"{item[0]} : {str(item[1])}", True, (0, 0, 0))
            surface.blit(syn_text, (10, 550 - (15 * i)))
        for i, item in enumerate(self.top_synergy.items()):
            syn_text = font.render(f"{item[0]} : {str(item[1])}", True, (0, 0, 0))
            surface.blit(syn_text, (650, 550 - (15 * i)))

        # show all champs with number
        for i, champ in enumerate(self.team_top + self.team_bot):
            champ_text = font.render(f"{champ.name} [{champ.rank}]: hp={int(champ.current_health)}, mana={int(champ.mana)}", True, (0, 0, 0))
            surface.blit(champ_text, (10, 600 + (i * 15)))

    @staticmethod
    def _dot_damage(target):
        for dot in ["gwound"]:
            for status_effect in target.status_effects:
                if status_effect.has(dot):
                    status_effect.proc()

    def _set_team_synergies(self):
        bot_names = []
        for champ in self.team_bot:
            if champ.name not in bot_names:
                bot_names.append(champ.name)
            for type_ in champ.class_ + champ.origin:
                if type_ not in self.bot_synergy:
                    self.bot_synergy[type_] = 1
                else:
                    self.bot_synergy[type_] += 1

        top_names = []
        for champ in self.team_top:
            if champ.name not in top_names:
                top_names.append(champ.name)
                for type_ in champ.class_ + champ.origin:
                    if type_ not in self.top_synergy:
                        self.top_synergy[type_] = 1
                    else:
                        self.top_synergy[type_] += 1

    def _trigger_fight_start(self):
        # check synergies
        # disable items

        # trigger items like: Zeke' Herald

        for champ in self.team_top + self.team_bot:
            if champ in self.team_bot:
                champ.team_synergies = self.bot_synergy
            else:
                champ.team_synergies = self.top_synergy

            # shield testing purpose
            # champ.shields.append(Shield(champ, self, self.now, 100, duration=7))

            # @synergy: Sorcerer
            synergy_name = "Sorcerer"
            if synergy_name in self.top_synergy:
                n_syn = self.top_synergy[synergy_name]
                ap_bonus = 0
                if n_syn >= 9:
                    ap_bonus += 175
                elif n_syn >= 6:
                    ap_bonus += 100
                elif n_syn >= 3:
                    ap_bonus += 40
                for allie in self.team_top:
                    allie.start_ap_bonus += ap_bonus
            elif synergy_name in self.bot_synergy:
                n_syn = self.bot_synergy[synergy_name]
                ap_bonus = 0
                if n_syn >= 9:
                    ap_bonus += 175
                elif n_syn >= 6:
                    ap_bonus += 100
                elif n_syn >= 3:
                    ap_bonus += 40
                for allie in self.team_bot:
                    allie.start_ap_bonus += ap_bonus

            # @synergy: Exile
            synergy_name = "Exile"
            if synergy_name in champ.origin:
                if len(self.adjacent_allies(champ)) == 0:
                    champ.shields.append(Shield(champ, self, self.now, champ.max_health))

            # @todo: add combination list for Thiefs Glove
            # @body: see twitter link in [Link](https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:Thief%27s_Gloves#cite_note-0)
            # @item: Thief's Gloves
            item_name = "Thief's Gloves"
            if champ.item_count(item_name) > 0:
                # tier rises with level
                random_items = []
                champ.items.extend(random_items)

            # @item: Hand of Justice
            item_name = "Hand of Justice"
            if champ.item_count(item_name) > 0:
                n_item = champ.item_count(item_name)
                for item in champ.items:
                    if random.random() <= 0.5:  # get aa and sa increase by 40%
                        item.name = "Hand of Justice damage"
                    else:  # aa heal 40 onhit
                        item.name = "Hand of Justice heal"

            possible_positions = [(champ.pos[0] + 2, champ.pos[1]),
                                  (champ.pos[0] - 4, champ.pos[1]),
                                  (champ.pos[0] + 4, champ.pos[1]),
                                  (champ.pos[0] - 2, champ.pos[1]),
                                  champ.pos]
            as_bonus = 1  # zekes
            shield_bonus = 0  # solari
            # @item: Zeke's Herald
            item_name = "Zeke's Herald"
            if champ.item_count(item_name) > 0:
                as_bonus += 0.15 * champ.item_count(item_name)

            # @item: Locket of the Iron Solari
            item_name = "Locket of the Iron Solari"
            if champ.item_count(item_name) > 0:
                shield_bonus += 300 * champ.item_count(item_name)

            for allie in self.champs_allie_team(champ):
                if allie.pos in possible_positions:
                    # give bonus to all champs in row_range <= 2
                    allie.bonus_aa_cc += allie.base_aa_cc * as_bonus
                    # give shield for 7 seconds to all in row_range <= 2
                    allie.shields.append(Shield(allie, self, self.now, shield_bonus, duration=7))

            # @item: Zephyr
            item_name = "Zephyr"
            if champ.item_count(item_name) > 0:
                mirror_posi = champ.init_pos
                for enemy in self.enemy_champs_alive(champ):
                    if enemy.init_pos == mirror_posi:
                        enemy.banish(self.map)

            # @synergy: Robot
            synergy_name = "Robot"
            if synergy_name in champ.origin:
                champ.mana = champ.max_mana

        # @synergy: Elementalist
        synergy_name = "Elementalist"
        if synergy_name in self.top_synergy:
            if self.top_synergy[synergy_name] >= 3:
                self._summon_golem(self.team_top)
        if synergy_name in self.bot_synergy:
            if self.bot_synergy[synergy_name] >= 3:
                self._summon_golem(self.team_bot)

        # @synergy: Guradian
        synergy_name = "Guardian"
        if synergy_name in self.top_synergy:
            n_syn = self.top_synergy[synergy_name]
            if n_syn >= 2:
                for champ in self.team_top:
                    if synergy_name in champ.class_:
                        for allie in self.adjacent_allies(champ):
                            allie.base_armor += 35
        if synergy_name in self.bot_synergy:
            n_syn = self.bot_synergy[synergy_name]
            if n_syn >= 2:
                for champ in self.team_bot:
                    if synergy_name in champ.class_:
                        for allie in self.adjacent_allies(champ):
                            allie.base_armor += 35

        # @synergy: Phantom
        synergy_name = "Phantom"
        if synergy_name in self.bot_synergy:
            if self.bot_synergy[synergy_name] >= 2:
                random.choice(self.team_top).current_health = 100
        elif synergy_name in self.top_synergy:
            if self.top_synergy[synergy_name] >= 2:
                random.choice(self.team_bot).current_health = 100

        # @synergy: Imperial
        synergy_name = "Imperial"
        if synergy_name in self.bot_synergy:
            imperial_champs = [champ for champ in self.team_bot if synergy_name in champ.origin]
            n_syn = self.bot_synergy[synergy_name]
            if n_syn >= 4:
                for champ in imperial_champs:
                    champ.imperial_buff = True
            elif n_syn >= 2:
                random.choice(imperial_champs).imperial_buff = True
        elif synergy_name in self.top_synergy:
            imperial_champs = [champ for champ in self.team_top if synergy_name in champ.origin]
            n_syn = self.top_synergy[synergy_name]
            if n_syn >= 4:
                for champ in imperial_champs:
                    champ.imperial_buff = True
            elif n_syn >= 2:
                random.choice(imperial_champs).imperial_buff = True

        # @synergy: Noble
        synergy_name = "Noble"
        if synergy_name in self.bot_synergy:
            noble_champs = [champ for champ in self.team_bot if synergy_name in champ.origin]
            n_syn = self.bot_synergy[synergy_name]
            if n_syn >= 6:
                for champ in noble_champs:
                    champ.noble_buff = True
            elif n_syn >= 3:
                random.choice(noble_champs).noble_buff = True
        elif synergy_name in self.top_synergy:
            noble_champs = [champ for champ in self.team_top if synergy_name in champ.origin]
            n_syn = self.top_synergy[synergy_name]
            if n_syn >= 6:
                for champ in noble_champs:
                    champ.noble_buff = True
            elif n_syn >= 3:
                random.choice(noble_champs).noble_buff = True

        # @synergy: Void
        synergy_name = "Void"
        if synergy_name in self.bot_synergy:
            void_champs = [champ for champ in self.team_bot if synergy_name in champ.origin]
            n_syn = self.bot_synergy[synergy_name]
            if n_syn >= 4:
                for champ in void_champs:
                    champ.void_buff = True
            elif n_syn >= 2:
                random.choice(void_champs).void_buff = True
        elif synergy_name in self.top_synergy:
            void_champs = [champ for champ in self.team_top if synergy_name in champ.origin]
            n_syn = self.top_synergy[synergy_name]
            if n_syn >= 4:
                for champ in void_champs:
                    champ.void_buff = True
            elif n_syn >= 2:
                random.choice(void_champs).void_buff = True

        # @synergy: Brawler
        synergy_name = "Brawler"
        if synergy_name in self.bot_synergy:
            n_syn = self.bot_synergy[synergy_name]
            max_health_bonus = 0
            if n_syn >= 6:
                max_health_bonus += 900
            elif n_syn >= 4:
                max_health_bonus += 500
            elif n_syn >= 2:
                max_health_bonus += 250
            for champ in self.team_bot:
                if synergy_name in champ.class_:
                    champ.bonus_health += max_health_bonus
        elif synergy_name in self.top_synergy:
            n_syn = self.top_synergy[synergy_name]
            max_health_bonus = 0
            if n_syn >= 6:
                max_health_bonus += 900
            elif n_syn >= 4:
                max_health_bonus += 500
            elif n_syn >= 2:
                max_health_bonus += 250
            for champ in self.team_top:
                if synergy_name in champ.class_:
                    champ.bonus_health += max_health_bonus

        # @synergy: Hextech
        synergy_name = "Hextech"
        four_bonus = 2
        two_bonus = 1
        self.hextech_tick = self.now
        if synergy_name in self.bot_synergy:
            if self.bot_synergy[synergy_name] >= 4:
                n_syn = four_bonus
            elif self.bot_synergy[synergy_name] >= 2:
                n_syn = two_bonus
            else:
                n_syn = 0
            if n_syn > 0:
                possible_bomb_targets = [enemy for enemy in self.team_top if len(enemy.items) > 0]
                bomb_target = random.choice(possible_bomb_targets)
                target_cell = self.map.get_cell_from_id(bomb_target.pos)
                effected_area_ids = [cell.id for cell in self.map.get_all_cells_in_range(target_cell, n_syn)]
                for enemy in self.team_top:
                    if enemy.pos in effected_area_ids:
                        enemy.disables_items = enemy.items
                        enemy.items = []
                        self.hextech_disabled_champs.append(enemy)
        elif synergy_name in self.top_synergy:
            if self.top_synergy[synergy_name] >= 4:
                n_syn = four_bonus
            elif self.top_synergy[synergy_name] >= 2:
                n_syn = two_bonus
            else:
                n_syn = 0
            if n_syn > 0:
                possible_bomb_targets = [enemy for enemy in self.team_bot if len(enemy.items) > 0]
                bomb_target = random.choice(possible_bomb_targets)
                target_cell = self.map.get_cell_from_id(bomb_target.pos)
                effected_area_ids = [cell.id for cell in self.map.get_all_cells_in_range(target_cell, n_syn)]
                for enemy in self.team_bot:
                    if enemy.pos in effected_area_ids:
                        enemy.disables_items = enemy.items
                        enemy.items = []
                        self.hextech_disabled_champs.append(enemy)

        # @synergy: Elementalist
        synergy_name = "Elementalist"
        if synergy_name in self.top_synergy:
            if self.top_synergy[synergy_name] >= 3:
                elementalists = [champ for champ in self.team_top if synergy_name in champ.class_]
                summon_cell = None
                summon_cell_dist = 9999999
                for champ in elementalists:
                    for cell in self.map.get_cell_from_id(champ.pos).free_neighbors:
                        for enemy in self.team_bot:
                            enemy_cell = self.map.get_cell_from_id(enemy.pos)
                            dist = self.map.distance(cell, enemy_cell)
                            if dist < summon_cell_dist:
                                summon_cell = cell
                if summon_cell:
                    # summon golem with 2200 health, 100 ad, and 40 armor
                    pass
        elif synergy_name in self.bot_synergy:
            if self.bot_synergy[synergy_name] >= 3:
                elementalists = [champ for champ in self.team_bot if synergy_name in champ.class_]
                summon_cell = None
                summon_cell_dist = 9999999
                for champ in elementalists:
                    for cell in self.map.get_cell_from_id(champ.pos).free_neighbors:
                        for enemy in self.team_top:
                            enemy_cell = self.map.get_cell_from_id(enemy.pos)
                            dist = self.map.distance(cell, enemy_cell)
                            if dist < summon_cell_dist:
                                summon_cell = cell
                if summon_cell:
                    # summon golem with 2200 health, 100 ad, and 40 armor
                    pass

        # ----- Fight Start -----

        # @synergy: Assassin
        synergy_name = "Assassin"
        for champ in self.team_top + self.team_bot:
            if synergy_name in champ.class_ and not champ.has_effect("banish"):
                furthest_enemy = self.furthest_enemy_away(champ)
                new_cell = random.choice(self.map.get_cell_from_id(furthest_enemy.pos).free_neighbors)
                champ.move_to(new_cell, self)
                champ.untargetable(1, self)

    def _activate_aura(self, champ):
        # @item: Warmog's Armor
        item_name = "Warmog's Armor"
        if champ.item_count(item_name) > 0:
            regeneration = 0
            for item in champ.items:
                if item.last_proc is None or self.now - item.last_proc >= 1000 and item.name == item_name:
                    item.last_proc = self.now
                    regeneration += 0.06 * (champ.max_health - champ.current_health)
            if regeneration > 400:
                regeneration = 400
            if regeneration > 0:
                champ.heal(regeneration, self.map)

        # @item: Frozen Heart
        item_name = "Frozen Heart"
        if champ.item_count(item_name) > 0:
            n_items = champ.item_count(item_name)
            for enemy in self.adjacent_enemies(champ):
                if enemy.has_effect_with_name(item_name):
                    for effect in enemy.status_effects:
                        if effect.name == item_name:
                            enemy.status_effects.remove(effect)
                enemy.status_effects.append(
                    StatusEffect(self.map, 4, item_name, effects=["frozen_heart_" + str(n_items)]))

    def _get_next_cell_id(self, current_cell_id, target_id):
        direction = self.get_direction(current_cell_id, target_id)

        next_cell_id = self.map.get_id_in_direction(current_cell_id, direction)
        return next_cell_id

    @staticmethod
    def _im_target(target, start):
        x = target[0] - start[0]
        y = target[1] - start[1]
        im_target = (target[0] + 10*x, target[1] + 10*y)
        return im_target

    @staticmethod
    def _degree(start_id, goal_id):
        x = (goal_id[0] - start_id[0]) / 2
        y = start_id[1] - goal_id[1]
        if x == 0:
            return 90
        return abs(math.degrees(math.atan(y / x)))

    def _enemy_team_item_count(self, champ, item_name):
        item_count = 0
        for enemy in self.champs_enemy_team(champ):
            item_count += enemy.item_count(item_name)
        return item_count

    def _update_cell_status(self, champ, status):
        cell = self.map.get_cell_from_id(champ.pos)
        cell.taken = status

    @staticmethod
    def _check_valid_pos(r, c, team):
        init_pos_list = [champ.pos for champ in team]
        if len(init_pos_list) != len(set(init_pos_list)):
            raise Exception("Champs share same init_pos.")
        for c_pos in init_pos_list:
            if c_pos[0] > (r - 1) or c_pos[1] > (c - 1):
                raise Exception("Champ is placed outside of the Board.")

    def _place_champs(self):
        # set positions for bot team
        logger.info("Team BOT:")
        for champ in self.team_bot:
            logger.info(f"{champ.name} spawned on {champ.pos} with rank {champ.rank}")
            if (champ.pos[1] % 2) == 0:
                champ.pos = (champ.pos[0] * 2 + 1, champ.pos[1] + 3)
            else:
                champ.pos = (champ.pos[0] * 2, champ.pos[1] + 3)

        # set positions for top team
        logger.info("Team TOP:")
        for champ in self.team_top:
            logger.info(f"{champ.name} spawned on {champ.pos} with rank {champ.rank}")
            cols = self.map.n_cols
            rows = int(self.map.n_rows / 2)
            if (champ.pos[1] % 2) == 0:
                champ.pos = (((cols * 2) - 2) - (champ.pos[0] * 2), rows - 1 - champ.pos[1])
            else:
                champ.pos = (((cols * 2) - 1) - (champ.pos[0] * 2), rows - 1 - champ.pos[1])

        # lock positions for every champ

        for champ in self.team_top + self.team_bot:
            self._update_cell_status(champ, True)
            champ.pos = (int(champ.pos[0]), int(champ.pos[1]))
            champ.fight = self

    def _draw_winner(self, surface):
        team_top, team_bot = self.result
        if len(team_top) > len(team_bot):
            show = f"Team TOP won with: {len(team_top)} champs alive"

        else:
            show = f"Team BOT won with: {len(team_bot)} champs alive"

        font = pygame.font.SysFont("Comic Sans Ms", 40)
        text = font.render(show, False, (255, 0, 0))
        surface.blit(text, (0, 0))

        team_font = pygame.font.SysFont("Comic Sans Ms", 30)
        team = f"Champions alive:"
        team_text = team_font.render(team, False, (0, 0, 0))
        surface.blit(team_text, (0, 100))

        for i, champ in enumerate(team_top + team_bot):
            champ = f"{champ.name} [Rank {champ.rank}] with {int(champ.current_health)}/{int(champ.max_health)}"
            champ_text = team_font.render(champ, False, (0, 0, 0))
            surface.blit(champ_text, (0, 100 + ((i+1) * 25)))

    def _summon_golem(self, team):
        synergy_name = "Elementalist"
        champs = [champ for champ in team if synergy_name in champ.class_]
        best_cell = None
        best_dist = 99999
        for champ in champs:
            for free_cell in champ.my_cell.free_neighbors:
                for enemy in self.enemy_champs_alive(champ):
                    distance = self.map.distance(free_cell, enemy.my_cell)
                    if distance < best_dist:
                        best_cell = free_cell
                        best_dist = distance
        if best_cell:
            golem = Golem(best_cell.id, self)
            best_cell.taken = True
            team.append(golem)

