import random

from fight_sim.fight_interface import create_team, run_fight


def possible_positions(height=3, length=7):
    positions = []
    for i in range(length):
        for k in range(height):
            positions.append((i, k))
    return positions


def one_champ_test(name, rank, n, items):
    team = [[name, pos, rank, items] for pos in random.sample(possible_positions(), n)]
    teams = {
        "team_bot": create_team(team),
        "team_top": create_team(team),
    }

    team1, team2 = run_fight(**teams)
    print(team1, team2)


def specific_team_test(team_bot, team_top):
    run_fight(team_top=team_top, team_bot=team_bot)


one_champ_test("Pyke", 1, 1, [])


