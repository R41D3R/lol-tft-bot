class Tournament:
    def __init__(self):
        self.round_counter = 0
        self.agents = []
        self.champ_pool = {}

    def step(self):
        # make fight based on round
        # update agents states
        pass

    def buy_champ(self, champ, agent):
        # update buys
        # update agent
        pass

    def level_up(self, agent):
        # update agent: gold, exp
        pass

    def sell_champ(self, champ, agent):
        # update pool
        # update agent
        pass

    def reroll(self, agent):
        self._get_random_buys(agent)
        # lock pool and give agent new_buys
        # update agent
        pass

    def move_champ(self, agent, champ, pos):
        pass

    def _unlock_buys(self, champs):
        pass

    def _get_random_buys(self, agent):
        self._unlock_buys(agent.buys)
        pass

    def _update_agent_state(self, agent):
        pass

    def _match_agents(self):
        # pairs of agents
        pass

    def _fight(self, agent1, agent2):
        # (optional: select random parameters for each fight)
        #
        # do fight with special parameters

        # based on round
        # return survived champs
        # (optional: do fight x times and return probability for each
        #            win and pick random survived champs for damage
        #            calculation
        pass

    def _update_fight_results(self, results):
        # damage to agent
        # get gold from, round, streak, gold pots and pirates
        # give drops
        pass

    def _damage_to_agent(self, champs, agent):
        pass

