import pygame


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
        self.champ.shields.append(self)

    def get_duration(self, time):
        if self.duration is None:
            return 99999999999
        else:
            return time - self.created

    def is_active(self, time):
        if self.duration is None:
            if self.amount > 0:
                return True
        elif self.created - time <= self.duration and self.amount > 0:
            return True
        self.champ.shields.remove(self)
        return False

    def damage(self, damage):
        self.amount -= damage
        overhead = self.amount
        if overhead < 0:
            self.amount = 0
        return overhead


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
        self.negative = False
        if "stun" in self.effects \
                or "gwound" in self.effects \
                or "mana-lock" in self.effects \
                or "root" in self.effects \
                or "airborne" in self.effects \
                or "shrink" in self.effects \
                or "channeling" in self.effects \
                or "banish" in self.effects:
            self.negative = True

    def is_active(self, time):
        if time - self.created >= self.duration:
            return False
        else:
            return True

    def has(self, effect):
        if effect in self.effects:
            return True
        else:
            return False


class GWounds(StatusEffect):
    def __init__(self, champ, map_, duration, name, originator=None, damage=False):
        super().__init__(map_, duration, name, effects=["gwound"])
        self.damage = damage
        self.last_proc = None
        self.target = champ
        self.damage_interval = 1000
        self.originator = originator

    def proc(self):
        if self.damage:
            now = pygame.time.get_ticks()
            if self.last_proc is None or now - self.last_proc >= self.damage_interval:
                self.target.get_damage("true", self.target.max_health * 0.02, self.map, origin="spell", originator=self.originator)
                self.last_proc = now


class Channelling(StatusEffect):
    def __init__(self, champ, fight, duration, name, proc_interval, interruptable):
        super().__init__(fight.map, duration, name, effects=["channeling"])
        if proc_interval is None:
            self.proc_interval = 0
        else:
            self.proc_interval = int(proc_interval * 1000)
        self.last_proc = None
        self.champ = champ
        self.interruptable = interruptable

    def does_proc(self, time):
        if self.last_proc is None or time - self.last_proc >= self.proc_interval:
            self.last_proc = time
            return True
        else:
            return False

    def completed(self, time):
        if time - self.created >= self.duration:
            return True
        else:
            return False





