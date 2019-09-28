from typing import List
import random

import pygame

from board.map import Map
from helper.dummy import DummyChamp


class Fight:
    def __init__(self, team_bot: List[DummyChamp], team_top: List[DummyChamp]):
        self.map = Map(cell_radius=50, n_rows=6, n_cols=7, color=(0, 150, 0), space=0)
        self.team_bot = team_bot
        self.team_top = team_top
        self.path = None

        self.check_valid_pos(self.map.n_cols, self.map.n_rows, team_bot)
        self.check_valid_pos(self.map.n_cols, self.map.n_rows, team_top)

    def make_fight_step(self):
        now = pygame.time.get_ticks()
        champs = [champ for champ in self.team_bot + self.team_top if champ.alive]
        random.shuffle(champs)
        for champ in champs:
            if champ.alive:
                print(f"{champ.name} turn")

                #       use ability if enemy_target in range
                #       autoattack if enemy_target in range
                enemy_team = [enemy for enemy in self.champs_enemy_team(champ) if enemy.alive]
                if len(enemy_team) == 0:
                    break
                current_cell = self.map.get_cell_from_id(champ.pos)

                enemys_around = [enemy for neighbor in current_cell.neighbors for enemy in enemy_team if
                                 enemy.pos == neighbor.id]

                if champ.mana >= 100:
                    champ.special_ability(self)
                    champ.mana = 0
                elif now - champ.aa_last >= champ.aa_cc and len(enemys_around) > 0:
                    print(f"{champ.name} attacks")
                    target_enemy = random.choice(enemys_around)
                    champ.aa_last = now
                    target_enemy.get_physical_damage(champ.aa_damage(), self.map)
                    champ.mana += champ.mana_on_aa
                elif len(enemys_around) > 0:
                    print(f"{champ.name} waits for next aa")
                    pass
                else:
                    new_next_pos = champ.get_move_to_closest_enemy(enemy_team, self.map)
                    if new_next_pos is None:
                        print(f"{champ.name} can not find a next_pos")
                        pass
                    else:
                        print(f"{champ.name} moves")
                        if new_next_pos != champ.next_pos:
                            champ.next_pos = new_next_pos.id
                        champ.move_progress += 0.03
                        print(champ.move_progress)
                        if champ.move_progress >= 0.5:
                            champ.move_progress = 0
                            self.map.get_cell_from_id(champ.next_pos).taken = True
                            self.map.get_cell_from_id(champ.pos).taken = False
                            champ.pos = champ.next_pos
                            champ.next_pos = None

    @property
    def game_over(self):
        return all(not champ.alive for champ in self.team_top) \
               or all(not champ.alive for champ in self.team_bot)

    @property
    def result(self):
        return [champ for champ in self.team_top if champ.alive is True], \
               [champ for champ in self.team_bot if champ.alive is True]

    def get_champ_from_cell(self, cell):
        for champ in self.team_top + self.team_bot:
            if champ.pos == cell.id:
                return champ
        else:
            return None

    @property
    def champions_alive(self):
        return [champ for champ in self.team_top + self.team_bot if champ.alive]

    def champs_enemy_team(self, champ):
        if champ in self.team_bot:
            return self.team_top
        else:
            return self.team_bot

    def render(self, surface):
        self.map.draw(surface)
        for top, bot in zip(self.team_top, self.team_bot):
            if bot.alive:
                bot.draw(surface, self.map, "team_bot")
            if top.alive:
                top.draw(surface, self.map, "team_top")

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
        print("Team BOT:")
        for champ in self.team_bot:
            print(f"{champ.name} spawned on {champ.pos}")
            if (champ.pos[1] % 2) == 0:
                champ.pos = (champ.pos[0] * 2 + 1, champ.pos[1] + 3)
            else:
                champ.pos = (champ.pos[0] * 2, champ.pos[1] + 3)

        # set positions for top team
        print("Team TOP:")
        for champ in self.team_top:
            print(f"{champ.name} spawned on {champ.pos}")
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
