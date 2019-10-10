class Champion:
    def __init__(self, name, pos):
        self.name = name  # onehotencoding
        self.rank = 1
        self.items = {0: 0, 1: 0, 2: 0}
        self.pos = pos  # onehot
        self.class_ = []
        self.origin = []

        # other attributes
        # like health, mana, ...
        # costs, tier

    def upgrade_rank(self):
        self.rank += 1

    @property
    def get_item_slots(self):
        return [self.items[i] for i in range(3)]

