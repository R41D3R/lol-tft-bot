import pygame
import random
from fight import Fight, DummyChamp
from testing import *  # only for test
import copy

# realpython
# https://realpython.com/pygame-a-primer/

# ----- Shortcuts ------
# End the Game = K_ESCAPE
# Reset the game to start = K_r
# Pause, Resume the Game = K_SPACE

from pygame.locals import (
    K_SPACE,
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

possible_positions = [(x, y) for x in range(7) for y in range(3)]  # rows 0..2, cols 0..6
bottom_team = [DummyChamp(pos, "Champ " + str(i)) for i, pos in enumerate(random.sample(possible_positions, 3))]
top_team = [DummyChamp(pos, "Champ " + str(i+3)) for i, pos in enumerate(random.sample(possible_positions, 3))]

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
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                pause = not pause
            elif event.key == K_r:
                bot_new_copy = copy.deepcopy(bottom_team)
                top_new_copy = copy.deepcopy(top_team)
                fight = Fight(team_bot=bot_new_copy, team_top=top_new_copy)
                fight.place_champs()

    # pressed_keys_ = pygame.key.get_pressed()
    screen.fill(BG_COLOR)

    if not fight.game_over and not pause:
        fight.make_fight_step()

    fight.render(screen)

    pygame.display.flip()
    clock.tick(30)


pygame.quit()
