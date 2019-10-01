import pygame


from helper.status_effect import StatusEffect


# @todo: relative and absolute aoe
# @body: this class needs better modeling to work effectively
class Aoe:
    def __init__(self, created, duration, delay, effected_area, team, effects, user, fight, interval, static_area=None, amount=0, type_=None, status_effetct=None):
        self.created = created
        self.duration = duration * 1000
        self.effected_area = effected_area
        self.team = team
        self.delay = delay * 1000
        self.user = user
        self.static_area = static_area
        self.effects = effects
        self.last_proc = None
        self.proc_interval = interval * 1000
        self.amount = amount
        self.type = type_
        self.status_effect = status_effetct

        if self.delay <= 0:
            self.activate(created, fight)

    @property
    def area(self):
        if self.effected_area == "around_user":
            if self.user.is_alive:
                return self.user.neighbors
            else:
                return []
        elif self.effected_area == "static_area":
            return self.static_area
        elif self.effected_area == "static_around_user":
            raise NotImplementedError()
        else:
            raise NotImplementedError()

    def effect(self):
        pass

    def activate(self, time, fight):
        if self.effected_area == "around_user":
            if time - self.created >= self.delay and self.last_proc is None or time - self.last_proc >= self.proc_interval:
                self.last_proc = time
                if "heal" in self.effects:
                    champs_in_area = fight.champs_in_area(self.area, fight.champs_allie_team(self))
                    for champ in champs_in_area:
                        champ.heal(self.amount)
                if "damage" in self.effects:
                    champs_in_area = fight.champs_in_area(self.area, fight.champs_enemy_team(self))
                    for champ in champs_in_area:
                        champ.get_damage(self.type, self.amount, fight.map)
                if "zone" in self.effects:
                    if self.team == "enemy_team":
                        champs_in_area = fight.champs_in_area(self.area, fight.champs_enemy_team(self))
                    else:
                        champs_in_area = fight.champs_in_area(self.area, fight.champs_allie_team(self))
                    for champ in champs_in_area:
                        champ.get_spell_effect(self.status_effect, fight.map)
            if time - self.created >= self.duration:
                fight.aoe.remove(self)
            else:
                pass
