import pygame
from abc import ABC, abstractmethod

from helper.status_effect import StatusEffect


# @todo: relative and absolute aoe
# @body: this class needs better modeling to work effectively
class Aoe(ABC):
    def __init__(self, created, duration, delay, effected_area, user, fight, interval, user_needed=False):
        self.fight = fight
        self.fight.aoe.append(self)

        self.created = created
        self.duration = int(duration * 1000)
        self.delay = int(delay * 1000)
        self.last_proc = None
        self.proc_interval = int(interval * 1000)

        self.activated = False

        self.effected_area = effected_area

        self.user = user
        self.user_needed = user_needed

    @property
    def interval(self):
        return self.fight.now - self.created

    @property
    def active(self):
        if not self.activated or self.interval + self.delay < self.duration or (self.user_needed and self.user.alive):
            return True
        else:
            return False

    @abstractmethod
    def proc(self):
        pass

    def all_enemies_in_area(self):
        enemies = []
        area_ids = [cell.id for cell in self.effected_area]
        for enemy in self.fight.enemy_champs_alive(self.user):
            if enemy.pos in area_ids:
                enemies.append(enemy)
        return enemies
