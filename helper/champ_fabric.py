import random

from helper.dummy import DummyChamp
from helper.dummy_vision_event import DummyEvent


class ChampionFabric:
    def __init__(self):
        pass

    @staticmethod
    def get_champ(rank, pos, champ_item, items=None):
        if champ_item[0] == "Khazix":
            return Khazix(pos, champ_item, rank, items=items)
        if champ_item[0] == "Garen":
            return Garen(pos, champ_item, rank, items=items)


class Khazix(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [150, 250, 350]
        self.sa_damage_alone = [400, 600, 800]

    def special_ability(self, fight, in_range, visible, alive, time):
        target = random.choice(in_range)
        effected_area = fight.map.get_cell_from_id(target.pos)
        if len(target.get_alllies_around(fight)) == 0:
            target.get_damage("magic", self.sa_damage_alone[self.rank - 1], fight.map)
        else:
            target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map)
        fight.events.append(DummyEvent(1000, (36, 36, 36), effected_area))


class Garen(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [40, 65, 90]

    def special_ability(self, fight, in_range, visible, alive, time):
        if self.has_effect_with_name("Judgement"):
            for enemy in in_range:
                enemy.get_damage("magic", self.sa_damage[self.rank - 1], fight.map)
                effected_area = fight.map.get_cell_from_id(self.pos)
                fight.events.append(DummyEvent(1000, (36, 36, 36), effected_area))
            else:
                self.status_effects.append(self.channelling(fight, 4, "Judgement", 0.5))


class Lucian(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [100, 225, 350]

    def special_ability(self, fight, in_range, visible, alive, time):
        target = self.get_target(in_range)
        target_cell = fight.map.get_cell_from_id(target.pos)
        # find furthest spot from enemy where enemy is in self.enemies_in_range
        self_cell = fight.map.get_cell_from_id(self.pos)
        range_around_target = [cell for cell in fight.map.get_all_cells_in_range(target_cell, self.range) if not cell.taken]
        jump = max([goal for goal in range_around_target if fight.map.distance(self_cell, goal) <= 2])
        self.move_to(jump)
        self.autoattack(time, fight, in_range)
        target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map)





