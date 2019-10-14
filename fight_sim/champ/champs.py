import random

from fight_sim.champ.dummy import DummyChamp
from fight_sim.effects.dummy_vision_event import DummyEvent
from fight_sim.effects.aoe import Aoe
from fight_sim.effects.status_effect import StatusEffect
from fight_sim.effects.shield import Shield


class Aatrox(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [300, 600, 900]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Cleaves the area in front of him,
        # dealing 300 / 600 / 900 magic damage to all enemies within
        target = self.get_target(in_range)
        target_cell = fight.map.get_cell_from_id(target.pos)
        effected_area = [target_cell] + target_cell.neighbors
        damage = self.sa_damage[self.rank - 1]
        targets = [target] + self.fight.adjacent_allies(target)
        for target in targets:
            target.get_damage("magic", damage, fight, origin="sa", originator=self, source="The Darkin Blade")
        fight.events.append(DummyEvent(1000, (36, 36, 36), effected_area))

    @property
    def can_use_sa(self):
        if len(self.fight.adjacent_enemies(self)) > 0:
            return True
        else:
            return False


class SpiritOrb(Aoe):
    def __init__(self, fight, user, effected_area, interval, damage):
        super().__init__(fight, user, effected_area=effected_area, interval=interval)
        self.area_index_counter = 0
        self.true_damage = False
        self.damage = damage
        self.name = "Spirit Orb"

    def proc(self):
        if self.last_proc is None:
            self.do_damage()
        elif self.fight.now - self.last_proc >= self.proc_interval:
            self.last_proc = self.fight.now
            self.do_damage()

        if self.true_damage and self.area_index_counter == 0:
            self.activated = True

    def do_damage(self):
        if not self.true_damage:
            self.area_index_counter += 1
        else:
            self.area_index_counter -= 1

        if self.area_index_counter > 5:
            self.area_index_counter = 5
            self.true_damage = True
        current_cell = self.effected_area[self.area_index_counter]
        if current_cell is not None:
            enemy = self.fight.get_champ_from_cell(current_cell)
            if enemy in self.fight.enemy_champs_alive(self.user):
                if self.true_damage:
                    enemy.get_damage("true", self.damage, self.fight, origin="sa", originator=self.user, source=self.name)
                else:
                    enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source=self.name)
                self.fight.events.append(DummyEvent(200, (36, 36, 36), [current_cell], type_="half_fade"))


