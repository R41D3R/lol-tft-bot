import random

import pygame

from helper.pathfinding_helper import PriorityQueue
from helper.dummy_vision_event import DummyEvent
from helper.damage_visualization import DummyDamage


class DummyChamp:
    def __init__(self, init_pos, champ_item, rank):
        self.rank = rank

        self.base_stats = champ_item[1]
        # base stats
        self.range = self.base_stats["range"]
        self.name = champ_item[0]
        self.base_health = self.base_stats["health"][rank - 1]
        self.ad = self.base_stats["ad"][rank - 1]
        self.aa_cc = int(1 / self.base_stats["attack_speed"] * 1000)
        self.max_mana = self.base_stats["mana"]
        self.mana = self.base_stats["starting_mana"]
        self.armor = self.base_stats["armor"]
        self.mr = self.base_stats["mr"]
        self.crit_chance = self.base_stats["crit_chance"]
        self.base_crit_bonus = 0.5

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

    @property
    def max_health(self):
        return self.base_health  # + items, ...

    @property
    def ability_power_multiplier(self):
        # (ap from items + ninja bonus + sorcerer bonus) * (1 + (#of_rabadons * 0.5))
        raise NotImplementedError()

    @property
    def mana_on_aa(self):
        # sorcerer and elementalist gain 2x -> cap 20
        if self.rank <= 1:  # how to handle 0-Star units that got downgraded?
            return 6 + random.randint(1, 4)
        else:
            return 10

    def downgrade_rank(self):
        raise NotImplementedError()  # first add 0-Star Stats to base_stats
        if self.rank > 0:
            self.rank -= 1
            self.max_health = self.base_stats["health"][self.rank]
            self.ad = self.base_stats["ad"][self.rank]

    def get_enemies_in_range(self, fight):
        current_cell = fight.map.get_cell_from_id(self.pos)
        enemy_champs_alive = fight.enemy_champs_alive(self)
        cell_ids_in_range = [cell.id for cell in fight.map.get_all_cells_in_range(current_cell, self.range)]
        return [enemy for enemy in enemy_champs_alive if enemy.pos in cell_ids_in_range]

    def special_ability(self, fight):
        # nearby enemies get Mega Crit
        effected_area = fight.map.get_cell_from_id(self.pos).neighbors
        fight.events.append(DummyEvent(1000, (36, 36, 36), effected_area))
        for n_cell in effected_area:
            for enemy in [champ
                          for champ in fight.champs_enemy_team(self)
                          if champ.alive]:
                if enemy.pos == n_cell.id:
                    enemy.get_magic_damage(self.aa_damage(crit=True) * 2, fight.map)

    @property
    def crit_multiplier(self):
        return 1 + self.base_crit_bonus  # + additional bonus with items, ...

    def aa_damage(self, crit=False):
        if crit or random.random() <= self.crit_chance:
            return self.ad * self.crit_multiplier
        else:
            return self.ad

    def get_physical_damage(self, incoming_damage, map_):
        real_damage = incoming_damage * (1 - (self.armor / 100))
        self.current_health -= real_damage
        self.damage_events.append(DummyDamage(real_damage, self.position(map_), "physical"))
        self.mana += self.mana_on_aa
        self.check_alive(map_)

    def get_magic_damage(self, incoming_damage, map_):
        real_damage = incoming_damage * (1 - (self.mr / 100))
        self.current_health -= real_damage
        self.damage_events.append(DummyDamage(real_damage, self.position(map_), "magic"))
        self.mana += self.mana_on_aa
        self.check_alive(map_)

    def check_alive(self, map_):
        if self.current_health <= 0:
            self.kill(map_)

    def kill(self, map_):
        print(f"Champ died on {self.pos}")
        self.alive = False
        if self.pos is not None:
            map_.get_cell_from_id(self.pos).taken = False
        # if self.next_pos is not None:
        #     map_.get_cell_from_id(self.next_pos).taken = False
        if self.target_pos is not None:
            map_.get_cell_from_id(self.target_pos).taken = False

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
        goal_locations = map_.get_cell_from_id(enemy.pos).free_neighbors
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
