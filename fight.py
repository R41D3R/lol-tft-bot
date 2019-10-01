from typing import List
import random

import pygame

from board.map import Map
from helper.dummy import DummyChamp
from config import logger


class Fight:
    def __init__(self, team_bot: List[DummyChamp], team_top: List[DummyChamp]):
        self.map = Map(cell_radius=50, n_rows=6, n_cols=7, color=(0, 150, 0), space=0)
        self.team_bot = team_bot
        self.team_top = team_top
        self.path = None
        self.events = []
        self.aoe = []
        self.now = None

        self.check_valid_pos(self.map.n_cols, self.map.n_rows, team_bot)
        self.check_valid_pos(self.map.n_cols, self.map.n_rows, team_top)

    def make_fight_step(self):
        now = pygame.time.get_ticks()
        self.now = now
        champs = [champ for champ in self.team_bot + self.team_top if champ.alive]
        random.shuffle(champs)
        for champ in champs:
            champ.check_status_effects(now)
            if champ.alive and not champ.has_effect("banish"):
                logger.debug(f"{champ.name} turn")

                enemies_alive = self.enemy_champs_alive(champ)
                if len(enemies_alive) == 0:
                    break
                enemy_team = self.enemy_team_visible(champ)

                enemies_in_range = champ.get_enemies_in_range(self)
                if champ.has_effect("channeling"):
                    champ.stop_moving(self)
                    effects = [effect for effect in champ.status_effects if effect.has("channeling")]
                    for effect in effects:
                        if effect.does_proc(now):
                            champ.special_ability(self, enemies_in_range, enemy_team, enemies_alive, now)
                elif not champ.has_effect("airborne") and not champ.has_effect("stun"):
                    if champ.mana >= champ.max_mana:
                        champ.stop_moving(self)
                        champ.special_ability(self, enemies_in_range, enemy_team, enemies_alive, now)
                        champ.mana = 0
                    elif len(enemies_in_range) > 0 and (champ.target_pos is None):
                        champ.stop_moving(self)
                        if now - champ.aa_last >= champ.aa_cc:
                            if not champ.has_effect("disarm"):
                                logger.debug(f"{champ.name} attacks")
                                champ.autoattack(now, self, enemies_in_range)
                            else:
                                logger.debug(f"{champ.name} is disarmed")
                        else:
                            logger.debug(f"{champ.name} aa is on cooldown")
                    elif len(enemies_in_range) > 0 and champ.target_pos is None:
                        champ.stop_moving(self)
                        logger.debug(f"{champ.name} waits for next aa")
                    else:
                        new_next_pos = champ.get_move_to_closest_enemy(enemy_team, self.map)
                        if (new_next_pos is None or champ.has_effect("root")) and champ.target_pos is None:
                            logger.debug(f"{champ.name} can not find a next_pos or is rooted")
                            champ.stop_moving(self)
                        else:
                            if champ.target_pos is None:
                                champ.start_pos = champ.pos
                                champ.target_pos = new_next_pos.id
                                self.map.get_cell_from_id(champ.target_pos).taken = True
                            champ.move_progress += 0.05
                            logger.debug(f"{champ.name} moves")
                            if champ.move_progress >= 1:
                                champ.move_progress = 0
                                self.map.get_cell_from_id(champ.pos).taken = False
                                champ.pos = champ.target_pos
                                champ.stop_moving(self)

    @property
    def game_over(self):
        return all(not champ.alive for champ in self.team_top) \
               or all(not champ.alive for champ in self.team_bot)

    @property
    def result(self):
        return [champ for champ in self.team_top if champ.alive is True], \
               [champ for champ in self.team_bot if champ.alive is True]

    def draw_winner(self, surface):
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
            if champ.id in area_ids:
                champs_in_area.append(champ)
        return champs_in_area

    @property
    def champions_alive(self):
        return [champ for champ in self.team_top + self.team_bot if champ.alive]

    def enemy_champs_alive(self, champ):
        enemy_team = self.champs_enemy_team(champ)
        return [enemy for enemy in enemy_team if enemy.alive]

    def enemy_team_visible(self, champ):
        return [enemy for enemy in self.enemy_champs_alive(champ) if not enemy.has_effect("banish") and not enemy.has_effect("stealth")]

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

    def render(self, surface):
        self.map.draw(surface)
        for event in self.events:
            if event.is_active:
                event.draw(surface, self.map)
            else:
                self.events.remove(event)

        for top, bot in zip(self.team_top, self.team_bot):
            if bot.alive:
                bot.draw(surface, self, "team_bot")
            if top.alive:
                top.draw(surface, self, "team_top")
        if self.game_over:
            self.draw_winner(surface)

    def update_cell_status(self, champ, status):
        cell = self.map.get_cell_from_id(champ.pos)
        cell.taken = status

    @staticmethod
    def check_valid_pos(r, c, team):
        init_pos_list = [champ.pos for champ in team]
        if len(init_pos_list) != len(set(init_pos_list)):
            raise Exception("Champs share same init_pos.")
        for c_pos in init_pos_list:
            if c_pos[0] > (r - 1) or c_pos[1] > (c - 1):
                raise Exception("Champ is placed outside of the Board.")

    def place_champs(self):
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
            self.update_cell_status(champ, True)
            champ.pos = (int(champ.pos[0]), int(champ.pos[1]))

    # def show_rnd_shortest_path(self, surface):
    #     start = self.team_bot[0]
    #     end = self.team_top[0]
    #     if self.path:
    #         pass
    #     else:
    #         print("run path")
    #         self.path = start.find_shortest_path_to_enemy(end, self.map)
    #     for cell in self.path:
    #         cell.draw(surface, (0, 130, 124))
