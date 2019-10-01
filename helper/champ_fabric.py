import random

import pygame

from helper.dummy import DummyChamp
from helper.dummy_vision_event import DummyEvent
from helper.status_effect import StatusEffect
from helper.aoe import Aoe
from config import logger
from helper.champs import champs_dict


class ChampionFabric:
    def __init__(self):
        self.possible_positions = [(x, y) for x in range(7) for y in range(3)]  # rows 0..2, cols 0..6

    def get_team(self):
        logger.info("Team gets initialized.")
        k = 3
        k_picks = random.sample(list(champs_dict.items()), k)
        k_pos = random.sample(self.possible_positions, k)
        k_ranks = [random.choices([1, 2, 3], weights=[0.85, 0.1, 0.05])[0] for i in range(k)]
        return [self.get_champ(pos, item, rank) for pos, item, rank in zip(k_pos, k_picks, k_ranks)]

    @staticmethod
    def get_champ(pos, champ_item, rank, items=None):
        if champ_item[0] == "Khazix":
            return Khazix(pos, champ_item, rank, items=items)
        if champ_item[0] == "Garen":
            return Garen(pos, champ_item, rank, items=items)
        if champ_item[0] == "Lucian":
            return Lucian(pos, champ_item, rank, items=items)
        if champ_item[0] == "Fiora":
            return Fiora(pos, champ_item, rank, items=items)
        # if champ_item[0] == "Shen":
        #     return Shen(pos, champ_item, rank, items=items)
        if champ_item[0] == "Camille":
            return Camille(pos, champ_item, rank, items=items)
        if champ_item[0] == "Jayce":
            return Jayce(pos, champ_item, rank, items=items)


# @todo: What should champ do if no enemy is in range for sa
# @body: champs like kha, jayce, camille need a champ in range, currently wasting sa


class Khazix(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [150, 250, 350]
        self.sa_damage_alone = [400, 600, 800]

    def special_ability(self, fight, in_range, visible, alive, time):
        if len(in_range) > 0:
            target = random.choice(in_range)
            effected_area = [fight.map.get_cell_from_id(target.pos)]
            if len(target.get_allies_around(fight)) == 0:
                target.get_damage("magic", self.sa_damage_alone[self.rank - 1], fight.map)
            else:
                target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map)
            fight.events.append(DummyEvent(1000, (36, 36, 36), effected_area))


