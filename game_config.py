import random

from helper.dummy import DummyChamp
from helper.champs import champs_dict
from config import logger

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (255, 255, 255)

possible_positions = [(x, y) for x in range(7) for y in range(3)]  # rows 0..2, cols 0..6


def get_team():
    logger.info("Team gets initialized.")
    k = 3
    k_picks = random.sample(list(champs_dict.items()), k)
    k_pos = random.sample(possible_positions, k)
    k_ranks = [random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0] for i in range(k)]
    return [DummyChamp(pos, item, rank) for pos, item, rank in zip(k_pos, k_picks, k_ranks)]