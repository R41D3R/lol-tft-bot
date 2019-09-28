from math import cos, pi, sin
import pygame
from board.map import Map


from pygame.locals import (
    K_a,
    K_w,
    K_e,
    K_d,
    K_x,
    K_y,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

MAP = Map(cell_radius=50, n_rows=6, n_cols=7, color=(0, 150, 0), space=3)
player = (0, 0)
for _ in MAP.cell_map:
    for c in _:
        if c.id == player:
            c.taken = True


def draw_regular_polygon(surface, color, vertex_count, radius, position):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * cos(2 * pi * i / n + (1/6 * pi)), y + r * sin(2 * pi * i / n + (1/6 * pi)))
        for i in range(n)
    ])


def draw_hexagon(surface, pos):
    draw_regular_polygon(surface, (0, 250, 0), 6, 50, pos)
    draw_regular_polygon(surface, (0, 0, 100), 6, 40, pos)


def get_cell_from_id(id,):
    for _ in MAP.cell_map:
        for c_ in _:
            if c_.id == id:
                return c_
    return None


def update_player(current_player, pressed_keys):
    new_player = None
    if pressed_keys[K_a]:
        new_player = (current_player[0] - 2, current_player[1])
    if pressed_keys[K_w]:
        new_player = (current_player[0] - 1, current_player[1] - 1)
    if pressed_keys[K_e]:
        new_player = (current_player[0] + 1, current_player[1] - 1)
    if pressed_keys[K_d]:
        new_player = (current_player[0] + 2, current_player[1])
    if pressed_keys[K_x]:
        new_player = (current_player[0] + 1, current_player[1] + 1)
    if pressed_keys[K_y]:
        new_player = (current_player[0] - 1, current_player[1] + 1)

    cell = get_cell_from_id(new_player)
    if cell in get_cell_from_id(current_player).neighbors:
        cell.taken = True
        get_cell_from_id(player).taken = False
        print(f"Move from {current_player} to {new_player}")
        current_player = new_player
    return current_player