class Garen(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [40, 65, 90]
        self.interval = 500
        self.last_proc = None

    def special_ability(self, fight, in_range, visible, alive, time):
        effected_area = fight.map.get_cell_from_id(self.pos).neighbors

        if self.has_effect_with_name("Judgement"):
            # self.last_proc = time
            for enemy in in_range:
                enemy.get_damage("magic", self.sa_damage[self.rank - 1], fight.map)
            fight.events.append(DummyEvent(50, (36, 36, 36), effected_area))
        else:
            self.channel(fight, 4, "Judgement", 0.5, False)
            self.status_effects.append(StatusEffect(fight.map, 4, "Judgement", effects=["immune_magic"]))


class Lucian(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [100, 225, 350]

    # @todo: jump to furthest point from all enemies
    # @body: currently jumps to max(distance <= 2) from current position relative to the current target
    def special_ability(self, fight, in_range, visible, alive, time):
        target = self.get_target(self.get_enemies_in_range(fight, self.range + 2))
        if target:
            target_cell = fight.map.get_cell_from_id(target.pos)
            # find furthest spot from enemy where enemy is in self.enemies_in_range
            self_cell = fight.map.get_cell_from_id(self.pos)
            # @todo: should be straight distance from lucian_cell
            # @body: range is currently absolute cell_distance
            range_around_target = [cell for cell in fight.map.get_all_cells_in_range(target_cell, self.range) if not cell.taken]
            ranges = [(fight.map.distance(self_cell, goal), goal) for goal in range_around_target if fight.map.distance(self_cell, goal) <= 2]
            best_jump = None
            best_range = 0
            for item in ranges:
                if item[0] >= best_range:
                    best_jump = item[1]
                    best_range = item[0]
            self.move_to(best_jump, fight)
            self.autoattack(time, fight, in_range)
            target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map)


class Fiora(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [100, 250, 400]
        self.sa_used = None

    def special_ability(self, fight, in_range, visible, alive, time):
        channel_duration = 1.5
        if self.sa_used is None:
            self.immune(1.5, fight)
            self.channel(fight, 1.5, "Riposte")
            self.sa_used = time
        elif time - self.sa_used >= channel_duration * 1000:
            target = self.get_target(in_range)
            if target:
                target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map)
                stun = StatusEffect(fight.map, 1.5, "Stun", effects=["stun"])
                target.get_spell_effect(stun, fight)
                fight.events.append(DummyEvent(1000, (36, 36, 36), [fight.map.get_cell_from_id(target.pos)]))

            self.sa_used = None
        else:
            pass


class Shen(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_duration = [3, 4, 5]

    def special_ability(self, fight, in_range, visible, alive, time):
        # creates zone around self.pos
        effect = StatusEffect(fight.map, 0, "Spirit's Refuge", effects=["aa_dodge"])
        aoe = Aoe(time, self.sa_duration[self.rank - 1], 0, "around_user", "allie_team", "zone", self, fight, 0, status_effetct=effect)
        fight.aoe.append(aoe)


class Camille(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_duration = [4, 5, 6]
        self.sa_damage = [200, 325, 450]

    def special_ability(self, fight, in_range, visible, alive, time):
        # big damage on enemy
        # roots enemy + status_effect(allies prioritize target)
        target = self.get_target(in_range)
        if target:
            target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map)
            fight.events.append(DummyEvent(1000, (36, 36, 36), fight.map.get_cell_from_id(target.pos)))
            status_effect = StatusEffect(fight.map, self.sa_duration[self.rank - 1], "The Hextech Ultimatum", effects=["root", "priority"])
            target.get_spell_effect(status_effect, fight)


class Jayce(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_stun_duration = [2.5, 4.25, 6]
        self.sa_damage = [200, 350, 500]
        self.as_hit_duration = [3, 5, 7]
        self.as_increase = [1, 3, 5]
        self.rank_on_use = None
        self.aa_counter_after_sa = 0

    def special_ability(self, fight, in_range, visible, alive, time):
        self.rank_on_use = self.rank
        target = self.get_target(in_range)
        if target:
            target.get_damage("magic", self.sa_damage[self.rank_on_use - 1], fight.map, origin="spell", originator=self)
            fight.events.append(DummyEvent(self.sa_stun_duration[self.rank_on_use - 1] * 1000, (36, 36, 36), fight.map.get_cell_from_id(target.pos)))
            target.get_spell_effect(StatusEffect(fight.map, self.sa_stun_duration[self.rank_on_use - 1], "Mercury Cannon", effects=["stun"]), fight)

        # buffs
        buff_duration = 60
        range_effect = StatusEffect(fight.map, buff_duration, "Transform Mercury Cannon", effects=["range_buff_+1"])
        as_buff = StatusEffect(fight.map, buff_duration, "Transform Mercury Cannon", effects=["jayce_as_boost"])
        self.mana_lock(fight.map, buff_duration)
        for _ in range(3):
            self.status_effects.append(range_effect)
        self.status_effects.append(as_buff)

    def autoattack(self, time, fight, enemies_in_range):
        super().autoattack(time, fight, enemies_in_range)
        if self.aa_counter_after_sa >= self.as_hit_duration[self.rank_on_use - 1]:
            effects = self.get_all_effects_with("jayce_as_boost")
            for effect in effects:
                self.status_effects.remove(effect)

    @property
    def aa_cc(self):
        if self.rank_on_use:
            rank = self.rank_on_use
        else:
            rank = self.rank
        super_aa_cc = 1 / super().aa_cc / 1000
        return int(1 / (super_aa_cc + self.as_increase[rank - 1] * len(self.get_all_effects_with("jayce_as_boost"))) * 1000)


class Swain(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_duration = 6
        self.sa_damage = [40, 80, 120]
        self.interval = 0.5 * 1000
        self.sa_healing = [30, 60, 90]
        self.sa_end_damage = [300, 600, 900]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass






