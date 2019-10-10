class Agent:
    def __init__(self):
        self.state = AgentState()

    def action(self):
        # based on round
        # if carousel -> other nn
        pass


class AgentState:
    def __init__(self):
        self.health = 100
        self.gold = 0
        self.exp = 0
        self.champs = 0
        self.last_observations = []
        self.win_streak = 0
        self.lose_streak = 0
        self.items = []
        self.buys = []
        self.damage_last_round = 0
        # --- from tournament ---
        # other agents champs + items + gold pots + level + health + damage taken
        # championpool from last state + update from own player moves
        #

    @property
    def _get_max_champs(self):
        # based on level and champ items
        # force of nature
        pass

    @property
    def _get_level(self):
        # calculate level based on exp
        pass
