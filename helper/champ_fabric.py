import random

import pygame

from helper.dummy import DummyChamp
from helper.dummy_vision_event import DummyEvent
from helper.status_effect import StatusEffect
from helper.aoe import Aoe
from config import logger
from helper.champs import champs_dict
from data.items_base_stats import Item, all_items


# @todo: Do checks before you place champs and assign champs + pos
# @body: Spatula items (only on non class, unique), valid champ position, number of champs, number of same champs, ...
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
        if champ_item[0] == "Aatrox":
            return Aatrox(pos, champ_item, rank, items=items)
        if champ_item[0] == "Ahri":
            return Ahri(pos, champ_item, rank, items=items)
        if champ_item[0] == "Akali":
            return Akali(pos, champ_item, rank, items=items)
        if champ_item[0] == "Anivia":
            return Anivia(pos, champ_item, rank, items=items)
        if champ_item[0] == "Ashe":
            return Ashe(pos, champ_item, rank, items=items)
        if champ_item[0] == "Aurelion Sol":
            return AurelionSol(pos, champ_item, rank, items=items)
        if champ_item[0] == "Blitzcrank":
            return Blitzcrank(pos, champ_item, rank, items=items)
        if champ_item[0] == "Brand":
            return Brand(pos, champ_item, rank, items=items)
        if champ_item[0] == "Braum":
            return Braum(pos, champ_item, rank, items=items)
        if champ_item[0] == "Camille":
            return Camille(pos, champ_item, rank, items=items)
        if champ_item[0] == "Cho'gath":  # check name
            return ChoGath(pos, champ_item, rank, items=items)
        if champ_item[0] == "Darius":  # check name
            return Darius(pos, champ_item, rank, items=items)
        if champ_item[0] == "Draven":  # check name
            return Draven(pos, champ_item, rank, items=items)
        if champ_item[0] == "Elise":  # check name
            return Elise(pos, champ_item, rank, items=items)
        if champ_item[0] == "Evelynn":  # check name
            return Evelyn(pos, champ_item, rank, items=items)
        if champ_item[0] == "Fiora":  # check name
            return Fiora(pos, champ_item, rank, items=items)
        if champ_item[0] == "Gangplank":  # check name
            return Gangplank(pos, champ_item, rank, items=items)
        if champ_item[0] == "Garen":  # check name
            return Garen(pos, champ_item, rank, items=items)
        if champ_item[0] == "Gnar":  # check name
            return Gnar(pos, champ_item, rank, items=items)
        if champ_item[0] == "Graves":  # check name
            return Graves(pos, champ_item, rank, items=items)
        if champ_item[0] == "Jayce":  # check name
            return Jayce(pos, champ_item, rank, items=items)
        if champ_item[0] == "Jinx":  # check name
            return Jinx(pos, champ_item, rank, items=items)
        if champ_item[0] == "Kaisa":  # check name
            return Kaisa(pos, champ_item, rank, items=items)
        if champ_item[0] == "Karthus":  # check name
            return Karthus(pos, champ_item, rank, items=items)
        if champ_item[0] == "Kassadin":  # check name
            return Kassadin(pos, champ_item, rank, items=items)
        if champ_item[0] == "Katarina":  # check name
            return Kataring(pos, champ_item, rank, items=items)
        if champ_item[0] == "Kayle":  # check name
            return Kayle(pos, champ_item, rank, items=items)
        if champ_item[0] == "Kennen":  # check name
            return Kennen(pos, champ_item, rank, items=items)
        if champ_item[0] == "Kha'zix":  # check name
            return Khazix(pos, champ_item, rank, items=items)


# @todo: What should champ do if no enemy is in range for sa
# @body: champs like kha, jayce, camille need a champ in range, currently wasting sa

