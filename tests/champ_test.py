import random

import pygame

from fight_sim.fight import Fight
from fight_sim.champ_fabric import ChampionFabric

# realpython
# https://realpython.com/pygame-a-primer/

# ----- Shortcuts ------
# End the Game = K_ESCAPE
# Reset the game to start = K_r
# Pause, Resume the Game = K_SPACE
# New fight = K_n

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
BG_COLOR = (255, 255, 255)


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
clock = pygame.time.Clock()
running = True
pause = False

champ_fabric = ChampionFabric()
fight = Fight(champ_fabric)

possible_positions = [(x, y) for x in range(7) for y in range(3)]
n_champs = 1
champs = [["Zed", pos, 1, []] for pos in random.sample(possible_positions, n_champs)]
print(champs)
fight.new_fight(champs_bot=champs, champs_top=champs)

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
                fight.new_fight(champs_bot=champs, champs_top=champs)
            elif event.key == K_n:  # create new fight
                fight.new_fight(champs_bot=champs, champs_top=champs)

    # pressed_keys_ = pygame.key.get_pressed()
    screen.fill(BG_COLOR)

    if not fight.game_over and not pause:
        fight.make_fight_step()

    fight.render(screen)

    pygame.display.flip()
    clock.tick(30)


pygame.quit()

