import pygame
import random
from fight import Fight, DummyChamp
from testing import *  # only for test

# realpython
# https://realpython.com/pygame-a-primer/

from pygame.locals import (
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

fight = Fight(team_bot=bottom_team, team_top=top_team)
fight.place_champs()


clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # pressed_keys_ = pygame.key.get_pressed()

    if fight.game_over:
        break

    screen.fill(BG_COLOR)
    fight.make_fight_step()
    fight.render(screen)

    pygame.display.flip()
    clock.tick(30)

# show result
team_top, team_bot = fight.result
if len(team_top) > len(team_bot):
    print(f"Team TOP won with: {len(team_top)} champs alive")
else:
    print(f"Team BOT won with: {len(team_bot)} champs alive")

pygame.quit()
