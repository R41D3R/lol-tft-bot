import copy

import pygame

from fight_sim.fight import Fight
from fight_sim.champ_fabric import ChampionFabric

# ----- Shortcuts ------
# End the Game = K_ESCAPE
# Reset the game to start = K_r
# Pause, Resume the Game = K_SPACE
# New fight = K_n


def create_team(team_info_list, random_team=False):
    champ_fabric = ChampionFabric()
    if random_team:
        return champ_fabric.get_team()
    return champ_fabric.get_real_team(team_info_list)


def run_fight(team_bot=None, team_top=None, hypeparameters_dict=None, visual=True, fast=False):
    # implement customizable hyperparameters for fight simulation

    teams = {
        "team_bot": team_bot,
        "team_top": team_top,
    }

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

    if not fast:
        clock = pygame.time.Clock()
    else:
        clock = 0
    running = True
    pause = False

    fight = _get_fight(**teams)

    while running:

        if visual:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # quit
                        running = False
                    elif event.key == K_SPACE:  # pause and resume the game
                        pause = not pause
                    elif event.key == K_r:  # reset fight
                        fight = _get_fight(**teams)

        if not fight.game_over and not pause:
            fight.make_fight_step()
        else:
            return team_top, team_bot

        # pressed_keys_ = pygame.key.get_pressed()
        if visual:
            screen.fill(BG_COLOR)
            fight.render(screen)
            pygame.display.flip()
            clock.tick(30)

    pygame.quit()


def _get_fight(team_bot, team_top):
    return Fight(team_bot=team_bot, team_top=team_top)
