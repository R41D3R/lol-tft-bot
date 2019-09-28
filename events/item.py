from abc import ABC, abstractmethod

# https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:Items
class Item(ABC):
    def __init__(self, item_stats):
        self.name = item_stats["name"]
        self.unique = item_stats["unique"]
        self.passiv = None
        self.attack_damage = item_stats["attack_damage"]
        self.attack_speed = item_stats["attack_speed"]
        self.ability_power = item_stats["ability_power"]
        self.starting_mana = item_stats["starting_mana"]
        self.armor = item_stats["armor"]
        self.magic_resistance = item_stats["magic_resistance"]
        self.health = item_stats["health"]

        self.passive = None  # event


