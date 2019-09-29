import random
# from testing import *  # only for test
import copy

import pygame

from fight import Fight
from helper.dummy import DummyChamp
from helper.champs import champs_dict

# @todo: replace print functions with logger

# realpython
# https://realpython.com/pygame-a-primer/

# ----- Shortcuts ------
# End the Game = K_ESCAPE
# Reset the game to start = K_r
# Pause, Resume the Game = K_SPACE
# New fight = K_n


possible_positions = [(x, y) for x in range(7) for y in range(3)]  # rows 0..2, cols 0..6


def get_team():
    k = 3
    k_picks = random.sample(list(champs_dict.items()), k)
    k_pos = random.sample(possible_positions, k)
    k_ranks = [random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0] for i in range(k)]
    return [DummyChamp(pos, item, rank) for pos, item, rank in zip(k_pos, k_picks, k_ranks)]


from pygame.locals import (
    K_SPACE,
    K_n,
    K_r,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bottom_team = get_team()
top_team = get_team()

bot_t_copy = copy.deepcopy(bottom_team)
top_t_copy = copy.deepcopy(top_team)

fight = Fight(team_bot=bot_t_copy, team_top=top_t_copy)
fight.place_champs()


clock = pygame.time.Clock()
running = True
pause = False

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # quit
                running = False
            elif event.key == K_SPACE:  # pause and resume the game
                pause = not pause
            elif event.key == K_r:  # reset fight
                bot_new_copy = copy.deepcopy(bottom_team)
                top_new_copy = copy.deepcopy(top_team)
                fight = Fight(team_bot=bot_new_copy, team_top=top_new_copy)
                fight.place_champs()
            elif event.key == K_n:  # create new fight
                bottom_team = get_team()
                top_team = get_team()
                bot_t_copy = copy.deepcopy(bottom_team)
                top_t_copy = copy.deepcopy(top_team)
                fight = Fight(team_bot=bot_t_copy, team_top=top_t_copy)
                fight.place_champs()

    # pressed_keys_ = pygame.key.get_pressed()
    screen.fill(BG_COLOR)

    if not fight.game_over and not pause:
        fight.make_fight_step()

    fight.render(screen)

    pygame.display.flip()
    clock.tick(30)


pygame.quit()
