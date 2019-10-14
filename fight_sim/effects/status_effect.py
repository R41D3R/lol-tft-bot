import pygame


class StatusEffect:
    def __init__(self, map_, duration, name, effects=None):
        if effects is None:
            self.effects = []
        else:
            self.effects = effects
        self.duration = duration * 1000
        self.created = pygame.time.get_ticks()
        self.name = name
        self.map = map_

    def is_active(self, time):
        if time - self.created > self.duration:
            return False
        else:
            return True

    def has(self, effect):
        if effect in self.effects:
            return True
        else:
            return False


class Dot(StatusEffect):
    def __init__(self, target, fight, duration, name, user, effects, source=None, interval=None, dmg_type=None, damage=False):
        super().__init__(fight.map, duration, name, effects=effects)
        self.target = target
        self.fight = fight
        self.user = user
        self.source = source
        self.interval = int(1000 * interval)
        self.damage = damage
        self.dmg_type = dmg_type

        self.last_proc = None

    def proc(self):
        if self.damage:
            if self.last_proc is None or self.fight.now - self.last_proc >= self.interval:
                self.target.get_damage(self.dmg_type, self.target.max_health * 0.02, self.fight, origin="spell", originator=self.user, source=self.source)
                self.last_proc = self.fight.now


class Channelling(StatusEffect):
    def __init__(self, fight, duration, name, interruptable):
        super().__init__(fight.map, duration, name, effects=["channeling"])
        self.interruptable = interruptable