class Aatrox(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [700, 1260, 2520]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Cleaves the area in front of him,
        # dealing 300 / 600 / 900 magic damage to all enemies within.


class Ahri(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage_to = [100, 200, 300]  # magic
        self.sa_damage_back = [100, 200, 300]  # true

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Fires an orb in a 5-hex line, dealing 100 / 200 / 300
        # magic damage to all enemies it passes through. The orb then
        # returns to her, dealing 100 / 200 / 300 true damage to all enemies
        # it passes through.


class Akali(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [200, 350, 500]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Throws kunai at her target, dealing 200 / 350 / 500
        # magic damage to all enemies in a 2-hex cone. This damage
        # can critically strike.


class Anivia(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage_per_half_second = [66.67, 91.67, 116.67]
        self.sa_slowing_attack_speed = [1 - 0.5, 1 - 0.7, 1 - 0.9]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Creates a large hailstorm that lasts 6 seconds,
        # dealing 66.67 / 91.67 / 116.67 damage every 0.5 seconds
        # for a total of 800 / 1100 / 1400 magic damage and slowing
        # the attack speed of all enemies inside by 50 / 70 / 90%.
        # The storm is not canceled when she dies.


class Ashe(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [200, 400, 600]
        self.sa_stun_duration = [1, 1.5, 2]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Fires an arrow at the farthest enemy that
        # stops on the first target hit, dealing 200 / 400 / 600
        # magic damage and Stun icon stunning them. The stun
        # lasts 1 / 1.5 / 2 seconds per hex traveled.


class AurelionSol(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [250, 500, 750]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: After a 0.35-second delay, breathes fire
        # in a line, dealing 250 / 500 / 750 magic damage
        # to all enemies in the area.


class Blitzcrank(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [250, 550, 850]
        self.sa_stun_duration = 2.5
        self.sa_airborne_duration = 1

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Airborne icon Pulls the furthest enemy
        # into melee range, dealing 250 / 550 / 850 magic
        # damage and Stun icon stunning them for 2.5 seconds.
        # Additionally his next basic attack Airborne icon knocks
        # up his target for 1 seconds. Allies within range will
        # prioritize attacking that enemy.


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


class Braum(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage_reduction = [1 - 0.7, 1 - 0.8, 1 - 0.9]
        self.sa_duration = 4

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Puts up his shield at the furthest enemy
        # for 4 seconds, absorbing and stopping all incoming
        # missiles and reducing his damage taken from that
        # direction by 70 / 80 / 90%.


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
            target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map, origin="spell", originator=self)
            fight.events.append(DummyEvent(1000, (36, 36, 36), fight.map.get_cell_from_id(target.pos)))
            status_effect = StatusEffect(fight.map, self.sa_duration[self.rank - 1], "The Hextech Ultimatum", effects=["root", "priority"])
            target.get_spell_effect(status_effect, fight)


class ChoGath(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [175, 350, 525]
        self.sa_stun_duration = [1.5, 1.75, 2]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: After a 1.5-second delay, ruptures a 3x3 area,
        # dealing 175 / 350 / 525 magic damage and Airborne
        # icon knocking up all enemies within, Stun icon
        # stunning them for 1.5 / 1.75 / 2 seconds.


class Darius(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [150, 200, 250]
        self.sa_heal_for_each_hit = [100, 150, 200]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: After a small delay, swings his axe in a
        # circle, dealing 150 / 200 / 250 magic damage to all
        # nearby enemies and healing himself for 100 / 150 / 200
        # health for each enemy hit.


class Draven(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_ad_bonus = [0.5, 1, 1.5]
        self.sa_attack_speed_boost = 1
        self.sa_duration = 5.75
        self.sa_max_stacks = 2

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Starts spinning his axe, causing his next
        # basic attack to gain 50 / 100 / 150% AD bonus on-hit
        # physical damage and 100% attack speed for 5.75 seconds,
        # stacking up to two times.
        # The spinning axe ricochets off the target high up into
        # the air, landing 2 seconds later at Draven's current
        # position. If Draven catches an axe, Spinning Axe is
        # reapplied for no additional cost on his next basic attack.
        # Draven can hold up to two Spinning Axes in his hands at once.


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
                target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map, origin="spell", originator=self)
                stun = StatusEffect(fight.map, 1.5, "Stun", effects=["stun"])
                target.get_spell_effect(stun, fight)
                fight.events.append(DummyEvent(1000, (36, 36, 36), [fight.map.get_cell_from_id(target.pos)]))

            self.sa_used = None
        else:
            pass


class Gangplank(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [150, 250, 350]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Passive: Periodically places barrels near enemies.
        # Active: Shoots his barrels, causing them all to
        # explode in a chain reaction, dealing 150 / 250 / 350
        # magic damage to enemies caught in the blast and
        # applying on-hit effects.


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
                enemy.get_damage("magic", self.sa_damage[self.rank - 1], fight.map, origin="spell", originator=self)
            fight.events.append(DummyEvent(50, (36, 36, 36), effected_area))
        else:
            self.channel(fight, 4, "Judgement", 0.5, False)
            self.status_effects.append(StatusEffect(fight.map, 4, "Judgement", effects=["immune_magic"]))


class Gnar(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [200, 300, 400]
        self.sa_duration = 60
        self.sa_stun_duration = 2
        self.megaform_health_bonus = [250, 450, 650]
        self.megaform_ad_bonus = [50, 100, 150]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Leaps towards an enemy and transforms into
        # Mega Gnar, becoming a Melee role melee attacker
        # for 60 seconds. After leaping, Airborne icon throws
        # nearby enemies towards his team, dealing
        # 200 / 300 / 400 magic damage and Stun icon stunning
        # them for 2 seconds.
        # While in Mega Gnar form, gains 250 / 450 / 650 health
        # and 50 / 100 / 150 attack damage.


class Graves(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_bonus_ad_damage = [0.05, 0.1, 0.15]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Passive: Basic attacks deal 5 / 10 / 15% AD bonus
        # physical damage and hit all enemies in a 60° 2-hex
        # cone, applying on-hit effects to all enemies hit.


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


class Jinx(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_bonus_attack_speed = [0.6, 0.8, 1]
        self.sa_rocket_bonus_damage = [100, 200, 300]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Passive: After her first takedown, gains 60 / 80 / 100%
        # bonus attack speed.
        # After her second takedown, swaps to her rocket launcher,
        # causing her basic attacks to deal 100 / 200 / 300 bonus
        # magic damage to all enemies in a small area around her
        # target.


class Kaisa(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_shield = [300, 600, 900]
        self.sa_bonus_attack_speed = [0.3, 0.6, 0.9]
        self.sa_duration = 3

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Dashes to the farthest away unit, gaining
        # a 300 / 600 / 900 damage shield and 30 / 60 / 90%
        # bonus attack speed for 3 seconds.


class Karthus(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_damage = [350, 600, 850]
        self.sa_channel_duration = 2.25
        self.sa_random_enemies = [5, 7, 9]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Channels for 2.25 seconds to deal
        # 350 / 600 / 850 magic damage to 5 / 7 / 9 random
        # enemies.


class Kassadin(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_mana_reduce = [25, 50, 75]
        self.sa_shield_duration = 4

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Passive: Basic attacks reduce target's current
        # mana by 25 / 50 / 75, granting a shield for the
        # same amount lasting 4 seconds. The shield can stack.


class Kataring(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_channel_duration = 2.5
        self.sa_enemies = [4, 6, 8]
        self.sa_tick_damage = [45, 70, 95]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Channels for 2.5 seconds, while throwing
        # 15 knives at 4 / 6 / 8 enemies within 2 hexes,
        # dealing 45 / 70 / 95 magic damage per tick and
        # applying Grievous Wounds icon Grievous Wounds,
        # reducing healing on them for 3 seconds. The channel
        # can deal a total of 675 / 1050 / 1425 magic damage.


class Kayle(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_allies = [1, 2, 3]
        self.sa_duration = [2, 2.5, 3]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Targets the 1 / 2 / 3 weakest allies,
        # making them immune to damage for 2 / 2.5 / 3 seconds.


class Kennen(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_duration = 3
        self.sa_damage_per_tick = [37.5, 75, 112.5]
        self.sa_stun_duration = 1.5

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Summons a storm around himself for 3 seconds,
        # dealing 37.5 / 75 / 112.5 magic damage each 0.5
        # seconds to enemies in the area. Each enemy struck 3
        # times is Stun icon stunned for 1.5 seconds.
        # The storm can deal a total of 225 / 450 / 675
        # magic damage.


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
                target.get_damage("magic", self.sa_damage_alone[self.rank - 1], fight.map, origin="spell", originator=self)
            else:
                target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map, origin="spell", originator=self)
            fight.events.append(DummyEvent(1000, (36, 36, 36), effected_area))





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
            target.get_damage("magic", self.sa_damage[self.rank - 1], fight.map, origin="spell", originator=self)





class Shen(DummyChamp):
    def __init__(self, pos, champ_item, rank, items=None):
        super().__init__(pos, champ_item, rank, items=items)
        self.sa_duration = [3, 4, 5]

    def special_ability(self, fight, in_range, visible, alive, time):
        # creates zone around self.pos
        effect = StatusEffect(fight.map, 0, "Spirit's Refuge", effects=["aa_dodge"])
        aoe = Aoe(time, self.sa_duration[self.rank - 1], 0, "around_user", "allie_team", "zone", self, fight, 0, status_effetct=effect)
        fight.aoe.append(aoe)







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



