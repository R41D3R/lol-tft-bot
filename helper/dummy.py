import random

import pygame

from helper.pathfinding_helper import PriorityQueue
from helper.dummy_vision_event import DummyEvent
from helper.damage_visualization import DummyDamage
from helper.status_effect import StatusEffect, GWounds, Channelling, Shield
from config import logger
from helper.aoe import SpinningAxes


class DummyChamp:
    def __init__(self, init_pos, champ_item, rank, fight, items=None):
        self.status_effects = []
        self.fight = fight

        if items is None:
            self.items = []
        else:
            self.items = items
        self.rank = rank

        self.base_stats = champ_item[1]
        print(self.base_stats)
        self.base_range = int(self.base_stats["range"])
        self.name = champ_item[0]

        self.base_health = [int(e) for e in self.base_stats["hp"].split(" / ")]
        self.bonus_health = 0

        self.base_ad = [int(e) for e in self.base_stats["dmg"].split(" / ")]
        self.bonus_ad = 0

        self.base_aa_cc = float(self.base_stats["atk_speed"])
        self.bonus_aa_cc = 0
        self.ability_aa_cc = 0

        self.max_mana = int(self.base_stats["mana"])
        self.mana = int(self.base_stats["starting_mana"]) + (20 * len([item for item in self.items if "mana" in item.attribute]))
        self.base_armor = int(self.base_stats["armor"])
        self.base_mr = int(self.base_stats["mr"])
        self.base_crit_chance = 0.25
        self.base_crit_bonus = 0.5
        self.base_dodge_chance = 0
        self.base_origin = self.base_stats["origin"].split()  # list
        self.base_class = self.base_stats["class"].split()  # list

        # positions
        self.init_pos = init_pos
        self.pos = init_pos
        self.move_progress = 0
        self.start_pos = None
        self.target_pos = None

        self.alive = True
        self.current_health = self.max_health
        self.aa_last = 0  # pygame.time.get_ticks()
        self.damage_events = []
        self.channelling = False
        self.last_target = None
        self.got_damage_from = []
        self.sa_counter = 0
        self.aa_counter = 0

        self.shields = []

        self.team_synergies = None
        self.disables_items = None
        self.imperial_buff = False
        self.noble_buff = False
        self.void_buff = False
        self.fury_stacks = 0
        self.start_ap_bonus = 0
        self.mana_per_source = {}
        self.takedown_counter = 0
        self.sa_stacks = 0  # drave only


    @property
    def direction(self):
        #
        # 6  /\ 1
        # 5 |  | 2
        # 4  \/ 3
        #
        pass
        dir_pos = None
        target = self.get_target(self.get_enemies_in_range(self.fight))

        if target:
            dir_pos = target.pos
        elif self.target_pos:
            dir_pos = self.target_pos
        else:
            if self in self.fight.team_bot:
                return 1
            else:
                return 4

    def on_takedown(self):
        pass

    @property
    def all_shields(self):
        shield_amount = 0
        for shield in self.shields:
            shield_amount += shield.amount
        return shield_amount

    def shield_damage(self, damage, time):
        rest_damage = damage
        if len(self.shields) > 0:
            sorted_durations = sorted(self.shields, key=lambda shield_: shield_.get_duration(time))
            sorted_durations.reverse()
            for shield in sorted_durations:
                if rest_damage > 0:
                    if shield.is_active(time):
                        new_damage = shield.damage(rest_damage)
                        if new_damage >= 0:
                            rest_damage = 0
                        else:
                            rest_damage += new_damage
                else:
                    return 0
        return rest_damage

    def check_shields(self, time):
        for shield in self.shields:
            shield.is_active(time)

    # @todo: outsource target
    # @body: if target none don't switch to next target, interesting for Blademaster
    def autoattack(self, time, fight, enemies_in_range):
        # @todo: split onhit and autoattack

        targets = [self.get_target(enemies_in_range)]
        if None not in targets:
            if len(targets) > 0:
                self.aa_counter += 1
                self.aa_last = time

                self.get_mana("aa")

                # @item: Guinsoo's Rageblade
                item_name = "Guinsoo's Rageblade"
                if self.item_count(item_name) > 0:
                    n_items = self.item_count(item_name)
                    self.bonus_aa_cc += self.base_aa_cc * 0.05 * n_items

                # @synergy: Wild
                synergy_name = "Wild"
                if synergy_name in self.team_synergies:
                    n_syn = self.team_synergies[synergy_name]
                    if n_syn >= 4:
                        if self.fury_stacks < 5:
                            self.fury_stacks += 1
                    elif n_syn >= 2 and synergy_name in self.origin:
                        if self.fury_stacks < 5:
                            self.fury_stacks += 1
                        # @todo: Implement undodgeable aa's (maybe in self.dodge_chance)

                # @synergy: Gunslinger
                synergy_name = "Gunslinger"
                if synergy_name in self.team_synergies and synergy_name in self.class_:
                    n_syn = self.team_synergies[synergy_name]
                    possible_gunslinger_targets = enemies_in_range
                    if len(targets) > 0:
                        possible_gunslinger_targets.remove(targets[0])
                    try:
                        if n_syn >= 6:
                            for _ in range(3):
                                targets.append(possible_gunslinger_targets.pop())
                        elif n_syn >= 4:
                            for _ in range(2):
                                targets.append(possible_gunslinger_targets.pop())
                        elif n_syn >= 2:
                            for _ in range(1):
                                targets.append(possible_gunslinger_targets.pop())
                    except IndexError:
                        pass

            possible_on_hit_targets = []

            # blitzcrank knockup
            if self.has_effect("knockup_on_aa"):
                targets[0].airborne(1, fight.map)
                status_effect = StatusEffect(fight.map, 99999999, "Blitzcrank Knockup", effects=["priority"])
                targets[0].status_effects.appen(status_effect)
                self.remove_effects_with_name("Rocket Grab aa")

            for target in targets:
                damage = self.aa_damage()

                if self.name == "Draven":
                    if self.has_effect("spinning_axes"):
                        sa_ad_bonus = [0.5, 1, 1.5]
                        buffs = self.get_all_effects_with("spinning_axes")
                        stacks = len(buffs)
                        damage += self.ad * sa_ad_bonus[self.rank - 1] * stacks
                        fight.aoe.append(SpinningAxes(fight.now, [], self, fight))

                if self.name == "Jinx":
                    if self.has_effect("jinx_rocket_launcher"):
                        rocket_damage = [100, 200, 300]
                        target.get_damage("magic", rocket_damage[self.rank - 1], fight, origin="sa", originator=self, source="Get Excited")

                if self.name == "Kassadin":
                    mana_steal = [25, 50, 75]
                    mana_reduce = mana_steal[self.rank - 1]
                    target.steal_mana(mana_reduce, user=self)
                    self.shields.append(Shield(self, fight, fight.now, mana_reduce, duration=4))

                # @synergy: Imperial
                if self.imperial_buff:
                    damage *= 2

                hitted = target.get_damage("physical", damage, fight, origin="aa", originator=self)
                if hitted:
                    possible_on_hit_targets.append(target)

                # @item: Statikk Shiv
                item_name = "Statik Shiv"
                if self.item_count(item_name) > 0 and self.aa_counter != 0 and self.aa_counter % 3 == 0:
                    n_items = self.item_count(item_name)
                    target.get_damage("magic", n_items * 100, fight.map, origin="on_hit_no_dodge", originator=self)
                    # ---- need to implement jumping damage -----
                    # Every third basic attack from the wearer deals 100
                    # magic damage to the target and 2 additional targets.
                    # Bounces 3 times? Range?

                # @item: Titanic Hydra
                item_name = "Titanic Hydra"
                if self.item_count(item_name) > 0:
                    n_items = self.item_count(item_name)
                    # all target neighbors cell that are not in attackers.neighbors
                    cleave_area_id = []
                    attacker_neighbors = fight.map.get_cell_from_id(self.pos).neighbors
                    target_neighbors = fight.map.get_cell_from_id(target.pos).neighbors
                    for cell in target_neighbors:
                        if cell not in attacker_neighbors:
                            cleave_area_id.append(cell.id)
                    cleaved_enemies = []
                    for enemy in fight.champs_enemy_team(self):
                        if enemy.pos in cleave_area_id:
                            cleaved_enemies.append(enemy)
                    for enemy in cleaved_enemies:
                        enemy.get_damage("physical", 0.03 * n_items * enemy.max_health, fight, origin="on_hit_no_dodge",
                                         originator=self)

                # @synery: Blademaster
                synergy_name = "Blademaster"
                if synergy_name in self.team_synergies and synergy_name in self.class_ and random.random() <= 0.45:
                    n_syn = self.team_synergies[synergy_name]
                    if n_syn >= 9:
                        for _ in range(4):
                            self.autoattack(time, fight, enemies_in_range)
                    elif n_syn >= 6:
                        for _ in range(2):
                            self.autoattack(time, fight, enemies_in_range)
                    elif n_syn >= 3:
                        self.autoattack(time, fight, enemies_in_range)

                # @item: Runaan's Hurricane
                item_name = "Runaan's Hurricane"
                if self.item_count(item_name) > 0:
                    n_items = self.item_count(item_name)
                    enemy_neighbor_ids = [cell.id for cell in fight.map.get_cell_from_id(target.pos).neighbors]
                    runans_target_counter = 0
                    for enemy in enemies_in_range:
                        if enemy.pos in enemy_neighbor_ids and runans_target_counter < n_items:
                            hitted_ = enemy.get_damage("physical", damage * 0.75, fight, origin="aa", originator=self)
                            if hitted_:
                                possible_on_hit_targets.append(enemy)
                            runans_target_counter += 1

            # on_hit effects
            for target in possible_on_hit_targets:
                # @synergy: Noble
                synergy_name = "Noble"
                if self.noble_buff:
                    self.heal(30, fight.map)

                # @synergy: Demon
                synergy_name = "Demon"
                if synergy_name in self.team_synergies and synergy_name in self.origin and random.random() <= 0.4:
                    n_syn = self.team_synergies[synergy_name]
                    combo = 0
                    if n_syn >= 6:
                        combo = 3
                    elif n_syn >= 4:
                        combo = 2
                    elif n_syn >= 2:
                        combo = 1
                    target.mana -= 20
                    if target.mana < 0:
                        target.mana = 0
                    self.get_mana("Demon", 15 * combo)

                # synergy: Glacial
                synergy_name = "Glacial"
                if synergy_name in self.team_synergies and synergy_name in self.origin:
                    n_syn = self.team_synergies[synergy_name]
                    rnd_n = random.random()
                    if (n_syn >= 6 and rnd_n <= 0.5) or (n_syn >= 4 and rnd_n <= 0.33) or (n_syn >= 2 and rnd_n <= 0.2):
                        target.stun(1.5, fight.map)

                # @item: Sword Breaker
                item_name = "Sword Breaker"
                if self.item_count(item_name) > 0:
                    n_items = self.item_count(item_name)
                    rnd_n = random.random()
                    if (n_items == 1 and rnd_n <= 0.33) or (n_items == 2 and rnd_n <= 0.5511) or (n_items == 3 and rnd_n <= 0.699237):
                        target.disarm(fight.map, 3)

                # @item: Hand of Justice heal
                item_name = "Hand of Justice heal"
                if self.item_count(item_name) > 0:
                    n_items = self.item_count(item_name)
                    self.heal(40 * n_items, fight.map)

                # @item: Hush
                item_name = "Hush"
                if self.item_count(item_name) > 0:
                    n_items = self.item_count(item_name)
                    rnd_n = random.random()
                    if (n_items == 1 and rnd_n <= 0.33) or (n_items == 2 and rnd_n <= 0.5511) or (n_items == 3 and rnd_n <= 0.699237):
                        target.mana_lock(fight.map, 4)

                # @item: Giant Slayer
                item_name = "Giant Slayer"
                if self.item_count(item_name) > 0:
                    on_hit_damage = self.item_count(item_name) * target.max_health * 0.05
                    target.get_damage("true", on_hit_damage, fight, origin="on_hit", originator=self)

                # @item: Cursed Blade
                item_name = "Cursed Blade"
                if self.item_count(item_name) > 0:
                    n_items = self.item_count(item_name)
                    rnd_n = random.random()
                    if n_items == 1 and rnd_n <= 0.2:
                        target.shrink(fight)
                    elif n_items == 2:
                        if 0.36 >= rnd_n > 0.04:
                            target.shrink(fight)
                        elif rnd_n <= 0.04:
                            for _ in range(2):
                                target.shrink(fight)
                    elif n_items == 3:
                        if 0.488 >= rnd_n > 0.104:
                            target.shrink(fight)
                        elif 0.104 >= rnd_n > 0.008:
                            for _ in range(2):
                                target.shrink(fight)
                        elif rnd_n <= 0.008:
                            for _ in range(3):
                                target.shrink(fight)
                # @item: Red Buff
                item_name = "Red Buff"
                if self.item_count(item_name) > 0:
                    if not target.has_effect_with_name("Morellonomicon"):
                        target.gwounds(10, fight, "Morellonomicon", originator=self, dot=True)
                    else:
                        for effect in target.status_effects:
                            if effect.name == "Morellonomicon":
                                effect.duration = 10

    def heal(self, amount, map_):
        health_before = self.current_health
        if self.has_effect("gwound"):
            amount *= 0.2
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        health_after = self.current_health
        healed = health_after - health_before
        self.damage_events.append(DummyDamage(healed, self.position(map_), "heal"))

    def special_ability(self, fight, in_range, visible, alive, time):
        # nearby enemies get Mega Crit
        effected_area = fight.map.get_cell_from_id(self.pos).neighbors
        fight.events.append(DummyEvent(1000, (36, 36, 36), effected_area))
        for n_cell in effected_area:
            for enemy in [champ
                          for champ in fight.champs_enemy_team(self)
                          if champ.alive]:
                if enemy.pos == n_cell.id:
                    enemy.get_damage("magic", self.aa_damage(crit=True) * 2, fight, origin="spell", originator=self)

    @property
    def can_use_sa(self):
        return True

    # ----- Stat Properties ------

    @property
    def origin(self):
        item_origin = []
        # @item: Darkin
        item_name = "Darkin"
        if self.item_count(item_name) > 0:
            item_origin.append("Demon")
        # @item: Frozen Mallet
        item_name = "Frozen Mallet"
        if self.item_count(item_name) > 0:
            item_origin.append("Glacial")
        # @item: Mittens
        item_name = "Mittens"
        if self.item_count(item_name) > 0:
            item_origin.append("Yordle")

        return self.base_origin + item_origin

    @property
    def class_(self):
        item_class = []
        # @item: Youmuu's Ghostblade
        item_name = "Youmuu's Ghostblade"
        if self.item_count(item_name) > 0:
            item_class.append("Assassin")
        # @item: Blade of the Ruined King
        item_name = "Blade of the Ruined King"
        if self.item_count(item_name) > 0:
            item_class.append("Blademaster")
        # @item: Yuumi
        item_name = "Yuumi"
        if self.item_count(item_name) > 0:
            item_class.append("Sorcerer")
        # @item: Knight's Vow
        item_name = "Knight's Vow"
        if self.item_count(item_name) > 0:
            item_class.append("Knight")
        # @item: Youmuu's Ghostblade
        item_name = "Youmuu's Ghostblade"
        if self.item_count(item_name) > 0:
            item_class.append("Assassin")

        return self.base_class + item_class

    def item_sum_from(self, attribute):
        return sum([item.get_attribute_counter(attribute) for item in self.items])

    @property
    def range(self):
        if self.has_effect("melee"):
            range_ = 1
        else:
            range_ = self.base_range
        # @item: Rapid Firecannon
        item_name = "Rapid Firecannon"
        if self.item_count(item_name) > 0:
            n_items = self.item_count(item_name)
            range_ *= 2**n_items
        return self.base_range + len(self.get_all_effects_with("range_buff_+1"))

    @property
    def aa_cc(self):
        # @todo: respect rule: max_as = 5 also for override methods (jayce)
        item_bonus = 0
        item_bonus += self.base_aa_cc * 0.2 * self.item_sum_from("attack_speed")

        buffs = 0.05 * self.base_aa_cc * len(self.get_all_effects_with("small_as_boost"))

        frozen_heart_debuff = 1
        # @item: Frozen Heart
        if self.has_effect("frozen_heart_1"):
            frozen_heart_debuff = 0.35
        elif self.has_effect("frozen_heart_2"):
            frozen_heart_debuff = 0.5775
        elif self.has_effect("frozen_heart_3"):
            frozen_heart_debuff = 0.725375

        wild_bonus = 0
        # @synergy: Wild
        synergy_name = "Wild"
        wild_bonus += self.base_aa_cc * self.fury_stacks * 0.15

        aa_cc = (self.base_aa_cc + item_bonus + wild_bonus + self.bonus_aa_cc + self.ability_aa_cc + buffs) * frozen_heart_debuff

        # @synergy: Ranger
        synergy_name = "Ranger"
        if synergy_name in self.class_:
            if self.has_effect("double_attack_speed"):
                aa_cc *= 2

        if aa_cc > 5:
            aa_cc = 5
        return int(1 / aa_cc * 1000)

    @property
    def ad(self):
        # shrink effect
        shrinks = self.get_all_effects_with("shrink")
        index = self.rank - 1 - len(shrinks)
        if index < 0:
            base_ad = self.base_ad[0] * 0.7
        else:
            base_ad = self.base_ad[index]

        # @synergy: Ninja
        ninja_bonus = 0
        synergy_name = "Ninja"
        if synergy_name in self.team_synergies:
            if self.team_synergies[synergy_name] == 1:
                ninja_bonus += 50
            if self.team_synergies[synergy_name] == 4:
                ninja_bonus += 80

        return base_ad + self.bonus_ad + (15 * self.item_sum_from("ad")) + ninja_bonus

    @property
    def dodge_chance(self):
        return 0.1 * self.item_sum_from("dodge_chance")

    @property
    def crit_chance(self):
        assassin_bonus = 0
        # @synergy: Assassin
        synergy_name = "Assassin"
        if synergy_name in self.team_synergies and synergy_name in self.class_:
            n_syn = self.team_synergies[synergy_name]
            if n_syn >= 9:
                assassin_bonus += 0.3
            elif n_syn >= 6:
                assassin_bonus += 0.2
            elif n_syn >= 3:
                assassin_bonus += 0.1

        return self.base_crit_chance + (0.1 * self.item_sum_from("crit_chance")) + assassin_bonus

    @property
    def max_health(self):
        time_bonus_health = 100 * len(self.get_all_effects_with("bonus_health_100"))

        shrinks = self.get_all_effects_with("shrink")
        index = self.rank - 1 - len(shrinks)
        if index < 0:
            base_health = self.base_health[0] * 0.7
        else:
            base_health = self.base_health[index]
        return base_health + time_bonus_health + self.bonus_health + (200 * self.item_sum_from("health"))

    @property
    def armor(self):
        noble_bonus = 0
        # @synergy: Noble
        synergy_name = "Noble"
        if self.noble_buff:
            noble_bonus += 50
        return self.base_armor + (20 * self.item_sum_from("armor")) + noble_bonus

    @property
    def mr(self):
        noble_bonus = 0
        # @synergy: Noble
        synergy_name = "Noble"
        if self.noble_buff:
            noble_bonus += 50
        return self.base_mr + (20 * self.item_sum_from("mr")) + noble_bonus

    @property
    def ability_power_multiplier(self):
        # (ap_items + ninja bonus + sorcerer bonus) * (1 + (#of_rabadons * 0.5))
        bonus = 0
        item_bonus = (0.2 * len([item for item in self.items if item.attribute == "ap"]))
        ninja_bonus = 0
        sorcerer_bonus = 0
        rabadon_bonus = 1
        imperial_multiplier = 1

        # @synergy: Ninja
        synergy_name = "Ninja"
        if synergy_name in self.team_synergies:
            if self.team_synergies[synergy_name] == 1:
                ninja_bonus += 0.5
            if self.team_synergies[synergy_name] == 4:
                ninja_bonus += 0.8

        # @synergy: Imperial
        if self.imperial_buff:
            imperial_multiplier = 2

        # @item: Rabadon's Deathcap
        item_name = "Rabadon's Deathcap"
        if self.item_count(item_name) > 0:
            n_items = self.item_count(item_name)
            rabadon_bonus += 0.5 * n_items

        return (1 + self.start_ap_bonus + item_bonus + ninja_bonus) * rabadon_bonus * imperial_multiplier

    @property
    def mana_on_aa(self):
        multiplier = 1

        # @synergy: Elementalist
        synergy_name = "Elementalist"
        if synergy_name in self.class_:
            multiplier = 2

        # @synergy: Sorcerer
        synergy_name = "Sorcerer"
        if synergy_name in self.class_:
            multiplier = 2

        if self.rank <= 1:  # how to handle 0-Star units that got downgraded?
            return (6 + random.randint(1, 4)) * multiplier
        else:
            return 10 * multiplier

    @property
    def crit_multiplier(self):
        item_bonus = 0

        # @item: Infinity Edge
        item_name = "Infinity Edge"
        if self.item_count(item_name) > 0:
            n_items = self.item_count(item_name)
            item_bonus += 1.5 * n_items

        assassin_bonus = 0
        # @synergy: Assassin
        synergy_name = "Assassin"
        if synergy_name in self.team_synergies and synergy_name in self.class_:
            n_syn = self.team_synergies[synergy_name]
            if n_syn >= 9:
                assassin_bonus += 2.25
            elif n_syn >= 6:
                assassin_bonus += 1.5
            elif n_syn >= 3:
                assassin_bonus += 0.75

        return 1 + self.base_crit_bonus + item_bonus + assassin_bonus

    def aa_damage(self, crit=False):
        if crit or random.random() <= self.crit_chance:
            return self.ad * self.crit_multiplier
        else:
            return self.ad

    # ----- Items -----

    def has_item(self, item_name):
        pass

    def item_count(self, name):
        item_count = 0
        for item in self.items:
            if item.name == name:
                item_count += 1
        return item_count
    
    def item_proc(self, name):
        proc = None
        for item in self.items:
            if item.name == name:
                if item.last_proc is not None:
                    if proc is None or proc < item.last_proc:
                        proc = item.last_proc
        return proc
    
    def proc_item(self, name, time):
        for item in self.items:
            if item.name == name:
                item.last_proc = time

    # ----- Status Effects ------

    def remove_effects_with_name(self, name):
        for effect in self.status_effects:
            if effect.name == name:
                self.status_effects.remove(effect)
    
    def remove_negative_effects(self):
        for effect in self.status_effects:
            if effect.negative:
                self.status_effects.remove(effect)
    
    def get_spell_effect(self, status_effect, fight):
        if not self.has_effect("immune"):
            self.status_effects.append(status_effect)
        else:
            if status_effect.has("stun"):
                self.stun(status_effect.duration, fight.map)
            # immune visualization

    def has_effect(self, effect):
        for status_effect in self.status_effects:
            if status_effect.has(effect):
                return True
        return False

    def has_effect_with_name(self, name):
        for status_effect in self.status_effects:
            if status_effect.name == name:
                return True
        return False

    def check_status_effects(self, time):
        for status_effect in self.status_effects:
            if not status_effect.is_active(time):
                self.status_effects.remove(status_effect)

    def get_all_effects_with(self, attribute):
        return [effect for effect in self.status_effects if effect.has(attribute)]

    def disarm(self, map_, duration):
        self.status_effects.append(StatusEffect(map_, duration, "Disarm", effects=["disarm"]))

    def mana_lock(self, map_, duration):
        self.status_effects.append(StatusEffect(map_, duration, "Mana-loc", effects=["mana-lock"]))

    def banish(self, map_):
        self.status_effects.append(StatusEffect(map_, 6, "Zephyr", effects=["banish"]))

    def gwounds(self, duration, fight, name, originator, dot=False):
        self.status_effects.append(GWounds(self, fight, duration, name, originator=originator, damage=dot))

    def stealth(self, map_):
        self.status_effects.append(StatusEffect(map_, 10**10, "Stealth", effects=["stealth"]))

    def stun(self, duration, map_):
        self.interrupt()
        self.status_effects.append(StatusEffect(map_, duration, "Stun", effects=["stun"]))

    def root(self, duration, map_):
        self.status_effects.append(StatusEffect(map_, duration, "Root", effects=["root"]))

    def airborne(self, duration, map_):
        self.interrupt()
        self.status_effects.append(StatusEffect(map_, duration, "Airborne", effects=["airborne"]))

    def shrink(self, fight):
        self.status_effects.append(StatusEffect(fight.map, 99999999999, "Shrink", effects=["shrink"]))

    def channel(self, fight, duration, name, proc_interval=None, interruptable=True):
        self.status_effects.append(Channelling(self, fight, duration, name, proc_interval, interruptable))

    def interrupt(self):
        channels = self.get_all_effects_with("channeling")
        for effect in channels:
            if effect.interruptable:
                self.status_effects.remove(effect)

    def immune(self, duration, fight):
        self.status_effects.append(StatusEffect(fight.map, duration, "Immune", effects=["immune"]))

    # ----- Get Damage and Alive -----

    def steal_mana(self, amount, user=None):
        before = self.mana
        self.mana -= amount
        if self.mana < 0:
            self.mana = 0

    
    def get_mana(self, origin, amount_=0, source=None, damage=0):
        amount = amount_
        if not self.has_effect("mana-lock"):
            if origin == "aa":
                amount = self.mana_on_aa

                # @item: Spear of Shojin
                item_name = "Spear of Shojin"
                if self.item_count(item_name) > 0 and self.sa_counter > 0:
                    amount += self.max_mana * 0.15 * self.item_count(item_name)
            elif origin == "damage":
                amount = self.mana_on_aa

                # @todo: mana gain on damage
                # # max 50 mana per damage source
                # if source in self.mana_per_source:
                #     mana_recieved = self.mana_per_source[source]
                #     if mana_recieved >= 50:
                #         return
                #     if mana_recieved + amount > 50:
                #         amount = 50 - mana_recieved
                # else:
                #     self.mana_per_source[source] = amount

            # @item: Seraph's Embrace
            elif origin == "Seraphs's Embrace":
                amount = amount_

            # check if mana is full
            if self.mana + amount >= self.max_mana:
                self.mana = self.max_mana
            else:
                self.mana += amount

    def get_damage(self, type_, incoming_damage, fight, origin=None, originator=None, crit=False, source=None):
        # old implementation
        map_ = fight.map

        # @synergy: Void
        if originator.void_buff and (origin == "aa" or origin == "sa"):
            type_ = "true"

        if origin and originator:
            if origin == "aa":
                if self.has_effect("aa_dodge"):
                    return False
                # implement thornmail
        types = {
            "physical": self.armor,
            "magic": self.mr,
            "true": 0,
        }
        if (random.random() > self.dodge_chance or origin == "on_hit" or origin == "on_hit_no_dodge") and not self.has_effect("immune"):

            # @synergy: Yordle
            synergy_name = "Yordle"
            if not origin == "on_hit_no_dodge" and synergy_name in self.team_synergies and synergy_name in self.origin:
                n_syn = self.team_synergies[synergy_name]
                rnd_n = random.random()
                if (n_syn >= 9 and rnd_n <= 0.9) or (n_syn >= 6 and rnd_n <= 0.6) or (n_syn >= 3 and rnd_n <= 0.3):
                    return False

            if self.has_effect("immune_magic") and type_ == "magic" or self.has_effect("immune_physical") and type_ == "physical":
                return False
            resistance = types[type_]
            damage_reduction = (100 / (resistance + 100))
            real_damage = incoming_damage * damage_reduction

            # @item: Dragon's Claw
            item_name = "Dragon's Claw"
            if self.item_count(item_name) > 0 and type_ == "magic":
                n_items = self.item_count(item_name)
                if n_items == 1:
                    real_damage = incoming_damage * (1 - 0.75)
                elif n_items == 2:
                    real_damage = incoming_damage * (1 - 0.9375)
                elif n_items == 3:
                    real_damage = incoming_damage * (1 - 0.984375)

            # @synergy: Dragon
            synergy_name = "Dragon"
            if synergy_name in self.team_synergies and synergy_name in self.origin and type_ == "magic":
                if self.team_synergies[synergy_name] >= 2:
                    real_damage *= (1 - 0.75)

            if originator not in self.got_damage_from:
                self.got_damage_from.append(originator)
            if origin == "aa" or origin == "sa":
                if origin == "aa":
                    # @item: Bloodthirster
                    item_name = "Bloothirster"
                    if originator.item_count(item_name) > 0:
                        heal = real_damage * 0.4 * originator.item_count(item_name)
                        originator.heal(heal, map_)

                    # elise lifesteal
                    if originator.has_effect("elise_lifesteal"):
                        rank_lifesteal = [0.6, 0.9, 1.2]
                        heal = real_damage * rank_lifesteal[originator.rank - 1]
                        originator.heal(heal, map_)

                    # @item: Thornmail
                    item_name = "Thornmail"
                    if self.item_count(item_name) > 0:
                        n_items = self.item_count(item_name)
                        originator.get_damage("magic", incoming_damage * n_items, fight, origin="item", originator=self)
                        real_damage = 0
                if origin == "sa":
                    # @item: Jeweled Gauntlet
                    item_name = "Jeweled Gauntlet"
                    if originator.item_count(item_name) > 0 and random.random() <= originator.crit_chance:
                        real_damage *= originator.crit_multiplier

                    # @item: Morellonomicon
                    item_name = "Morellonomicon"
                    if originator.item_count(item_name) > 0:
                        if not self.has_effect_with_name(item_name):
                            self.gwounds(10, fight, item_name, originator=originator, dot=True)
                        else:
                            for effect in self.status_effects:
                                if effect.name == item_name:
                                    effect.duration = 10

                    # @item: Luden's Echo
                    item_name = "Luden's Echo"
                    if originator.item_count(item_name) > 0:
                        n_items = originator.item_count(item_name)
                        # When the wearer deals damage with their Special Ability,
                        # the first target hit and up to 3 nearby enemies are dealt
                        # an additional 180 magic damage. -> stacks normal
                        damage = 180 * n_items
                        self.get_damage("magic", damage, fight, origin="item", originator=originator, source="Luden's Echo")
                        # deal 3 nearby enemies damage -> allies
                        for allie in random.choices(self.fight.adjacent_allies(self), k=3):
                            allie.get_damage("magic", damage, fight, origin="item", originator=originator, source="Luden's Echo")

                # @item: Hextech Gunblade
                # @todo: Hextech multiple item healing is not tested
                # @body: [Link to Stat Website](https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:Items)
                item_name = "Hextech Gunblade"
                if originator.item_count(item_name) > 0:
                    hextech_healing = [0.25, 0.6506, 1.314]
                    originator.heal(real_damage * hextech_healing[originator.item_count(item_name) - 1], map_)

            # @synergy: Knight
            synergy_name = "Knight"
            if synergy_name in self.team_synergies:
                n_syn = self.team_synergies[synergy_name]
                if n_syn >= 6:
                    real_damage -= 65
                elif n_syn >=4:
                    real_damage -= 35
                elif n_syn >= 2:
                    real_damage -= 15
                if real_damage < 0:
                    real_damage = 0

            # shield
            damage_after_shield = self.shield_damage(real_damage, map_.time)

            self.current_health -= damage_after_shield
            self.damage_events.append(DummyDamage(real_damage, self.position(map_), type_))
            self.get_mana("damage", source=source)
            self.check_alive()
            return True
        else:
            # @item: Iceborn Gauntlet
            item_name = "Iceborn Gauntlet"
            if self.item_count(item_name) > 0:
                # @todo: Implement Iceborn Gauntlet after Aoe implementation
                pass
            return False

    def check_alive(self):
        if self.current_health <= 0:
            self.kill()

    def kill(self):
        map_ = self.fight.map
        # @item: Guradian Angel
        item_name = "Guardian Angel"
        if self.item_count(item_name) > 0 and self.item_proc(item_name) is None:
            self.stop_moving(map_, map_=True)
            self.proc_item(item_name, map_.time)
            self.mana = 0
            self.current_health = 500
            self.status_effects.append(StatusEffect(map_, 2, "Guardian Angel", effects=["revive"]))
            return False

        # @item: Repeating Crossbow
        item_name = "Repeating Crossbow"
        if self.item_count(item_name) > 0:
            for item in self.items:
                if item.name == item_name:
                    item.attribute.extend(["crit_chance", "crit_chance", "attack_speed"])
                    # npc champs included
                    possible_allies = [allie for allie in self.fight.champs_allie_team(self) if len(allie.items) < 3]
                    random_allie = random.choice(possible_allies)
                    random_allie.items.append(item)

        for enemy in self.got_damage_from:
            if enemy:
                enemy.takedown_counter += 1
                enemy.on_takedown()

                # @item: Deathblade
                item_name = "Deathblade"
                if enemy.item_count(item_name) > 0:
                    enemy.bonus_ad += 15

        logger.debug(f"Champ died on {self.pos}")
        self.alive = False
        if self.pos is not None:
            map_.get_cell_from_id(self.pos).taken = False
        # if self.next_pos is not None:
        #     map_.get_cell_from_id(self.next_pos).taken = False
        if self.target_pos is not None:
            map_.get_cell_from_id(self.target_pos).taken = False
        return True

    # ----- Helper -----

    def get_enemies_in_range(self, fight, range_=None):
        if range_ is None:
            range_ = self.range
        current_cell = fight.map.get_cell_from_id(self.pos)
        enemy_champs_visible = fight.enemy_team_visible(self)
        cell_ids_in_range = [cell.id for cell in fight.map.get_all_cells_in_range(current_cell, range_)]
        return [enemy for enemy in enemy_champs_visible if enemy.pos in cell_ids_in_range]

    def get_allies_around(self, fight):
        current_cell_neighbors_ids = [cell.id for cell in fight.map.get_cell_from_id(self.pos).neighbors]
        return [allie for allie in fight.champs_allie_team(self) if allie.pos in current_cell_neighbors_ids]

    def get_target(self, enemies_in_range):
        # check if priority target is in range
        priority_targets = [champ for champ in enemies_in_range if champ.has_effect("priority")]
        if len(priority_targets) > 0:
            if self.last_target in priority_targets:
                return self.last_target
            else:
                return random.choice(priority_targets)
        # @todo: priority for nearest enemy
        if self.last_target is None or self.last_target not in enemies_in_range:
            if len(enemies_in_range) == 0:
                return None
            self.last_target = random.choice(enemies_in_range)
        return self.last_target

    # ----- rendering -----

    def draw(self, surface, fight, team):
        map_ = fight.map
        font = pygame.font.SysFont("Comic Sans Ms", 20)
        player_pos = self.position(map_)

        # ----- player -----
        if team == "team_bot":
            color = (67, 52, 235)
        else:
            color = (229, 235, 52)
        pygame.draw.circle(surface, color, player_pos, 30)

        # ----- health bar -----
        hb_width = 60
        hb_height = 10
        hb_x = player_pos[0] - (hb_width / 2)
        hb_y = player_pos[1] - (hb_height / 2)
        # health background bar
        pygame.draw.rect(surface, (0, 0, 0), (hb_x, hb_y, hb_width, hb_height))
        # health progress bar
        pygame.draw.rect(surface, (0, 130, 46), (hb_x, hb_y, int(hb_width * self.current_health / self.max_health), hb_height))
        # SHIELD
        shield_pos_x = (hb_x + hb_width)
        shield_width = int(hb_width * (self.all_shields / self.max_health))
        if shield_width > hb_width:
            shield_width = hb_width
        pygame.draw.rect(surface, (214, 214, 214), (shield_pos_x, hb_y, -shield_width, hb_height))

        # ----- mana bar -----
        mb_width = 60
        mb_height = 10
        mb_x = player_pos[0] - (mb_width / 2)
        mb_y = hb_y + mb_height
        # mana background bar
        pygame.draw.rect(surface, (0, 0, 0), (mb_x, mb_y, mb_width, mb_height))
        # mana progress bar
        pygame.draw.rect(surface, (52, 219, 235), (mb_x, mb_y, int(mb_width * (self.mana / (self.max_mana + 0.01))), mb_height))

        # ----- status effects ------
        # channeling
        cb_width = 60
        cb_height = 3
        cb_x = player_pos[0] - (cb_width / 2)
        cb_y = mb_y + mb_height
        if self.has_effect("channeling"):
            effect = self.get_all_effects_with("channeling")[0]
            pygame.draw.rect(surface, (0, 0, 0), (cb_x, cb_y, cb_width, cb_height))
            pygame.draw.rect(surface, (255, 255, 255),
                             (cb_x, cb_y, int(cb_width * (fight.now - effect.created) / effect.duration), cb_height))
        # effects
        effect_font = pygame.font.SysFont("Comic Sans Ms", 15)
        effect_counter = 0
        for status_effect in self.status_effects:
            for effect in status_effect.effects:
                effect_counter += 1
                effect_text = effect_font.render(effect, True, (0, 0, 0))
                surface.blit(effect_text, (player_pos[0] - 30, cb_y + effect_counter * 8))

        # ----- name ------
        text = font.render(f"{self.name} [{self.rank}]", True, (0, 0, 0))
        surface.blit(text, (player_pos[0] - 30, player_pos[1] - 20))

        # ----- items -----
        item_font = pygame.font.SysFont("Comic Sans Ms", 15)
        item_counter = 0
        for item in self.items:
            item_counter += 1
            item_name = item_font.render(item.name, True, (30, 30, 30))
            surface.blit(item_name, (player_pos[0] - 30, player_pos[1] - 20 - int(item_counter * 10)))

        # ----- damage -----
        for dmg in self.damage_events:
            if dmg.is_active(fight.now):
                dmg.render(surface, fight.now)
            else:
                self.damage_events.remove(dmg)

    # ----- Positioning -----

    @property
    def my_cell(self):
        return self.fight.map.get_cell_from_id(self.pos)

    def position(self, map_):
        current_cell = map_.get_cell_from_id(self.pos)
        if self.target_pos:
            next_cell = map_.get_cell_from_id(self.target_pos)
            return int(current_cell.center[0] + ((next_cell.center[0] - current_cell.center[0]) * self.move_progress)), int(current_cell.center[1] + ((next_cell.center[1] - current_cell.center[1]) * self.move_progress))
        return int(current_cell.center[0]), int(current_cell.center[1])

    def update_pos(self, new_pos):
        # check if neighbor from current pos
        # move
        pass

    def stop_moving(self, fight, map_=False):
        if self.target_pos and self.target_pos != self.pos:
            if map_:
                fight.get_cell_from_id(self.target_pos).taken = False
            else:
                fight.map.get_cell_from_id(self.target_pos).taken = False
        self.start_pos = None
        self.target_pos = None
        self.move_progress = 0

    def move_to(self, new_cell, fight):
        fight.map.get_cell_from_id(self.pos).taken = False
        self.start_pos = None
        self.target_pos = None
        self.move_progress = 0
        self.pos = new_cell.id
        new_cell.taken = True

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        # print(f"best path from {start.id} to {goal.id}")
        current = goal
        path = []
        while current != start:
            # print(f"from {current.id}")
            path.append(current)
            current = came_from[current]
            # print(f"to {current.id}")

        path.append(start)  # optional
        path.reverse()  # optional
        return path

    def find_shortest_path_to_enemy(self, enemy, map_):
        start = map_.get_cell_from_id(self.pos)
        if enemy.target_pos is None:
            goal_locations = map_.get_cell_from_id(enemy.pos).free_neighbors
        else:
            goal_locations = map_.get_cell_from_id(enemy.target_pos).free_neighbors
        if len(goal_locations) == 0:
            return []
        best_came_from, best_cost = {}, 9999999
        best_goal = None
        for goal in goal_locations:
            came_from, cost = dijkstra_path(start, goal)
            if came_from is None and cost is None:
                return []
            if cost < best_cost:
                best_came_from, best_cost = came_from, cost
                best_goal = goal

        return self.reconstruct_path(best_came_from, start, best_goal)

    # todo: Maybe replace pathfinding with best path for team
    # body: Also a option is to order champ turn after min move_distance_to_enemy, maybe predict if cell is free if you reach it, best intersection from enemy_and_my team and champ path,
    def get_move_to_closest_enemy(self, enemy_team, map_):
        best_path = None
        for enemy in enemy_team:
            path = self.find_shortest_path_to_enemy(enemy, map_)
            if best_path:
                if len(path) < len(best_path):
                    best_path = path
            else:
                best_path = path
        if best_path is None:
            return None
        if len(best_path) == 0:
            return None
        # print(best_path)
        return best_path[1]


def dijkstra_path(start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_ in current.free_neighbors:
            new_cost = cost_so_far[current] + 1
            if next_ not in cost_so_far or new_cost < cost_so_far[next_]:
                cost_so_far[next_] = new_cost
                priority = new_cost
                frontier.put(next_, priority)
                came_from[next_] = current
    try:
        return came_from, cost_so_far[goal]
    except KeyError:
        return None, None
