from abc import ABC, abstractmethod

# https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:Champions#Origin
class Champion(ABC):
    def __init__(self, base_stats):
        # base stats
        self.name = base_stats["name"]
        self.tier = base_stats["tier"]
        self.cost = base_stats["cost"]
        self.class_ = base_stats["class"]
        self.origin = base_stats["origin"]
        self.health = base_stats["health"]
        self.attack_damage = base_stats["attack_damage"]
        self.attack_speed = base_stats["attack_speed"]
        self.armor = base_stats["armor"]
        self.magic_resistance = base_stats["magic_resistance"]
        self.crit_chance = base_stats["crit_chance"]
        self.critical_strike_damage = base_stats["critical_strike_damage"]
        self.mana_ = base_stats["mana"]
        self.ability_mana = base_stats["ability_mana"]
        self.starting_mana = base_stats["starting_mana"]
        self.attack_range = base_stats["attack_range"]
        self.ability_power = base_stats["ability_power"]

        # events that occur
        self.events = []

        # items
        self.items = []

        # status effects
        self.banished = False
        self.grevious_wounds = False
        self.disarmed = False
        self.dodge = False
        self.stealth = False
        self.shrink_stacks = 0
        self.mana_lock = False
        self.stunned = False
        self.rooted = False
        self.airborned = False

    @abstractmethod
    def special_ability(self):
        pass

    # @todo: add attribute calculation for every item affected stat
    # def get_stat(self, stat, with_items):
    #     if with_items:
    #         return self.attack_speed +
    #     else:
    #         return self.attack_speed

    def check_events(self, trigger):
        for event in self.events:
            if trigger == event.trigger:
                event.activate(self)