class Ahri(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [100, 200, 300]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Fires an orb in a 5-hex line, dealing 100 / 200 / 300
        # magic damage to all enemies it passes through. The orb then
        # returns to her, dealing 100 / 200 / 300 true damage to all enemies
        # it passes through.
        area_cells = fight.get_ability_area(self.get_target(in_range), self, 5)
        fight.aoe.append(SpiritOrb(fight, self, area_cells, 0.2, self.sa_damage[self.rank - 1]))


class Akali(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [200, 350, 500]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Throws kunai at her target, dealing 200 / 350 / 500
        # magic damage to all enemies in a 2-hex cone. This damage
        # can critically strike.
        first_dir = fight.get_direction(self.pos, self.get_target(in_range).pos)
        area_ids = [(self.pos[0] + fight.map.dir_dict[first_dir][0], self.pos[1] + fight.map.dir_dict[first_dir][1]),
                    (self.pos[0] + fight.map.dir_dict[first_dir + 1][0], self.pos[1] + fight.map.dir_dict[first_dir + 1][1]),
                    (self.pos[0] + fight.map.dir_dict[first_dir - 1][0], self.pos[1] + fight.map.dir_dict[first_dir - 1][1])]
        for id_ in area_ids:
            if fight.map.is_id_in_map(id_):
                cell = fight.map.get_cell_from_id(id_)
                enemy = fight.get_champ_from_cell(cell)
                damage = self.sa_damage[self.rank - 1]
                if enemy:
                    if random.random() <= self.crit_chance:
                        enemy.get_damage("magic", damage, fight, origin="sa", originator=self, crit=True, source="Five Point Strike")
                    else:
                        enemy.get_damage("magic", damage, fight, origin="sa", originator=self, crit=False, source="Five Point Strike")
                self.fight.events.append(DummyEvent(500, (36, 36, 36), [cell]))

    @property
    def can_use_sa(self):
        if len(self.fight.adjacent_enemies(self)) > 0:
            return True
        else:
            return False


class GlacialStorm(Aoe):
    def __init__(self, fight, user, duration, effected_area, interval, damage, as_slow):
        super().__init__(fight, user, duration=duration, effected_area=effected_area, interval=interval)
        self.damage = damage
        self.as_slow_stacks = as_slow
        self.name = "Glacial Storm"

    def proc(self):
        if self.last_proc is None:
            self.activated = True
            self.do_effect()
        elif self.fight.now - self.last_proc >= self.proc_interval:
            self.do_effect()
        else:
            pass

    def do_effect(self):
        for enemy in self._all_enemies_in_area():
            for _ in range(self.as_slow_stacks):
                enemy.status_effects.append(StatusEffect(self.fight.map, 0, "Glacial Storm", effects=["as_slow"]))
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source=self.name)
        self.fight.events.append(DummyEvent(500, (36, 36, 36), self.effected_area, type_="half_fade"))


class Anivia(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage_per_half_second = [66.67, 91.67, 116.67]
        self.sa_slowing_attack_speed = [10, 14, 18]  # stacks: 5% as slow per stack

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Creates a large hailstorm that lasts 6 seconds,
        # dealing 66.67 / 91.67 / 116.67 damage every 0.5 seconds
        # for a total of 800 / 1100 / 1400 magic damage and slowing
        # the attack speed of all enemies inside by 50 / 70 / 90%.
        # The storm is not canceled when she dies.
        random_enemy = random.choice(visible)
        area = fight.map.get_all_cells_in_range(fight.map.get_cell_from_id(random_enemy.pos), 2)
        fight.aoe.append(GlacialStorm(fight, self, duration=6, effected_area=area, interval=0.5, damage=self.sa_damage_per_half_second[self.rank - 1], as_slow=self.sa_slowing_attack_speed[self.rank - 1]))


class EnchantedCrystalArrow(Aoe):
    def __init__(self, fight, user, effected_area, interval, damage, stun_duration):
        super().__init__(fight, user, effected_area=effected_area, interval=interval)
        self.damage = damage
        self.stun_duration = stun_duration
        self.area_index_counter = 0
        self.last_proc = self.fight.now
        self.name = "Enchanted Crystal Arrow"

    def proc(self):
        if self.fight.now - self.last_proc >= self.proc_interval:
            self.last_proc = self.fight.now
            self.area_index_counter += 1
            cell = self.effected_area[self.area_index_counter]
            self.fight.events.append(DummyEvent(100, (0, 86, 110), [cell], type_="half_fade"))

            for enemy in self.fight.enemy_champs_alive(self.user):
                if cell is not None:
                    if enemy.pos == cell.id:
                        self.do_effect(enemy)

            if self.area_index_counter == len(self.effected_area - 1):
                self.activated = True

    def do_effect(self, enemy):
        duration = self.stun_duration * (self.area_index_counter + 1)
        enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Enchanted Crystal Arrow")
        enemy.stun(duration, self.fight.map)
        self.fight.events.append(DummyEvent(int(1000 * duration), (92, 102, 93), [enemy.my_cell]))
        self.activated = True


class Ashe(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [200, 400, 600]
        self.sa_stun_duration = [1, 1.5, 2]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Fires an arrow at the farthest enemy that
        # stops on the first target hit, dealing 200 / 400 / 600
        # magic damage and Stun icon stunning them. The stun
        # lasts 1 / 1.5 / 2 seconds per hex traveled.
        enemy = fight.furthest_enemy_away(self)
        area = fight.get_ability_area(enemy, self, 20)
        fight.aoe.append(EnchantedCrystalArrow(fight, self, area, 0.1, self.sa_damage[self.rank - 1], self.sa_stun_duration[self.rank - 1]))


class VoiceofLight(Aoe):
    def __init__(self, fight, user, delay, area, damage):
        super().__init__(fight, user, delay=delay, effected_area=area, user_needed=True)
        self.damage = damage

    def proc(self):
        if self.user.alive:
            if self.fight.now - self.created >= self.delay:
                self.proc()
                self.activated = True
        else:
            self.activated = True

    def do_effect(self):
        self.fight.events.append(DummyEvent(500, (66, 21, 92), [self.effected_area]))
        for cell in self.effected_area:
            for enemy in self.fight.enemy_champs_alive(self.user):
                if cell.id == enemy.pos:
                    enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Voice of Light")


class AurelionSol(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [250, 500, 750]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: After a 0.35-second delay, breathes fire
        # in a line, dealing 250 / 500 / 750 magic damage
        # to all enemies in the area.
        area = fight.get_ability_area(self.get_target(visible), self, 15)
        self.channel(fight, 0.35, "Voice of Light", interruptable=False)
        fight.aoe.append(VoiceofLight(fight, self, 0.35, area, self.sa_damage[self.rank - 1]))


class RocketGrab(Aoe):
    def __init__(self, fight, user, effected_area, damage, stun_duration):
        super().__init__(fight, user, effected_area=effected_area, interval=0.1, user_needed=True)
        self.damage = damage
        self.stun_duration = stun_duration
        self.area_index = -1
        self.last_proc = fight.now

    def proc(self):
        if self.fight.now - self.last_proc >= self.proc_interval:
            self.last_proc = self.fight.now
            self.area_index += 1
            current_cell = self.effected_area[self.area_index]
            if current_cell is not None:
                self.fight.events.append(DummyEvent(0.1, (217, 187, 22), [current_cell], type_="half_fade"))

                for enemy in self.fight.enemy_champs_alive(self.user):
                    if enemy.pos == current_cell.id:
                        self.do_effect(enemy)
                        self.activated = True

            if self.area_index + 1 >= len(self.effected_area):
                self.activated = True

    def do_effect(self, enemy):
        new_cell = enemy.my_cell
        for cell in self.effected_area:
            if not cell.taken:
                new_cell = cell
                break
        enemy.move_to(new_cell, self.fight)
        enemy.stun(2.5, self.fight.map)
        enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Rocket Grab")
        # remove status effects from blitz
        self.user.remove_effects_with_name("Rocket Grab")


class Blitzcrank(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [250, 550, 850]
        self.sa_stun_duration = 2.5
        self.sa_airborne_duration = 1

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Airborne icon Pulls the furthest enemy
        # into melee range, dealing 250 / 550 / 850 magic
        # damage and Stun icon stunning them for 2.5 seconds.
        # Additionally his next basic attack Airborne icon knocks
        # up his target for 1 seconds. Allies within range will
        # prioritize attacking that enemy.
        target = fight.furthest_enemy_away(self)
        area = fight.get_ability_area(target, self, None)
        # grab -> status effect on self
        self.channel(fight, 2, "Rocket Grab", interruptable=False)
        self.status_effects.append(StatusEffect(fight.map, 999999, "Rocket Grab aa", effects=["knockup_on_aa"]))
        fight.aoe.append(RocketGrab(fight, self, area, self.sa_damage[self.rank - 1], self.sa_stun_duration))


class Pyroclasm(Aoe):
    def __init__(self, fight, user, damage, bounces, enemy):
        super().__init__(fight, user, interval=0.5)
        self.damage = damage
        self.bounces = bounces
        self.bounce_counter = 0
        self.last_proc = fight.now
        self.last_enemy = enemy

    def proc(self):
        if self.fight.now - self.last_proc >= self.proc_interval and self.bounce_counter < self.bounces:
            enemies_in_bounce_range = self.fight.get_n_closest_allies(self.last_enemy, 1)
            if len(enemies_in_bounce_range) > 0:
                self.bounce_counter += 1
                random_bounce_enemy = random.choice(enemies_in_bounce_range)
                self.do_effect(random_bounce_enemy)
            else:
                self.activated = True

    def do_effect(self, enemy):
        self.last_enemy = enemy
        enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Pyroclasm")
        self.fight.events.append(DummyEvent(0.5, (217, 40, 0), [enemy.my_cell], type_="half_fade"))

        if self.bounce_counter == self.bounces:
            self.activated = True


class Brand(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [250, 450, 650]
        self.sa_bounces = [4, 6, 20]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Launches a bouncing fireball at an enemy.
        # The fireball bounces to nearby enemies
        # up to 4 / 6 / 20 times, dealing 250 / 450 / 650 magic damage
        # with each bounce.
        target = self.get_target(visible)
        fight.aoe.append(Pyroclasm(fight, self, self.sa_damage[self.rank - 1], self.sa_bounces[self.rank - 1], target))


class Braum(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage_reduction = [1 - 0.7, 1 - 0.8, 1 - 0.9]
        self.sa_duration = 4
        self.shield_target = None

    def special_ability(self, fight, in_range, visible, alive, time):
        self.shield_target = fight.furthest_enemy_away(self)

        # for autoattack, check if braum is between
        # for sa, maybe add type, missle
        # damage direction -> get_damage

        # Active: Puts up his shield at the furthest enemy
        # for 4 seconds, absorbing and stopping all incoming
        # missiles and reducing his damage taken from that
        # direction by 70 / 80 / 90%.


class Camille(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_duration = [4, 5, 6]
        self.sa_damage = [200, 325, 450]

    def special_ability(self, fight, in_range, visible, alive, time):
        # big damage on enemy
        # roots enemy + status_effect(allies prioritize target)
        target = self.get_target(in_range)
        target.get_damage("magic", self.sa_damage[self.rank - 1], fight, origin="sa", originator=self, source="The Hextech Ultimatum")
        fight.events.append(DummyEvent(1000, (92, 102, 93), fight.map.get_cell_from_id(target.pos)))
        status_effect = StatusEffect(fight.map, self.sa_duration[self.rank - 1], "The Hextech Ultimatum", effects=["root", "priority"])
        target.status_effects.append(status_effect)

    @property
    def can_use_sa(self):
        if len(self.fight.adjacent_enemies(self)) > 0:
            return True
        else:
            return False


class Rupture(Aoe):
    def __init__(self, fight, user, effected_area, damage, stun_duration):
        super().__init__(fight, user, delay=1.5, effected_area=effected_area)
        self.damage = damage
        self.stun_duration = stun_duration

    def proc(self):
        if self.fight.now - self.created >= self.delay:
            self.do_effect()
            self.activated = True

    def do_effect(self):
        self.fight.events.append(DummyEvent(1.5, (53, 27, 64), [self.effected_area]))
        for enemy in self._all_enemies_in_area():
            enemy.stun(self.stun_duration, self.fight.map)
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Rupture")


class ChoGath(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [175, 350, 525]
        self.sa_stun_duration = [1.5, 1.75, 2]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: After a 1.5-second delay, ruptures a 3x3 area,
        # dealing 175 / 350 / 525 magic damage and Airborne
        # icon knocking up all enemies within, Stun icon
        # stunning them for 1.5 / 1.75 / 2 seconds.
        target = self.get_target(visible)
        area = fight.map.get_all_cells_in_range(target.my_cell, 3)
        fight.aoe.append(Rupture(fight, self, area, self.sa_damage[self.rank - 1], self.sa_stun_duration[self.rank - 1]))


class Decimate(Aoe):
    def __init__(self, fight, user, effected_area, damage, heal_per_hit):
        super().__init__(fight, user, delay=1, effected_area=effected_area, user_needed=True)
        self.damage = damage
        self.heal_per_hit = heal_per_hit

    def proc(self):
        if self.fight.now - self.created >= self.delay and self.user.alive:
            self.do_effect()
            self.activated = True

        if not self.user.alive:
            self.activated = True

    def do_effect(self):
        hitted_enemys = 0
        user_cell = self.fight.map.get_cell_from_id(self.user.pos)
        self.fight.events.append(DummyEvent(0.5, (36, 36, 36), [self.effected_area]))
        for enemy in self._all_enemies_in_area():
            hitted_enemys += 1
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Decimate")
        if hitted_enemys > 0:
            self.user.heal(self.heal_per_hit * hitted_enemys, self.fight.map)


class Darius(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [150, 200, 250]
        self.sa_heal_for_each_hit = [100, 150, 200]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: After a small delay, swings his axe in a
        # circle, dealing 150 / 200 / 250 magic damage to all
        # nearby enemies and healing himself for 100 / 150 / 200
        # health for each enemy hit.
        self.channel(fight, 1, "Decimate")
        area = self.my_cell.neighbors
        fight.aoe.append(Decimate(fight, self, area, self.sa_damage[self.rank - 1], self.sa_heal_for_each_hit[self.rank - 1]))


class Draven(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_attack_speed_boost = 1
        self.sa_duration = 5.75
        self.sa_max_stacks = 2

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Starts spinning his axe, causing his next
        # basic attack to gain 50 / 100 / 150% AD bonus on-hit
        # physical damage and 100% attack speed for 5.75 seconds,
        # stacking up to two times.
        # The spinning axe ricochets off the target high up into
        # the air, landing 2 seconds later at Draven's current
        # position. If Draven catches an axe, Spinning Axe is
        # reapplied for no additional cost on his next basic attack.
        # Draven can hold up to two Spinning Axes in his hands at once.
        buffs = self.get_all_effects_with("spinning_axes")
        if len(buffs) < 2:
            self.status_effects.append(StatusEffect(fight.map, 5.75, "Spinning Axes", effects=["spinning_axes"]))
        # @todo: refresh draven buffs on activation


class Elise(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_spiderlings = [1, 2, 4]
        self.spider_lifesteal = [0.6, 0.9, 1.2]
        self.spider_health = 500
        self.spider_ad = 60
        self.spider_atk_speed = 0.7
        # create spider npc
        # spider gets demon bonus

    def special_ability(self, fight, in_range, visible, alive, time):
        summon_counter = 0
        range_counter = 1
        while summon_counter < self.sa_spiderlings[self.rank - 1]:
            free_positions = [cell for cell in self.fight.map.get_all_cells_in_range(self.my_cell, range_counter) if not cell.taken]
            if len(free_positions) > 0:
                random_cell = random.choice(free_positions)
                spider = Spider(random_cell.id, fight)
                if self in fight.team_bot:
                    fight.team_bot.append(spider)
                    random_cell.taken = True
                    summon_counter += 1
            else:
                range_counter += 1

        # transform
        self.status_effects.append(StatusEffect(fight.map, 60, "Spider Form", effects=["melee", "elise_lifesteal"]))

        # Active: Summons 1 / 2 / 4 Spiderlings and transforms
        # to her Spider Form, becoming a Melee role melee attacker for 60 seconds.
        # While in Spider Form, gains 60 / 90 / 120% life steal.
        # Each Spiderling has 500 health, 60 attack damage
        # and 0.7 attack speed, and can gain the Demon bonus.


class Spider(DummyChamp):
    def __init__(self, pos, fight):
        spider_dict = {
            "range": 1,
            "hp": "500 / 500 / 500",
            "dmg": "60 / 60 / 60",
            "atk_speed": 0.7,
            "mana": 0,
            "starting_mana": 0,
            "armor": 0,
            "mr": 0,
            "origin": "Demon",
            "class": "",
        }
        super().__init__(pos, ["Spider", spider_dict], 1, fight, items=[])

    def special_ability(self, fight, in_range, visible, alive, time):
        pass

    @property
    def can_use_sa(self):
        return False


class LastCaress(Aoe):
    def __init__(self, fight, user, enemies, damage, low_health_damage, new_cell):
        super().__init__(fight, user, delay=0.35, user_needed=True)
        self.enemies = enemies
        self.damage = damage
        self.low_health_damage = low_health_damage
        self.new_cell = new_cell

    def proc(self):
        if self.fight.now - self.created >= self.delay and self.user.alive:
            self.do_effect()
            self.activated = True

        if not self.user.alive:
            self.activated = True

    def do_effect(self):
        for enemy in self.enemies:
            if enemy.alive:
                enemy_health_ratio = enemy.current_health / enemy.max_health
                if enemy_health_ratio < 0.5:
                    enemy.get_damage("magic", self.low_health_damage, self.fight, origin="sa", originator=self.user, source="Last Caress")
                else:
                    enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Last Caress")
                self.fight.events.append(DummyEvent(0.5, (53, 27, 64), [enemy.my_cell]))
        self.user.move_to(self.new_cell, self.fight)


class Evelyn(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [200, 300, 400]
        self.sa_damage_below_50 = [600, 1200, 2000]
        self.sa_back_hexes = 3
        # to 3 closest enemies

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Roots the 3 closest enemies for 0.35 seconds,
        # after which deals 200 / 300 / 400 magic damage to
        # the 3 closest enemies and blinks back 3 hexes.
        # Damage is increased to 600 / 1200 / 2000 against enemies below 50% health
        self.channel(fight, 0.35, "Last Caress", interruptable=False)
        first_dir = fight.get_direction(self.pos, self.get_target(in_range).pos)
        area_ids = [(self.pos[0] + fight.map.dir_dict[first_dir][0], self.pos[1] + fight.map.dir_dict[first_dir][1]),
                    (self.pos[0] + fight.map.dir_dict[first_dir + 1][0],
                     self.pos[1] + fight.map.dir_dict[first_dir + 1][1]),
                    (self.pos[0] + fight.map.dir_dict[first_dir - 1][0],
                     self.pos[1] + fight.map.dir_dict[first_dir - 1][1])]
        enemies = []
        for id_ in area_ids:
            if fight.map.is_id_in_map(id_):
                cell = fight.map.get_cell_from_id(id_)
                enemy = fight.get_champ_from_cell(cell)
                if enemy:
                    enemy.root(0.35, fight.map)
                    enemies.append(enemy)

        port_dir = (first_dir + 3) % 6
        port_cell_id = self.my_cell.id
        for _ in range(3):
            id_ = port_cell_id[0] + fight.map.dir_dict[port_dir][0], port_cell_id[1] + fight.map.dir_dict[port_dir][1]
            if fight.map.get_cell_from_id(id_):
                port_cell_id = id_
        new_cell = fight.map.get_cell_from_id(port_cell_id)

        fight.aoe.append(LastCaress(fight, self, enemies, self.sa_damage[self.rank - 1], self.sa_damage_below_50[self.rank - 1], new_cell))


class Riposte(Aoe):
    def __init__(self, fight, user, damage,):
        super().__init__(fight, user, delay=1.5, user_needed=True)
        self.damage = damage

    def proc(self):
        if self.fight.now - self.created >= self.delay and self.user.alive:
            self.do_effect()
            self.activated = True

        if not self.user.alive:
            self.activated = True

    def do_effect(self):
        enemy = self.user.get_target(self.fight.adjacent_enemies(self.user))
        if enemy:
            enemy.stun(1.5, self.fight.map)
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Riposte")
            self.fight.events.append(DummyEvent(0.5, (191, 189, 191), [enemy.my_cell]))


class Fiora(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [100, 250, 400]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Enters a defensive stance for 1.5 seconds, becoming
        # immune to damage and enemy spell effects. Upon exiting the
        # stance, deals 100 / 250 / 400 magic damage to a nearby enemy
        # and Stun icon stuns them for 1.5 seconds.
        self.immune(1.5, fight)
        self.channel(fight, 1.5, "Riposte")
        fight.aoe.append(Riposte(fight, self, self.sa_damage[self.rank - 1]))


class Gangplank(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [150, 250, 350]
        self.barrels = []
        self.last_barrel = None

    def create_new_barrel(self):
        if self.last_barrel is None or self.fight.now - self.last_barrel >= 7000:
            self.last_barrel = self.fight.now
            enemies = self.get_enemies_in_range(self.fight, 3)
            if len(enemies) > 0:
                random_enemy = random.choice(enemies)
                pos_cell = random_enemy.my_cell
            else:
                pos_cell = self.my_cell
            self.barrels.append(pos_cell)

    def special_ability(self, fight, in_range, visible, alive, time):
        # Passive: Periodically places barrels near enemies.
        # Active: Shoots his barrels, causing them all to
        # explode in a chain reaction, dealing 150 / 250 / 350
        # magic damage to enemies caught in the blast and
        # applying on-hit effects.
        for barrel in self.barrels:
            cells = self.fight.map.get_all_cells_in_range(barrel, 2)
            self.fight.events.append(DummyEvent(0.5, (82, 57, 0), cells))
            for cell in cells:
                for enemy in self.fight.enemy_champs_alive(self):
                    if cell.id == enemy.pos:
                        # apply onhit
                        enemy.get_damage("magic", self.sa_damage[self.rank - 1], self.fight, origin="sa", originator=self, source="Powder Kegs")
                        self.do_onhit_damage(fight, enemy)
        self.barrels = []


class Judgement(Aoe):
    def __init__(self, fight, user, damage, interval, duration):
        super().__init__(fight, user, duration=duration, interval=interval, user_needed=True)
        self.damage = damage

    def proc(self):
        if self.fight.now - self.last_proc >= self.proc_interval and self.user.alive:
            self.last_proc = self.fight.now
            self.do_effect()

        if not self.user.alive or self.created - self.fight.now > self.duration:
            self.activated = True

    def do_effect(self):
        area = self.user.my_cell.neighbors
        self.fight.events.append(DummyEvent(0.5, (128, 128, 128), area))
        for enemy in self.fight.adjacent_enemies(self.user):
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Judgement")


class Garen(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [40, 65, 90]
        self.interval = 0.5

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Spins his sword for 4 seconds, becoming immune to
        # magic damage and dealing 40 / 65 / 90 magic damage to nearby
        # enemies each half-second. The spins can deal a total of
        # 360 / 585 / 810 magic damage.
        self.channel(fight, 4, "Judgement", False)
        self.status_effects.append(StatusEffect(fight.map, 4, "Judgement", effects=["immune_magic", "disarm"]))
        fight.aoe.append(Judgement(fight, self, self.sa_damage[self.rank - 1], 0.5, 4))


class Gnar(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
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
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_bonus_ad_damage = [0.05, 0.1, 0.15]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Passive: Basic attacks deal 5 / 10 / 15% AD bonus
        # physical damage and hit all enemies in a 60° 2-hex
        # cone, applying on-hit effects to all enemies hit.

    @property
    def can_use_sa(self):
        return False


class Jayce(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_stun_duration = [2.5, 4.25, 6]
        self.sa_damage = [200, 350, 500]
        self.as_hit_duration = [3, 5, 7]
        self.as_increase = [1, 3, 5]
        self.rank_on_use = None
        self.aa_counter_after_sa = None

    def special_ability(self, fight, in_range, visible, alive, time):
        self.aa_counter_after_sa = self.aa_counter
        self.rank_on_use = self.rank
        target = self.get_target(in_range)
        target.get_damage("magic", self.sa_damage[self.rank_on_use - 1], fight, origin="sa", originator=self, source="Mercury Cannon")
        fight.events.append(DummyEvent(self.sa_stun_duration[self.rank_on_use - 1] * 1000, (36, 36, 36), [target.my_cell]))
        target.stun(self.sa_stun_duration[self.rank - 1], fight.map)
        # @todo: add knockback for jayce

        # buffs
        buff_duration = 60
        range_effect = StatusEffect(fight.map, buff_duration, "Transform Mercury Cannon", effects=["range_buff_+1"])
        as_buff = StatusEffect(fight.map, buff_duration, "Transform Mercury Cannon", effects=["jayce_as_boost"])
        self.mana_lock(fight.map, buff_duration)
        for _ in range(3):
            self.status_effects.append(range_effect)
        self.status_effects.append(as_buff)

    def autoattack(self, time, fight, enemies_in_range, target_=None):
        super().autoattack(time, fight, enemies_in_range, target_=target_)
        if self.has_effect("jayce_as_boost"):
            if self.aa_counter_after_sa - self.aa_counter >= self.as_hit_duration[self.rank_on_use - 1]:
                effects = self.get_all_effects_with("jayce_as_boost")
                for effect in effects:
                    self.status_effects.remove(effect)

    @property
    def can_use_sa(self):
        if len(self.fight.adjacent_enemies(self)) > 0:
            return True
        else:
            return False

    @property
    def aa_cc(self):
        if self.has_effect("jayce_as_boost"):
            return 200
        else:
            return super().aa_cc


class Jinx(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
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

    def on_takedown(self):
        if self.takedown_counter == 1:
            self.bonus_aa_cc += self.base_aa_cc * self.sa_bonus_attack_speed[self.rank - 1]
        if self.takedown_counter == 2:
            self.status_effects.append(StatusEffect(self.fight.map, 999999999, "Get Excited", effects=["jinx_rocket_launcher"]))

    @property
    def can_use_sa(self):
        return False


class Kaisa(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_shield = [300, 600, 900]
        self.sa_bonus_attack_speed = [6, 12, 18]  # 5% per Stack -> 30%, 60%, 90%
        self.sa_duration = 3

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Dashes to the farthest away unit, gaining
        # a 300 / 600 / 900 damage shield and 30 / 60 / 90%
        # bonus attack speed for 3 seconds.
        new_cell = None
        target = fight.furthest_enemy_away(self)
        possible_positions = target.my_cell.neighbors
        while new_cell is None:
            for cell in possible_positions.copy():
                if not cell.taken:
                    new_cell = cell
                else:
                    for next_cell in cell.neighbors:
                        if next_cell not in possible_positions:
                            possible_positions.append(next_cell)
        self.move_to(new_cell, fight)
        self.shields.append(Shield(self, fight, fight.now, self.sa_shield[self.rank - 1], duration=3))
        for _ in range(self.sa_bonus_attack_speed[self.rank - 1]):
            self.status_effects.append(StatusEffect(fight.map, 3, "Killer Instinct", effects=["small_as_boost"]))


class Requiem(Aoe):
    def __init__(self, fight, user, damage, n_enemies):
        super().__init__(fight, user, delay=2.25, user_needed=True, interruptable=True)
        self.damage = damage
        self.n_enemies = n_enemies

    def proc(self):
        if self.fight.now - self.created >= self.delay and self.user.alive:
            self.do_effect()
            self.activated = True

        if not self.user.alive:
            self.activated = True

    def do_effect(self):
        enemies = self.fight.enemy_champs_alive(self.user)
        rnd_n_enemies = random.choices(enemies, k=min(len(enemies), self.n_enemies))
        for enemy in rnd_n_enemies:
            self.fight.events.append(DummyEvent(1, (64, 43, 69), [enemy.my_cell]))
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Requiem")


class Karthus(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [350, 600, 850]
        self.sa_channel_duration = 2.25
        self.sa_random_enemies = [5, 7, 9]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Channels for 2.25 seconds to deal
        # 350 / 600 / 850 magic damage to 5 / 7 / 9 random
        # enemies.
        self.channel(fight, 2.25, "Requiem", interruptable=True)
        fight.aoe.append(Requiem(fight, self, self.sa_damage[self.rank - 1], self.sa_random_enemies[self.rank - 1]))


class Kassadin(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_mana_reduce = [25, 50, 75]
        self.sa_shield_duration = 4

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Passive: Basic attacks reduce target's current
        # mana by 25 / 50 / 75, granting a shield for the
        # same amount lasting 4 seconds. The shield can stack.

    @property
    def can_use_sa(self):
        return False


class DeathLotus(Aoe):
    def __init__(self, fight, user, damage, area):
        super().__init__(fight, user, duration=2.5, effected_area=area, interval=(2.5 / 15), user_needed=True, interruptable=True)
        self.damage = damage

    def proc(self):
        if self.fight.now - self.created <= self.duration and self.user.alive:
            if self.last_proc is None or self.fight.now - self.last_proc >= self.proc_interval:
                self.last_proc = self.fight.now
                self.do_effect()
        else:
            self.activated = True

    def do_effect(self):
        for enemy in self._all_enemies_in_area(self.user):
            self.fight.events.append(DummyEvent((2.5 / 14), (64, 43, 69), [enemy.my_cell]))
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Death-Lotus")
            enemy.gwounds(3, self.fight, "Death-Lotus", self.user)


class Kataring(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_channel_duration = 2.5
        self.sa_enemies = [4, 6, 8]
        self.sa_tick_damage = [45, 70, 95]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Channels for 2.5 seconds, while throwing
        # 15 knives at 4 / 6 / 8 enemies within 2 hexes,
        # dealing 45 / 70 / 95 magic damage per tick and
        # applying Grievous Wounds icon Grievous Wounds,
        # reducing healing on them for 3 seconds. The channel
        # can deal a total of 675 / 1050 / 1425 magic damage.
        self.channel(fight, 2.5, "Death-Lotus", interruptable=True)
        area = fight.map.get_all_cells_in_range(self.my_cell, 2)
        self.fight.aoe.append(DeathLotus(fight, self, self.sa_tick_damage[self.rank - 1], area))


class Kayle(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_allies = [1, 2, 3]
        self.sa_duration = [2, 2.5, 3]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Targets the 1 / 2 / 3 weakest allies,
        # making them immune to damage for 2 / 2.5 / 3 seconds.
        protected_allies = []
        for allie in fight.allie_champs_alive(self):
            if len(protected_allies) < self.sa_allies[self.rank - 1]:
                protected_allies.append(allie)
            else:
                for p_allie in protected_allies:
                    if allie.current_health < p_allie.current_health:
                        protected_allies.remove(p_allie)
                        protected_allies.append(allie)
        for allie in protected_allies:
            allie.immune(self.sa_duration[self.rank - 1], fight)


class SlicingMaelstrom(Aoe):
    def __init__(self, fight, user, damage):
        super().__init__(fight, user, duration=3, interval=0.5, user_needed=True)
        self.damage = damage

    def proc(self):
        if self.fight.now - self.created <= self.duration and self.user.alive:
            if self.last_proc is None or self.fight.now - self.last_proc >= self.proc_interval:
                self.last_proc = self.fight.now
                self.do_effect()
        else:
            self.activated = True

    def do_effect(self):
        area = self.fight.map.get_all_cells_in_range(self.user.my_cell, 2)
        for enemy in self._all_enemies_in_area(area=area):
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Slicing Maelstrom")
            enemy.status_effects.append(StatusEffect(self.fight.map, 3, "Slicing Maelstrom", effects=["kennen_stack"]))
            if len(enemy.get_all_effects_with("kennen_stack")) == 3:
                enemy.remove_effects_with_name("Slicing Maelstrom")
                enemy.stun(1.5, self.fight.map)


class Kennen(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_duration = 3
        self.sa_damage_per_tick = [37.5, 75, 112.5]
        self.sa_stun_duration = 1.5

    def special_ability(self, fight, in_range, visible, alive, time):
        # Slicing Maelstrom
        # Active: Summons a storm around himself for 3 seconds,
        # dealing 37.5 / 75 / 112.5 magic damage each 0.5
        # seconds to enemies in the area. Each enemy struck 3
        # times is Stun icon stunned for 1.5 seconds.
        # The storm can deal a total of 225 / 450 / 675
        # magic damage.
        fight.aoe.append(SlicingMaelstrom(fight, self, self.sa_damage_per_tick[self.rank - 1]))


class Khazix(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [150, 250, 350]
        self.sa_damage_alone = [400, 600, 800]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Slashes the nearest enemy, dealing 150 / 250 / 350
        # magic damage to the target enemy.
        # If the enemy has no adjacent teammates, instead deals
        # 400 / 600 / 800 magic damage.
        target = self.get_target(in_range)
        if len(target.get_allies_around(fight)) == 0:
            damage = self.sa_damage_alone[self.rank - 1]
        else:
            damage = self.sa_damage[self.rank - 1]
        target.get_damage("magic", damage, fight, origin="sa", originator=self, source="Taste their Fear")
        fight.events.append(DummyEvent(1000, (36, 36, 36), [target.my_cell]))

    @property
    def can_use_sa(self):
        if len(self.fight.adjacent_enemies(self)) > 0:
            return True
        else:
            return False


class LambsRespite(Aoe):
    def __init__(self, fight, user, effected_area, duration, health):
        super().__init__(fight, user, duration=duration, effected_area=effected_area)
        self.health = health

    def proc(self):
        if self.fight.now - self.created <= self.duration:
            self.do_effect()
        else:
            self.activated = True

    def do_effect(self):
        for allie in self._all_allies_in_area():
            allie.status_effects.append(StatusEffect(self.fight.map, 0, "Lamb's Respite", effects=[f"kindred_{self.health}"]))


class Kindred(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_duration = [3, 4, 5]
        self.sa_health_drop = [300, 600, 900]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Creates a zone around themselves
        # for 3 / 4 / 5 seconds that prevents allies
        # within from dropping below 300 / 600 / 900
        # health or dying.
        area = fight.map.get_all_cells_in_range(self.my_cell, 2)
        fight.events.append(DummyEvent(int(self.sa_duration[self.rank - 1] * 1000), (168, 171, 0), area, type_="half_fade"))
        fight.aoe.append(LambsRespite(fight, self, area, self.sa_duration[self.rank - 1], self.sa_health_drop[self.rank - 1]))


class SolarFlare(Aoe):
    def __init__(self, fight, user, effected_area, damage, stun_duration, cell):
        super().__init__(fight, user, delay=0.625, effected_area=effected_area)
        self.damage = damage
        self.stun_duration = stun_duration
        self.center_cell = cell

    def proc(self):
        if self.fight.now - self.created >= self.delay:
            self.do_effect()
            self.activated = True
        else:
            self.activated = True

    def do_effect(self):
        self.fight.events.append(DummyEvent(500, (191, 121, 0), self.effected_area))
        for enemy in self._all_enemies_in_area():
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Solar Flare")
            if enemy.my_cell == self.center_cell:
                self.fight.events.append(DummyEvent(500, (112, 71, 0), [self.center_cell]))
                enemy.stun(self.stun_duration, self.fight.map)


class Leona(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [175, 250, 325]
        self.sa_stun_duration = [5, 7, 9]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: After a 0.625-second delay, calls down
        # a solar ray in a 3x3 area, dealing 175 / 250 / 325
        # magic damage to all enemies within and Stun icon
        # stunning the enemy in the center for 5 / 7 / 9
        # seconds.
        rnd_enemy = random.choice(fight.enemy_champs_alive(self))
        center_cell = rnd_enemy.my_cell
        area = fight.map.get_all_cells_in_range(center_cell, 2)
        fight.aoe.append(SolarFlare(fight, self, area, self.sa_damage[self.rank - 1], self.sa_stun_duration[self.rank - 1], center_cell))


class Lissandra(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [175, 325, 475]
        self.sa_stun_duration = 1.5
        self.sa_untargetable_duration = 2

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Encases an enemy in ice, Stun icon
        # stunning them for 1.5 seconds and dealing 175 / 325 / 475
        # magic damage to all enemies in the surrounding area.
        # If she is below 50% health, instead encases herself,
        # becoming untargetable for 2 seconds and dealing the
        # same magic damage to all enemies in the surrounding area.
        if self.current_health / self.max_health < 0.5:
            self.untargetable(2, fight)
            for cell in fight.map.get_all_cells_in_range(self.my_cell, 1):
                self.fight.events.append(DummyEvent(1000, (32, 48, 97), [cell]))
                for d_enemy in fight.enemy_champs_alive(self):
                    if cell.id == d_enemy.pos:
                        d_enemy.get_damage("magic", self.sa_damage[self.rank - 1], fight, origin="sa", originator=self, source="Frozen Tomb")
        else:
            enemy = self.get_target(in_range)
            enemy.stun(1.5, fight.map)
            for cell in fight.map.get_all_cells_in_range(enemy.my_cell, 1):
                self.fight.events.append(DummyEvent(1000, (32, 48, 97), [cell]))
                for d_enemy in fight.enemy_champs_alive(self):
                    if cell.id == d_enemy.pos:
                        d_enemy.get_damage("magic", self.sa_damage[self.rank - 1], fight, origin="sa", originator=self, source="Frozen Tomb")

    @property
    def can_use_sa(self):
        if self.current_health / self.max_health < 0.5:
            return True
        elif len(self.fight.champs_in_area(self.fight.map.get_all_cells_in_range(self.my_cell, 2), self.fight.enemy_champs_alive(self))) > 0:
            return True
        else:
            return False


class Lucian(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
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
            target.get_damage("magic", self.sa_damage[self.rank - 1], fight, origin="spell", originator=self)


class Lulu(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_bonus_health = [3, 4, 5]  # per stack 100 hp
        self.sa_bonus_health_duration = 6
        self.sa_knockup_duration = 1.25
        self.sa_allies = [1, 2, 3]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Grants 1 / 2 / 3 allies 300 / 400 / 500
        # bonus health for 6 seconds, Airborne icon knocking
        # up adjacent enemies near them for 1.25 seconds.
        allies = fight.allie_champs_alive(self)
        allies = random.choices(allies, k=min(len(allies), self.sa_allies[self.rank - 1]))
        health_gain_stacks = self.sa_bonus_health[self.rank - 1]
        for allie in allies:
            self.fight.events.append(DummyEvent(500, (104, 247, 164), [allie.my_cell]))
            for _ in range(health_gain_stacks):
                allie.status_effects.append(StatusEffect(fight.map, self.sa_bonus_health_duration, "Wild Growth", effects=["bonus_health_100"]))
            allie.heal(100 * health_gain_stacks, fight.map)
            for enemy in fight.adjacent_enemies(allie):
                self.fight.events.append(DummyEvent(1000, (18, 56, 34), [enemy.my_cell]))
                enemy.airborne(1.25, fight.map)


class BulletTime(Aoe):
    def __init__(self, fight, user, effected_area, damage):
        super().__init__(fight, user, duration=3, effected_area=effected_area, interval=(3 / 14), user_needed=True, interruptable=True)
        self.damage = damage

    def proc(self):
        if self.last_proc is None or (self.fight.now - self.created <= self.duration and self.fight.now - self.last_proc >= self.proc_interval):
            self.last_proc = self.fight.now
            self.do_effect()
        else:
            self.activated = True

    def do_effect(self):
        self.fight.events.append(DummyEvent(int(3 / 14 * 1000), (82, 65, 0), self.effected_area, type_="half_fade"))
        for enemy in self._all_enemies_in_area():
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Bullet Time")


class MissFortune(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_duration = 3
        self.sa_tick_damage = [1300 / 14, 2000 / 14, 2700 / 14]
        self.sa_tick_interval = 3 / 14

    @property
    def bullet_area(self):
        target = self.fight.furthest_enemy_away(self)
        direction = self.fight.get_direction(self.pos, target.pos)
        ids = []
        current_middle_id = self.pos
        for i in range(4):
            current_middle_id = (current_middle_id[0] + self.fight.map.dir_dict[direction][0], current_middle_id[1] + self.fight.map.dir_dict[direction][1])
            ids.append(current_middle_id)
            ids.append((current_middle_id[0] + self.fight.map.dir_dict[direction + 1][0], current_middle_id[1] + self.fight.map.dir_dict[direction + 1][1]))
            ids.append((current_middle_id[0] + self.fight.map.dir_dict[direction - 1][0], current_middle_id[1] + self.fight.map.dir_dict[direction - 1][1]))
        area = [self.fight.map.get_cell_from_id(id_) for id_ in ids]
        return area

    def special_ability(self, fight, in_range, visible, alive, time):
        # Bullet Time
        # Active: Channels and fires 14 waves of bullets in
        # a cone for 3 seconds, dealing a total of
        # 1300 / 2000 / 2700 magic damage to all enemies
        # within over the duration.
        self.channel(fight, 3, "Bullet Time", interruptable=True)
        fight.aoe.append(BulletTime(fight, self, self.bullet_area, self.sa_tick_damage[self.rank - 1]))


class Mordekaiser(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [250, 500, 750]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Slams his mace on two spaces in front of
        # him, dealing 250 / 500 / 750 magic damage to enemies
        # within.
        target = self.get_target(in_range)
        area = fight.get_ability_area(target, self, 2)
        self.fight.events.append(DummyEvent(700, (56, 71, 57), area))
        for enemy in fight.get_enemies_in_area(self, area):
            enemy.get_damage("magic", self.sa_damage[self.rank - 1], fight, origin="sa", originator=self, source="Obliterate")

    @property
    def can_use_sa(self):
        if len(self.get_enemies_in_range(self.fight, self.range)) > 0:
            return True
        else:
            return False


class SoulShackles(Aoe):
    def __init__(self, fight, user, damage, stun_duration):
        super().__init__(fight, user, delay=0.5, interval=3, user_needed=True)
        self.damage = damage
        self.stun_duration = stun_duration
        self.enemies = None

    def proc(self):
        if self.fight.now - self.created >= self.delay:
            self.do_effect()

        if not self.user.alive:
            self.activated = True

    def do_effect(self):
        if self.last_proc is None:
            self.last_proc = self.fight.now
            self.enemies = self.user.morgana_sa_range_enemies
            for enemy in self.enemies:
                self.fight.events.append(DummyEvent(500, (71, 56, 71), [enemy.my_cell]))
                enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Soul Shackles")
        elif self.fight.now - self.last_proc >= self.proc_interval:
            new_enemies = self.user.morgana_sa_range_enemies
            for enemy in self.enemies:
                if enemy in new_enemies:
                    self.fight.events.append(DummyEvent(1000, (71, 56, 71), [enemy.my_cell]))
                    enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Soul Shackles")
                    enemy.stun(self.stun_duration, self.fight.map)
            self.activated = True


class Morgana(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_delay = int(0.5 * 1000)
        self.sa_range = 3
        self.sa_damage = [175, 300, 425]
        self.sa_second_delay = 3
        self.sa_stun_duration = [2, 4, 6]  # damage again

    @property
    def morgana_sa_range_enemies(self):
        area = self.fight.map.get_all_cells_in_range(self.my_cell, 3)
        enemies = self.fight.get_enemies_in_area(self, area)
        return enemies

    def special_ability(self, fight, in_range, visible, alive, time):
        # Soul Shackles
        # Active: After a 0.5-second delay, fires chains to
        # nearby enemies up to 3 hexes away, dealing 175 / 300 / 425 magic damage.
        # After 3 seconds, all chained enemies still within her
        # range are Stun icon stunned for 2 / 4 / 6 seconds and take
        # the same magic damage.
        self.channel(fight, 0.5, "Soul Shackles")
        fight.aoe.append(SoulShackles(fight, self, self.sa_damage[self.rank - 1], self.sa_stun_duration[self.rank - 1]))


class PrimalSurge(Aoe):
    def __init__(self, fight, user, heal):
        super().__init__(fight, user, delay=0.5, duration=6, interval=0.5)
        self.heal_tick = heal
        self.allie = None

    def proc(self):
        if self.fight.now - self.created >= self.delay:
            self.do_effect()
        elif not self.user.alive:
            self.activated = True

    def nida_transform(self):
        self.user.status_effects.append(StatusEffect(self.fight.map, 60, "Primal Surge", effects=["melee"]))
        self.user.mana_lock(self.fight.map, 60)
        for _ in range(self.user.sa_cat_ad_bonus[self.user.rank - 1]):
            self.user.status_effects.append(StatusEffect(self.fight.map, 60, "Primal Surge", effects=["10_ad"]))

    def heal(self):
        if self.user.alive:
            self.user.heal(self.heal_tick, self.fight.map)
        if self.allie.alive:
            self.allie.heal(self.heal_tick, self.fight.map)
        self.last_proc = self.fight.now

    def do_effect(self):
        if self.last_proc is None:
            allies = sorted(self.fight.allie_champs_alive(self.user), key=lambda allie: allie.current_health)
            allies.reverse()
            self.allie = allies[0]
            self.fight.events.append(DummyEvent(500, (80, 219, 72), [self.user.my_cell, self.allie.my_cell]))
            self.heal()
            self.nida_transform()
        elif self.fight.now - self.last_proc >= self.proc_interval:
            self.heal()


class Nidalee(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_delay = 0.5
        self.sa_heal_duration = 6
        self.sa_heal_tick = [150 / (6*2), 375 / (6*2), 600 / (6*2)]
        self.sa_cat_duration = 60
        self.sa_cat_ad_bonus = [2, 7, 12]  # 10 per stack

    def special_ability(self, fight, in_range, visible, alive, time):
        # Primal Surge
        # Active: After a 0.5-second delay, heals herself and
        # the weakest ally over 6 seconds, healing them for
        # a total of 150 / 375 / 600 health, then transforms
        # to her Cat Form, becoming a Melee role melee attacker
        # for 60 seconds.
        # While in Cat Form, gains 20 / 70 / 120 attack damage.
        self.channel(fight, 0.5, "Primal Surge")
        fight.aoe.append(PrimalSurge(fight, self, self.sa_heal_tick[self.rank - 1]))


class Pantheon(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
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


class KeepersVerdict(Aoe):
    def __init__(self, user, fight, damage, stun_duration, n_enemies):
        super().__init__(fight, user, delay=0.75, user_needed=True)
        self.damage = damage
        self.stun_duration = stun_duration
        self.n_enemies = n_enemies
        self.n_counter = 0

    def proc(self):
        if self.fight.now - self.created >= self.delay and self.user.alive:
            self.do_effect()
            self.activated = True
        elif not self.user.alive:
            self.activated = True

    def do_effect(self):
        target = self.user.get_target(self.fight.adjacent_enemies(self.user))
        area = self.fight.get_ability_area(target, self.user, 12)
        cell_counter = -1
        while self.n_counter < self.n_enemies:
            cell_counter += 1
            current_cell = area[cell_counter]
            if current_cell is None:
                break
            else:
                self.fight.events.append(DummyEvent(500, (92, 92, 92), [current_cell], type_="half_fade"))
                for enemy in self.fight.enemy_champs_alive(self.user):
                    if current_cell.id == enemy.pos:
                        self.n_counter += 1
                        enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Keeper's Verdict")
                        enemy.stun(self.stun_duration, self.fight.map)
                        enemy.airborne(1, self.fight.map)


class Poppy(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_charge_duration = 0.75
        self.sa_enemies = [1, 2, 3]
        self.sa_damage = [300, 500, 700]
        self.sa_airborne_duration = 1
        self.sa_stun_duration = [2, 3, 4]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: After charging for 0.75 seconds, creates a
        # shockwave in a line that can hit up to 1 / 2 / 3
        # enemies, dealing 300 / 500 / 700 magic damage,
        # Airborne icon knocking up for 1 second and Stun icon
        # stunning them for 2 / 3 / 4 seconds.
        self.channel(fight, 0.75, "Keeper's Verdict")
        fight.aoe.append(KeepersVerdict(self, fight, self.sa_damage[self.rank - 1], self.sa_stun_duration[self.rank - 1], self.sa_enemies[self.rank - 1]))


class PhantomUndertow(Aoe):
    def __init__(self, fight, user, effected_area, damage, stun_duration):
        super().__init__(fight, user, delay=1, effected_area=effected_area, user_needed=True)
        self.damage = damage
        self.stun_duration = stun_duration

    def proc(self):
        if self.fight.now - self.created <= self.delay and self.user.alive:
            self.do_effect()
            self.activated = True
        elif not self.user.alive:
            self.activated = True

    def do_effect(self):
        self.fight.events.append(DummyEvent(500, (20, 64, 56), self.effected_area))
        for enemy in self._all_enemies_in_area():
            enemy.stun(self.stun_duration, self.fight.map)
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Phantom Undertow")


class Pyke(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_image_return = 1
        self.sa_damage = [150, 200, 250]
        self.sa_stun_duration = [1.5, 2, 2.5]

    def get_jump_cell(self):
        enemy = self.fight.furthest_enemy_away(self)
        direction = self.fight.get_direction(self.pos, enemy.pos)
        behind = (direction + 3) % 6
        cell = self.fight.map.get_cell_in_direction(enemy.my_cell, behind)
        if cell is None:
            cell = self.fight.map.get_cell_in_direction(enemy.my_cell, behind + 1)
            if cell is None:
                cell = self.fight.map.get_cell_in_direction(enemy.my_cell, behind - 1)
        return cell, enemy

    def special_ability(self, fight, in_range, visible, alive, time):
        # jumps to direction + 3 % 6  cell of furthest enemy
        # stuns and deals damage in line between them

        # Phantom Undertow
        # Active: Leaves an afterimage at his location,
        # then dashes behind the farthest enemy. After 1 second,
        # his afterimage returns to him, dealing 150 / 200 / 250
        # magic damage to all enemies it passes through and
        # and Stun icon stunning them for 1.5 / 2 / 2.5 seconds.
        jump_cell, enemy = self.get_jump_cell()
        area = fight.get_ability_area(enemy, self)
        self.move_to(jump_cell, fight)
        fight.aoe.append(PhantomUndertow(fight, self, area, self.sa_damage[self.rank - 1], self.sa_stun_duration[self.rank - 1]))


class Burrow(Aoe):
    def __init__(self, fight, user, damage, heal):
        super().__init__(fight, user, interval=1, user_needed=True)
        self.damage = damage
        self.heal = heal

    def proc(self):
        self.do_effect()
        if not self.user.alive:
            self.activated = True

    def do_effect(self):
        if self.last_proc is None:
            self.last_proc = self.fight.now
            self.user.heal(self.heal, self.fight.map)
        elif self.fight.now - self.last_proc >= self.proc_interval:
            self.activated = True
            # @todo: adjsut reksai target selection
            target = self.user.get_target(self.fight.enemy_champs_alive(self.user))
            new_cell = random.choice(target.my_cell.free_neighbors)
            self.user.move_to(new_cell, self.fight)
            self.fight.events.append(DummyEvent(500, (19, 7, 36), [target.my_cell]))
            target.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Burrow")
            target.airborne(1.75, self.fight.map)


class Reksai(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_untargetable_duration = 1
        self.sa_healing_per_half_second = [150, 300, 450]
        self.sa_damage = [200, 350, 500]
        self.sa_airborne_duration = 1.75

    def special_ability(self, fight, in_range, visible, alive, time):# Burrow
        # Active: Burrows, becoming untargetable for 1 second
        # while healing each 0.5 seconds for 150 / 300 / 450 health
        # in total. She then emerges at her target, dealing 200 / 350 / 500
        # magic damage and Airborne icon knocking them up for 1.75 seconds.
        self.untargetable(1, fight)
        fight.aoe.append(Burrow(fight, self, self.sa_damage[self.rank - 1], 2 * self.sa_healing_per_half_second[self.rank - 1]))


class Rengar(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_percent_ad_damage = [2, 3, 4]
        self.sa_duration = 6
        self.sa_crit_chance_increase = 0.25
        self.sa_attack_speed_bonus_total = [6, 10, 14]

    @property
    def weakest_enemies(self):
        enemies = sorted(self.fight.enemy_team_visible(self), key=lambda enemy: enemy.current_health)
        enemies.reverse()
        return enemies

    @property
    def jump_cell(self):
        for enemy in self.weakest_enemies:
            possible_jumps = enemy.my_cell.free_neighbors
            if len(possible_jumps) > 0:
                return random.choice(possible_jumps), enemy

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Leaps to and stabs the weakest enemy,
        # dealing 200 / 300 / 400% AD physical damage and applying
        # on-hit effects to his target. After this leap, for the next
        # 6 seconds, gains 25% critical strike chance and increases his
        # total attack speed by 30 / 50 / 70%.
        cell, enemy = self.jump_cell
        self.move_to(cell, fight)
        self.fight.events.append(DummyEvent(500, (64, 43, 11), [enemy.my_cell]))
        enemy.get_damage("physical", self.ad * self.sa_percent_ad_damage[self.rank - 1], fight, origin="sa", originator=self, source="Savagery")
        self.status_effects.append(StatusEffect(fight.map, 6, "Savagery", effects=["small_crit_chance_boost"]*5 + ["small_as_boost_total"]*self.sa_attack_speed_bonus_total[self.rank - 1]))


class GlacialPrison(Aoe):
    def __init__(self, fight, user, damage, stun_duration, enemy):
        super().__init__(fight, user, delay=2, user_needed=True)
        self.damage = damage
        self.stun_duration = stun_duration
        self.enemy = enemy

    def proc(self):
        if self.fight.now - self.created >= self.delay and self.user.alive:
            self.do_effect()
            self.activated = True
        elif not self.user.alive:
            self.activated = True

    def do_effect(self):
        for enemy in [self.enemy] + self.fight.adjacent_allies(self.enemy):
            self.fight.events.append(DummyEvent(500, (14, 15, 46), [enemy.my_cell]))
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Glacial Prison")
            enemy.stun(self.stun_duration, self.fight.map)


class Sejuani(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_delay = 2
        self.sa_damage = [100, 175, 250]
        self.sa_stun_duration = [2, 3.5, 5]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Glacial Prison
        # Active: After a 2 second delay, creates a glacial prison
        # on an enemy, dealing 100 / 175 / 250 magic damage to all
        # nearby enemies and Stun icon stunning them for 2 / 3.5 / 5 seconds.
        self.channel(fight, 2, "Glacial Prison")
        fight.aoe.append(GlacialPrison(self, fight,
                                       self.sa_damage[self.rank - 1], self.sa_stun_duration[self.rank - 1],
                                       random.choice(fight.enemy_team_visible(self))))


class SpiritsRefuge(Aoe):
    def __init__(self, fight, user, duration):
        super().__init__(fight, user, duration=duration, user_needed=True)

    def proc(self):
        if self.fight.now - self.created <= self.duration and self.user.alive:
            self.do_effect()
        else:
            self.activated = True

    def do_effect(self):
        area = [self.user.my_cell] + self.user.my_cell.neighbors
        self.fight.events.append(DummyEvent(100, (133, 130, 53), area, type_="half_fade"))
        effect = StatusEffect(self.fight.map, 0, "Spirit's Refuge", effects=["aa_dodge"])
        for allie in self.fight.adjacent_allies(self.user) + [self.user]:
            allie.status_effects.append(effect)


class Shen(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_duration = [3, 4, 5]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Creates a zone around himself that follows him
        # for 3 / 4 / 5 seconds, allowing allies inside to Blind
        # icon dodge all incoming basic attacks.
        fight.aoe.append(SpiritsRefuge(fight, self, self.sa_duration[self.rank - 1]))


class Shyvana(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
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


class Swain(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_duration = 6
        self.sa_damage = [40, 80, 120]
        self.interval = 0.5 * 1000
        self.sa_healing = [30, 60, 90]
        self.sa_end_damage = [300, 600, 900]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Transforms to his Demon Form for 6 seconds.
        # While in Demon Form, drains health from nearby enemies,
        # dealing 40 / 80 / 120 magic damage and healing himself
        # for 30 / 60 / 90 each 0.5 seconds for each enemy in range.
        # At the end of the transformation, sends out a Soul Flare,
        # dealing 300 / 600 / 900 magic damage to all nearby enemies.
        # In total, for each enemy, the drain can deal 480 / 960 / 1440
        # magic damage and heal for 360 / 720 / 1080 health.


class ExplosiveCharge(Aoe):
    def __init__(self, fight, user, damage, enemy):
        super().__init__(fight, user, delay=4)
        self.damage = damage
        if enemy in user.target_aa_counter:
            pass
        else:
            user.target_aa_counter[enemy] = 0
        self.start_counter = user.target_aa_counter[enemy]
        self.dict = user.target_aa_counter
        self.enemy = enemy

    @property
    def current_counter(self):
        return self.user.target_aa_counter[self.enemy] - self.start_counter

    def proc(self):
        if self.fight.now - self.created >= self.delay or self.current_counter == 4 or not self.enemy.alive:
            self.do_effect()
            self.activated = True

    def do_effect(self):
        damage = self.damage * 1.5**self.current_counter
        area = self.fight.map.get_all_cells_in_range(self.enemy.my_cell, 2)
        self.fight.events.append(DummyEvent(700, (77, 47, 11), area))
        for enemy in self._all_enemies_in_area(area=area):
            enemy.get_damage("magic", damage, self.fight, origin="sa", originator=self.user, source="Explosive Charge")


class Tristana(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_detonation_delay_time = 4
        self.sa_detonation_delay_aa = 3
        self.sa_damage = [70, 110, 150]
        self.sa_damage_increase_per_aa = 1.5

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Places a bomb on her current target that detonates
        # after 4 seconds or 3 basic attacks, dealing 70 / 110 / 150
        # magic damage to all nearby enemies within 2 hexes. The damage
        # is increased by 50% with each basic attack on the target,
        # dealing up to 175 / 275 / 375 magic damage.
        fight.aoe.append(ExplosiveCharge(fight, self, self.sa_damage[self.rank - 1], self.get_target(in_range)))

    @property
    def can_use_sa(self):
        if len(self.get_enemies_in_range(self.fight, self.range)) > 0:
            return True
        else:
            return False


class TwistedFate(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_aa_additional_damage = [150, 250, 350]
        self.sa_blue_mana = [30, 50, 70]
        self.sa_gold_stun_duration = [2, 3, 4]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: After a small delay, randomly selects one of three cards,
        # enhancing his next basic attack to deal 150 / 250 / 350 bonus
        # magic damage and apply an additional effect:
        #
        # Blue Card Blue Card: Restores 30 / 50 / 70 mana to himself and
        # adjacent allies.
        #
        # Red Card Red Card: Deals the same magic damage to enemies adjacent
        # to the target.
        #
        # Gold Card Gold Card: Stun icon Stuns the target
        # for 2 / 3 / 4 seconds.
        self.status_effects.append(StatusEffect(fight.map, 999999, "Pick a Card", effects=["random_card"]))


class PiercingArrow(Aoe):
    def __init__(self, fight, user, damage):
        super().__init__(fight, user, delay=1.5, user_needed=True, interruptable=True)
        self.damage = damage

    def proc(self):
        if self.fight.now - self.created >= self.delay and self.user.alive:
            self.do_effect()
            self.activated = True
        elif not self.user.alive:
            self.activated = True

    def do_effect(self):
        area = self.fight.get_ability_area(self.fight.furthest_enemy_away(self.user), self.user, 8)
        self.fight.events.append(DummyEvent(500, (44, 39, 51), area))
        for enemy in self._all_enemies_in_area(area=area):
            enemy.get_damage("magic", self.damage, self.fight, origin="sa", originator=self.user, source="Piercing Arrow")


class Varus(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_range = 8
        self.sa_damage = [300, 550, 800]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: After channeling for 1.5 seconds, fires a piercing
        # arrow up to 8 hexes away, dealing 300 / 550 / 800 magic damage
        # to all enemies in its path.
        self.channel(fight, 1.5, "Piercing Arrow", interruptable=True)
        fight.aoe.append(PiercingArrow(fight, self, self.sa_damage[self.rank - 1]))


class Vayne(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_third_stack_damage = [0.08, 0.12, 0.16]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Passive: Basic attacks apply a Silver Bolts stack.
        # Attacking a new enemy removes all her stacks from the
        # previous target.
        # The third stack consumes them all to deal 8 / 12 / 16%
        # of target's maximum health bonus true damage.

    @property
    def can_use_sa(self):
        return False


class Veigar(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [350, 650, 950]
        self.sa_damage_higher_level = 19999

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Blasts an enemy with magical energy,
        # dealing 350 / 650 / 950 magic damage to the target enemy.
        # If Veigar is a higher star level than his target, the
        # damage is increased to 19999.
        target = self.get_target(in_range)
        if self.rank > target.rank:
            damage = self.sa_damage_higher_level
        else:
            damage = self.sa_damage[self.rank - 1]
        target.get_damage("magic", damage, fight, origin="sa", originator=self, source="Primordial Burst")

    @property
    def can_use_sa(self):
        if len(self.get_enemies_in_range(self.fight, self.range)) > 0:
            return True
        else:
            return False


class Vi(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [300, 500, 700]
        self.sa_airborne = [2, 2.5, 3]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Charges at the farthest enemy, dealing 300 / 500 / 700
        # magic damage and Airborne icon knocking aside all enemies along
        # the way. Upon reaching her target, deals the same magic damage
        # and Airborne icon knocks them up for 2 / 2.5 / 3 seconds.


class Volibear(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_empower_duration = 20
        self.sa_chain_enemies = [2, 3, 4]
        self.sa_ad_percent_damage = [0.8, 0.9, 1]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Empowers his basic attacks for the next 20 seconds,
        # causing them to chain up to 2 / 3 / 4 enemies 1 hex away,
        # dealing 80 / 90 / 100% AD physical damage to secondary targets
        # and applying on-hit effects.


class Warwick(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_stun_duration = 1.5
        self.sa_strikes = 3
        self.sa_strike_damage = [150 / 3, 225 / 3, 300 / 3]

    def special_ability(self, fight, in_range, visible, alive, time):
        pass
        # Active: Pounces on the weakest enemy, Stun icon stunning them
        # for 1.5 seconds and striking them 3 times, dealing a total
        # of 150 / 225 / 300 magic damage. Each strike triggers on-hit
        # effects and heals for all the damage dealt.


class Yasuo(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [150, 350, 550]
        self.sa_tornado_airborne_duration = 1.5
        self.yasuo_stacks = 0

    def sword_damage(self, enemy):
        enemy.get_damage("magic", self.sa_damage[self.rank - 1], self.fight, origin="sa", originator=self, source="Steel Tempest")
        self.do_onhit_damage(self.fight, enemy)

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Stabs his sword into the two spaces in front of him,
        # dealing 150 / 350 / 550 magic damage and applying on-hit effects
        # to enemies within.
        # Every third cast, instead throws a tornado in a line that
        # travels 6 hexes, dealing the same magic damage and additionally
        # Airborne icon knocking enemies up for 1.5 seconds.
        self.yasuo_stacks += 1
        target = self.get_target(in_range)
        if self.yasuo_stacks == 3:
            self.yasuo_stacks = 0
            area = fight.get_ability_area(target, self, 6)
            self.fight.events.append(DummyEvent(500, (135, 132, 133), area))
            for enemy in fight.get_enemies_in_area(self, area):
                enemy.airborne(1.5, fight.map)
                self.sword_damage(enemy)
        else:
            area = fight.get_ability_area(target, self, 2)
            self.fight.events.append(DummyEvent(500, (135, 132, 133), area))
            for enemy in fight.get_enemies_in_area(self, area):
                self.sword_damage(enemy)

    @property
    def can_use_sa(self):
        if len(self.get_enemies_in_range(self.fight, self.range)) > 0:
            return True
        else:
            return False


class Zed(DummyChamp):
    def __init__(self, pos, champ_item, rank, fight, items=None):
        super().__init__(pos, champ_item, rank, fight, items=items)
        self.sa_damage = [200, 350, 500]

    def special_ability(self, fight, in_range, visible, alive, time):
        # Active: Throws a shuriken in a 4-hex line, dealing
        # 200 / 350 / 500 magic damage to all enemies in its path.
        target = self.get_target(in_range)
        area = fight.get_ability_area(target, self, 4)
        self.fight.events.append(DummyEvent(500, (56, 13, 29), area))
        for enemy in fight.get_enemies_in_area(self, area):
            enemy.get_damage("magic", self.sa_damage[self.rank - 1], fight, origin="sa", originator=self, source="Razor Shuriken")


class Golem(DummyChamp):
    # The Golem has 2200 health, 100 attack damage, and 40 armor.
    def __init__(self, pos, fight):
        golem_dict = {
            "range": 1,
            "hp": [2200, 2200, 2200],
            "dmg": [100, 100, 100],
            "atk_speed": 0.5,
            "mana": 0,
            "starting_mana": 0,
            "armor": 40,
            "mr": 0,
            "origin": "",
            "class": "",
        }
        super().__init__(pos, ["Golem", golem_dict], 1, fight, items=[])

    def special_ability(self, fight, in_range, visible, alive, time):
        pass

    @property
    def can_use_sa(self):
        return False
