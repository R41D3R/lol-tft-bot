import random

import pygame

from helper.pathfinding_helper import PriorityQueue
from helper.dummy_vision_event import DummyEvent
from helper.damage_visualization import DummyDamage
from helper.status_effect import StatusEffect, GWounds, Channelling
from config import logger


class DummyChamp:
    def __init__(self, init_pos, champ_item, rank, items=None):
        if items is None:
            self.items = []
        else:
            self.items = items
        self.rank = rank

        self.base_stats = champ_item[1]
        # base stats
        self.range = self.base_stats["range"]
        self.name = champ_item[0]
        self.base_health = self.base_stats["health"][rank - 1]
        self.base_ad = self.base_stats["ad"][rank - 1]
        self.base_aa_cc = self.base_stats["attack_speed"]
        self.max_mana = self.base_stats["mana"]
        self.mana = self.base_stats["starting_mana"] + (20 * len([item for item in self.items if "mana" in item.attribute]))
        self.base_armor = self.base_stats["armor"]
        self.base_mr = self.base_stats["mr"]
        self.base_crit_chance = 0.25
        self.base_crit_bonus = 0.5
        self.base_dodge_chance = 0

        # positions
        self.pos = init_pos
        self.move_progress = 0
        self.start_pos = None
        self.target_pos = None

        self.alive = True
        self.current_health = self.max_health
        self.aa_last = 0  # pygame.time.get_ticks()
        self.damage_events = []
        self.status_effects = []
        self.channelling = False
        self.last_target = None

    def autoattack(self, time, fight, enemies_in_range):
        target = self.get_target(enemies_in_range)
        self.aa_last = time
        hitted = target.get_physical_damage(self.aa_damage(), fight.map)  # for on_hit items
        if not self.has_effect("mana-lock"):
            self.mana += self.mana_on_aa

    def heal(self, amount):
        if self.has_effect("gwound"):
            amount *= 0.2
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def special_ability(self, fight, in_range, visible, alive, time):
        # nearby enemies get Mega Crit
        effected_area = fight.map.get_cell_from_id(self.pos).neighbors
        fight.events.append(DummyEvent(1000, (36, 36, 36), effected_area))
        for n_cell in effected_area:
            for enemy in [champ
                          for champ in fight.champs_enemy_team(self)
                          if champ.alive]:
                if enemy.pos == n_cell.id:
                    enemy.get_magic_damage(self.aa_damage(crit=True) * 2, fight.map)

    # ----- Stat Properties ------

    @property
    def aa_cc(self):
        return int(1 / (self.base_aa_cc + (0.2 * self.item_sum_from("attack_speed"))) * 1000)

    @property
    def ad(self):
        return self.base_ad + (15 * self.item_sum_from("ad"))

    @property
    def dodge_chance(self):
        return 0.1 * self.item_sum_from("dodge_chance")

    @property
    def crit_chance(self):
        return self.base_crit_chance + (0.1 * self.item_sum_from("crit_chance"))

    @property
    def max_health(self):
        return self.base_health + (200 * self.item_sum_from("health"))

    @property
    def armor(self):
        return self.base_armor + (20 * self.item_sum_from("armor"))

    @property
    def mr(self):
        return self.base_mr + (20 * self.item_sum_from("mr"))

    def item_sum_from(self, attribute):
        return sum([item.get_attribute_counter(attribute) for item in self.items])

    @property
    def ability_power_multiplier(self):
        # + ninja bonus + sorcerer bonus) * (1 + (#of_rabadons * 0.5))
        return 1 + (0.2 * len([item for item in self.items if item.attribute == "ap"]))

    @property
    def mana_on_aa(self):
        # sorcerer and elementalist gain 2x -> cap 20
        if self.rank <= 1:  # how to handle 0-Star units that got downgraded?
            return 6 + random.randint(1, 4)
        else:
            return 10

    @property
    def crit_multiplier(self):
        return 1 + self.base_crit_bonus  # + additional bonus with items, ...

    def aa_damage(self, crit=False):
        if crit or random.random() <= self.crit_chance:
            return self.ad * self.crit_multiplier
        else:
            return self.ad

    # ----- Status Effects ------

    def has_effect(self, effect):
        for status_effect in self.status_effects:
            if status_effect.has(effect):
                return True
        return False

    def has_effect_with_name(self, name):
        for status_effect in self.status_effects:
            if status_effect.name == name:
                return True
        return False

    def check_status_effects(self):
        for status_effect in self.status_effects:
            if not status_effect.is_active:
                self.status_effects.remove(status_effect)

    def mana_lock(self, map_):
        self.status_effects.append(StatusEffect(map_, 3, "Hush", effects=["mana-lock"]))

    def banish(self, map_):
        self.status_effects.append(StatusEffect(map_, 6, "Zephyr", effects=["banish"]))

    def gwounds(self, duration, map_, dot=False):
        self.status_effects.append(GWounds(self, map_, duration, "Grievous Wounds", damage=dot))

    def stealth(self, map_):
        self.status_effects.append(StatusEffect(map_, 10**10, "Stealth", effects=["stealth"]))

    def stun(self, duration, map_):
        self.status_effects.append(StatusEffect(map_, duration, "Stun", effects=["stun"]))

    def root(self, duration, map_):
        self.status_effects.append(StatusEffect(map_, duration, "Root", effects=["root"]))

    def airborne(self, duration, map_):
        self.status_effects.append(StatusEffect(map_, duration, "Airborne", effects=["airborne"]))

    def shrink(self):
        if self.rank > 0:
            self.rank -= 1
            health_before = self.current_health
            self.base_health = self.base_stats["health"][self.rank]
            if health_before >= self.base_health:
                self.current_health = self.max_health
            self.base_ad = self.base_stats["ad"][self.rank]

    def channeling(self, fight, duration, name, proc_interval=None):
        self.status_effects.append(Channelling(self, fight, duration, name, proc_interval))

    # ----- Get Damage and Alive -----

    def get_physical_damage(self, incoming_damage, map_):
        return self.get_damage("physical", incoming_damage, map_)

    def get_damage(self, type_, incoming_damage, map_):
        types = {
            "physical": self.armor,
            "magic": self.mr,
            "true": 0,
        }
        if random.random() >= self.dodge_chance:
            resistance = types[type_]
            damage_reduction = (100 / (resistance + 100))
            real_damage = incoming_damage * damage_reduction
            self.current_health -= real_damage
            self.damage_events.append(DummyDamage(real_damage, self.position(map_), type_))
            self.mana += self.mana_on_aa
            self.check_alive(map_)
            return True
        else:
            return False

    def get_magic_damage(self, incoming_damage, map_):
        return self.get_damage("magic", incoming_damage, map_)

    def check_alive(self, map_):
        if self.current_health <= 0:
            self.kill(map_)

    def kill(self, map_):
        logger.debug(f"Champ died on {self.pos}")
        self.alive = False
        if self.pos is not None:
            map_.get_cell_from_id(self.pos).taken = False
        # if self.next_pos is not None:
        #     map_.get_cell_from_id(self.next_pos).taken = False
        if self.target_pos is not None:
            map_.get_cell_from_id(self.target_pos).taken = False

    # ----- Helper -----

    def get_enemies_in_range(self, fight):
        current_cell = fight.map.get_cell_from_id(self.pos)
        enemy_champs_visible = fight.enemy_team_visible(self)
        cell_ids_in_range = [cell.id for cell in fight.map.get_all_cells_in_range(current_cell, self.range)]
        return [enemy for enemy in enemy_champs_visible if enemy.pos in cell_ids_in_range]

    def get_allies_around(self, fight):
        current_cell_neighbors_ids = fight.map.get_cell_from_id(self.pos)
        return [allie for allie in fight.champs_allie_team(self) if allie.pos in current_cell_neighbors_ids]

    def get_target(self, enemies_in_range):
        if self.last_target is None or self.last_target not in enemies_in_range:
            self.last_target = random.choice(enemies_in_range)
        return self.last_target

    # ----- rendering -----

    def draw(self, surface, map_, team):
        font = pygame.font.SysFont("Comic Sans Ms", 20)
        player_pos = self.position(map_)

        # ----- player -----
        if team == "team_bot":
            color = (67, 52, 235)
        else:
            color = (229, 235, 52)
        pygame.draw.circle(surface,
                           color,
                           player_pos,
                           30)

        # ----- health bar -----
        hb_width = 60
        hb_height = 10
        hb_x = player_pos[0] - (hb_width / 2)
        hb_y = player_pos[1] - (hb_height / 2)
        # health background bar
        pygame.draw.rect(surface, (0, 0, 0), (hb_x, hb_y, hb_width, hb_height))
        # health progress bar
        pygame.draw.rect(surface, (0, 130, 46), (hb_x, hb_y, int(hb_width * self.current_health / self.max_health), hb_height))

        # ----- mana bar -----
        mb_width = 60
        mb_height = 10
        mb_x = player_pos[0] - (mb_width / 2)
        mb_y = hb_y + mb_height
        # mana background bar
        pygame.draw.rect(surface, (0, 0, 0), (mb_x, mb_y, mb_width, mb_height))
        # mana progress bar
        pygame.draw.rect(surface, (52, 219, 235), (mb_x, mb_y, int(mb_width * self.mana / self.max_mana), mb_height))

        # ----- name ------
        text = font.render(f"{self.name} [{self.rank}]", False, (0, 0, 0))
        surface.blit(text, (player_pos[0] - 30, player_pos[1] - 20))

        # ----- damage -----
        for dmg in self.damage_events:
            if dmg.is_active:
                dmg.render(surface)
            else:
                self.damage_events.remove(dmg)

    # ----- Positioning -----

    def position(self, map_):
        current_cell = map_.get_cell_from_id(self.pos)
        if self.target_pos:
            next_cell = map_.get_cell_from_id(self.target_pos)
            return int(current_cell.center[0] + ((next_cell.center[0] - current_cell.center[0]) * self.move_progress)), int(current_cell.center[1] + ((next_cell.center[1] - current_cell.center[1]) * self.move_progress))
        return int(current_cell.center[0]), int(current_cell.center[1])

    def update_pos(self, new_pos):
        # check if neighbor from current pos
        # move
        pass

    def move_to(self, new_cell, fight):
        fight.map.get_cell_from_id(self.pos).taken = False
        self.start_pos = None
        self.target_pos = None
        self.move_progress = 0
        self.pos = new_cell.id
        new_cell.taken = True

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        # print(f"best path from {start.id} to {goal.id}")
        current = goal
        path = []
        while current != start:
            # print(f"from {current.id}")
            path.append(current)
            current = came_from[current]
            # print(f"to {current.id}")

        path.append(start)  # optional
        path.reverse()  # optional
        return path

    def find_shortest_path_to_enemy(self, enemy, map_):
        start = map_.get_cell_from_id(self.pos)
        if enemy.target_pos is None:
            goal_locations = map_.get_cell_from_id(enemy.pos).free_neighbors
        else:
            goal_locations = map_.get_cell_from_id(enemy.target_pos).free_neighbors
        if len(goal_locations) == 0:
            return []
        best_came_from, best_cost = {}, 9999999
        best_goal = None
        for goal in goal_locations:
            came_from, cost = dijkstra_path(start, goal)
            if came_from is None and cost is None:
                return []
            if cost < best_cost:
                best_came_from, best_cost = came_from, cost
                best_goal = goal

        return self.reconstruct_path(best_came_from, start, best_goal)

    # todo: Maybe replace pathfinding with best path for team
    def get_move_to_closest_enemy(self, enemy_team, map_):
        best_path = None
        for enemy in enemy_team:
            path = self.find_shortest_path_to_enemy(enemy, map_)
            if best_path:
                if len(path) < len(best_path):
                    best_path = path
            else:
                best_path = path
        if len(best_path) == 0:
            return None
        # print(best_path)
        return best_path[1]


def dijkstra_path(start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_ in current.free_neighbors:
            new_cost = cost_so_far[current] + 1
            if next_ not in cost_so_far or new_cost < cost_so_far[next_]:
                cost_so_far[next_] = new_cost
                priority = new_cost
                frontier.put(next_, priority)
                came_from[next_] = current
    try:
        return came_from, cost_so_far[goal]
    except KeyError:
        return None, None
