import random

import pygame

from helper.dummy import DummyChamp
from helper.dummy_vision_event import DummyEvent
from helper.status_effect import StatusEffect
from helper.aoe import Aoe
from config import logger
from helper.champs import champs_dict
from data.items_base_stats import Item, all_items


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
    def get_items():
        items = []
        n_items = random.choices([0, 1, 2, 3], weights=[0.5, 0.3, 0.1, 0.1])[0]
        for i in range(n_items):
            random_item = random.choice(list(all_items.items()))
            items.append(Item(random_item[1]["attribute"], random_item[1]["name"]))
        return items

    def get_champ(self, pos, champ_item, rank, items=None):
        if items is None:
            items = self.get_items()
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


class Aatrox(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [700, 1260, 2520]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Cleaves the area in front of him,
        # dealing 300 / 600 / 900 magic damage to all enemies within.


class Brand(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [250, 450, 650]
        self.sa_bounces = [4, 6, 20]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Launches a bouncing fireball at an enemy.
        # The fireball bounces to nearby enemies
        # up to 4 / 6 / 20 times, dealing 250 / 450 / 650 magic damage
        # with each bounce.


class Elise(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_spiderlings = [1, 2, 4]
        self.spider_lifesteal = [0.6, 0.9, 1.2]
        self.spider_health = 500
        self.spider_ad = 60
        self.spider_atk_speed = 0.7
        # create spider npc
        # spider gets demon bonus

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Summons 1 / 2 / 4 Spiderlings and transforms
        # to her Spider Form, becoming a Melee role melee attacker for 60 seconds.
        # While in Spider Form, gains 60 / 90 / 120% life steal.
        # Each Spiderling has 500 health, 60 attack damage
        # and 0.7 attack speed, and can gain the Demon bonus.


class Evelyn(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [200, 300, 400]
        self.sa_damage_below_50 = [600, 1200, 2000]
        self.sa_back_hexes = 3
        # to 3 closest enemies

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Roots the 3 closest enemies for 0.35 seconds,
        # after which deals 200 / 300 / 400 magic damage to
        # the 3 closest enemies and blinks back 3 hexes.
        # Damage is increased to 600 / 1200 / 2000 against enemies below 50% health


class Morgana(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_delay = int(0.5 * 1000)
        self.sa_range = 3
        self.sa_damage = [175, 300, 425]
        self.sa_second_delay = 3
        self.sa_stun_duration = [2, 4, 6]  # damage again

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: After a 0.5-second delay, fires chains to
        # nearby enemies up to 3 hexes away, dealing 175 / 300 / 425 magic damage.
        # After 3 seconds, all chained enemies still within her
        # range are Stun icon stunned for 2 / 4 / 6 seconds and take
        # the same magic damage.


class Varus(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_channeltime = int(1.5 * 1000)
        self.sa_range = 8
        self.sa_damage = [300, 550, 800]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: After channeling for 1.5 seconds, fires a piercing
        # arrow up to 8 hexes away, dealing 300 / 550 / 800 magic damage
        # to all enemies in its path.


class AurelioSol(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_delay = int(0.35 * 1000)
        self.sa_damage = [250, 500, 750]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: After a 0.35-second delay, breathes fire in a line,
        # dealing 250 / 500 / 750 magic damage to all enemies in the area.


class Pantheon(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_stun_duration = int(2 * 1000)
        self.sa_percent_damage = [0.1, 0.2, 0.3]
        # grievous wounds 2% true damage for 10 sec.

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Leaps in the air, becoming untargetable, and crashes down
        # towards the farthest enemy, Stun icon stunning them for 2 seconds.
        # As he lands, deals 10 / 20 / 30% of their maximum health magic
        # damage and applies a burn for 10 seconds, dealing 2% of target's
        # maximum health true damage each second and applying Grievous Wounds
        # for the duration, reducing healing on the target.


class Shyvana(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_duration = int(60 * 1000)
        self.sa_dragon_ad_increase = [100, 150, 200]
        self.sa_dot_duration = int()

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Dashes away from her current target and transforms
        # to her Dragon Form, becoming a Ranged role ranged attacker for 60 seconds.
        # While in Dragon Form, gains 100 / 150 / 200 attack damage
        # and basic attacks apply a burn on enemies hit for 3 seconds,
        # dealing a total of 200 / 300 / 400 bonus magic damage.



