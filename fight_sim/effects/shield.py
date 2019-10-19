class Shield:
    def __init__(self, champ, fight, created, amount, duration=None):
        self.created = created
        if duration is None:
            self.duration = duration
        else:
            self.duration = int(duration * 1000)
        self.fight = fight
        self.amount = amount
        self.champ = champ

    def get_duration(self):
        if self.duration is None:
            return 99999999999
        else:
            return self.fight.now - self.created

    def is_active(self):
        if self.duration is None:
            if self.amount > 0:
                return True
        elif self.fight.now - self.created <= self.duration and self.amount > 0:
            return True
        return False

    def damage(self, damage):
        self.amount -= damage
        overhead = self.amount
        if overhead < 0:
            self.amount = 0
        return overhead
