from abc import ABC, abstractmethod

from fight.effects.status_effect import StatusEffect


# @todo: relative and absolute aoe
# @body: this class needs better modeling to work effectively
class Aoe(ABC):
    def __init__(self, fight, user, name, duration=0, delay=0, effected_area=None, interval=0, user_needed=False, interruptable=False):
        self.name = name
        self.fight = fight
        self.fight.aoe.append(self)

        self.created = fight.now
        self.duration = int(duration * 1000)
        self.delay = int(delay * 1000)
        self.last_proc = None
        self.proc_interval = int(interval * 1000)

        self.activated = False

        self.effected_area = effected_area

        self.user = user
        self.user_needed = user_needed
        self.interruptable = interruptable

    @property
    def active(self):
        if not self.activated:
            if self.user_needed and self.user.alive:
                if self.interruptable and self.user.interrupted(self.name):
                    return False
                return True
            else:
                return False
        else:
            return False

    @abstractmethod
    def proc(self):
        pass

    def _create_channel(self, duration):
        self.user.channel(self.fight, duration, self.name, self.interruptable)

    def _all_enemies_in_area(self):
        enemies = []
        area_ids = [cell.id for cell in self.effected_area]
        for enemy in self.fight.enemy_champs_alive(self.user):
            if enemy.pos in area_ids:
                enemies.append(enemy)
        return enemies


class SpinningAxes(Aoe):
    def __init__(self, created, effected_area, user, fight):
        super().__init__(created, 0, 2, effected_area, user, fight, 0, user_needed=True)
        self.old_pos = self.user.pos

    def proc(self):
        if self.user.alive:
            if self.fight.now - self.created >= self.delay:
                self._do_effect()
                self.activated = True
        else:
            self.activated = True

    def _do_effect(self):
        if self.old_pos == self.user.pos:
            buffs = self.user.get_all_effects_with("spinning_axes")
            if len(buffs) > 0:
                for buff in buffs:
                    buff.duration = self.duration * 1000


