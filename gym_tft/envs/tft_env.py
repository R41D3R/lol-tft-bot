import gym
from gym import error, spaces, utils
from gym.utils import seeding


class TFTEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, tournament):
        self.tournament = tournament
        self.agents = self.tournament.agents

        self.action_space = spaces.Discrete(7)
        # --- Actions ---
        # Reroll
        # Level Up
        # Move Champ
        # Buy Champ
        # Sell Champ
        # Give Item
        # Ready

    def step(self, action):
        for agent in self.agents:
            # do actions until ready
            pass

    def reset(self):
        pass

    def _get_obs(self, agent):
        # observation for a particular agent
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass
