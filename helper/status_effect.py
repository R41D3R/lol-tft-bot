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

    @property
    def is_active(self):
        now = pygame.time.get_ticks()
        if now - self.created >= self.duration:
            return False
        else:
            return True

    def has(self, effect):
        if effect in self.effects:
            return True
        else:
            return False


class GWounds(StatusEffect):
    def __init__(self, champ, map_, duration, name, damage=False):
        super().__init__(map_, duration, name, effects=["gwound"])
        self.damage = damage
        self.last_proc = None
        self.target = champ
        self.damage_interval = 1000

    def proc(self):
        if self.damage:
            now = pygame.time.get_ticks()
            if self.last_proc is None or now - self.last_proc >= self.damage_interval:
                self.target.get_damage("true", self.target.max_health * 0.02, self.map)
                self.last_proc = now


class Channelling(StatusEffect):
    def __init__(self, champ, fight, duration, name, proc_interval):
        super().__init__(fight.map, duration, name, effects=["channeling"])
        self.proc_interval = proc_interval * 1000
        self.last_proc = None
        self.champ = champ

    def does_proc(self, time):
        if self.last_proc is None or time - self.last_proc >= self.proc_interval:
            return True
        else:
            return False



