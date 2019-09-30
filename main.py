import copy

import pygame

from fight import Fight
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, get_team

# @todo: replace print functions with logger

# realpython
# https://realpython.com/pygame-a-primer/

# ----- Shortcuts ------
# End the Game = K_ESCAPE
# Reset the game to start = K_r
# Pause, Resume the Game = K_SPACE
# New fight = K_n


from pygame.locals import (
    K_SPACE,
    K_n,
    K_r,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

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
