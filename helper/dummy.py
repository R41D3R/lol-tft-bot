import pygame
import random

from helper.pathfinding_helper import PriorityQueue
from helper.dummy_vision_event import DummyEvent

dmg_color = {
    "physical": (255, 140, 0),
    "magic": (226, 121, 252),
    "true_damage": (255, 255, 255)
}


class DummyDamage:
    def __init__(self, amount, stat_pos, kind: str):
        self.color = dmg_color[kind]
        self.amount = amount
        self.create = pygame.time.get_ticks()
        self.start_pos = stat_pos
        self.font = pygame.font.SysFont("Comic Sans Ms", int(amount/10 * 5 + 20))
        self.duration = int(self.amount / 10 * 1000)

    def render(self, surface):
        state = pygame.time.get_ticks() - self.create
        text = self.font.render(str(self.amount), False, self.color)
        surface.blit(text, (self.start_pos[0],
                            int(self.start_pos[1] - (state / self.duration * 50))))

    @property
    def is_active(self):
        state = pygame.time.get_ticks() - self.create
        if state >= self.duration:
            return False
        else:
            return True


class DummyChamp:
    def __init__(self, init_pos, name):
        self.name = name
        self.alive = True
        self.health = 100
        self.ad = 5
        self.pos = init_pos
        self.next_pos = None
        self.move_progress = 0
        self.target_pos = None
        self.aa_last = pygame.time.get_ticks()
        self.aa_cc = 1000
        self.range = random.choices([1, 2, 3, 4], weights=[0.4, 0.3, 0.2, 0.1])[0]
        self.mana = 0
        self.mana_on_aa = 10
        self.armor = 10
        self.mr = 20
        self.crit_chance = 0.25
        self.crit_multiplier = 1.5

        self.damage_events = []

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

    def aa_damage(self, crit=False):
        if crit or random.random() <= self.crit_chance:
            return self.ad * self.crit_multiplier
        else:
            return self.ad

    def get_physical_damage(self, incoming_damage, map_):
        real_damage = incoming_damage * (1 - (self.armor / 100))
        self.health -= real_damage
        self.damage_events.append(DummyDamage(real_damage, self.position(map_), "physical"))
        self.mana += self.mana_on_aa
        self.check_alive(map_)

    def get_magic_damage(self, incoming_damage, map_):
        real_damage = incoming_damage * (1 - (self.mr / 100))
        self.health -= real_damage
        self.damage_events.append(DummyDamage(real_damage, self.position(map_), "magic"))
        self.mana += self.mana_on_aa
        self.check_alive(map_)

    def check_alive(self, map_):
        if self.health <= 0:
            self.kill(map_)

    def kill(self, map_):
        print(f"Champ died on {self.pos}")
        self.alive = False
        if self.pos is not None:
            map_.get_cell_from_id(self.pos).taken = False
        if self.next_pos is not None:
            map_.get_cell_from_id(self.next_pos).taken = False

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
        pygame.draw.rect(surface, (0, 130, 46), (hb_x, hb_y, int(hb_width * self.health / 100), hb_height))

        # ----- mana bar -----
        mb_width = 60
        mb_height = 10
        mb_x = player_pos[0] - (mb_width / 2)
        mb_y = hb_y + mb_height
        # mana background bar
        pygame.draw.rect(surface, (0, 0, 0), (mb_x, mb_y, mb_width, mb_height))
        # mana progress bar
        pygame.draw.rect(surface, (52, 219, 235), (mb_x, mb_y, int(mb_width * self.mana / 100), mb_height))

        # ----- name ------
        text = font.render(self.name, False, (0, 0, 0))
        surface.blit(text, (player_pos[0] - 30, player_pos[1] - 20))

        # ----- damage -----
        for dmg in self.damage_events:
            if dmg.is_active:
                dmg.render(surface)
            else:
                self.damage_events.remove(dmg)

    def position(self, map_):
        current_cell = map_.get_cell_from_id(self.pos)
        if self.next_pos:
            next_cell = map_.get_cell_from_id(self.next_pos)
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
