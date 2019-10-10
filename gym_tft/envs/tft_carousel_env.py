import gym
from gym import error, spaces, utils
from gym.utils import seeding


class TFTCarouselEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, tournament):
        self.tournament = tournament
        self.action_space = spaces.Discrete()
        self.agents = tournament.agents

        self.state = self._random_carousel

    def step(self, action):
        # update state
        # update agent
        pass

    def reset(self):
        pass

    @property
    def _random_carousel(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass