
class Item:
    def __init__(self, attribute, name):
        self.name = name
        self.attribute = attribute

    def get_attribute_counter(self, attribute):
        counter = 0
        for attr in self.attribute:
            if attr == attribute:
                counter += 1
        return counter


all_items = {
    0: {
        "name": "B.F. Sword",
        "attribute": ["ad"],
    },
    1: {
        "name": "Recursive Bow",
        "attribute": ["attack_speed"],
    },
    2: {
        "name": "Chain West",
        "attribute": ["armor"],
    },
    3: {
        "name": "Negatron Cloak",
        "attribute": ["mr"],
    },
    4: {
        "name": "Needlessly Large Rod",
        "attribute": ["ap"],
    },
    5: {
        "name": "Tear of the Goddess",
        "attribute": ["mana"],
    },
    6: {
        "name": "Giant's Belt",
        "attribute": ["health"],
    },
    7: {
        "name": "Spatula",
        "attribute": [],
    },
    8: {
        "name": "Sparring Gloves",
        "attribute": ["crit_chance", "dodge_chance"],
    },
    9: {
        "name": "Deathblade",
        "attribute": ["ad", "attack_speed"],
    },
    10: {
        "name": "Giant Slayer",
        "attribute": ["ad", "attack_speed"],
    },
    11: {
        "name": "Hextech Gunblade",
        "attribute": ["ad", "ap"],
    },
    12: {
        "name": "Spear of Shojin",
        "attribute": ["ad", "mana"],
    },
    13: {
        "name": "Guardian Angel",
        "attribute": ["ad", "armor"],
    },
    14: {
        "name": "Bloodthirster",
        "attribute": ["ad", "mr"],
    },
    15: {
        "name": "Zeke's Herald",
        "attribute": ["ad", "health"],
    },
    16: {
        "name": "Infinity Edge",
        "attribute": ["ad", "crit_chance", "crit_chance"],
    },
    17: {
        "name": "Youmuu's Ghostblade",
        "attribute": ["ad", "ad"],
    },
    18: {
        "name": "Rapidfire Cannon",
        "attribute": ["attack_speed", "attack_speed"],
    },
    19: {
        "name": "Guinsoo's Rageblade",
        "attribute": ["ap", "attack_speed"],
    },
    20: {
        "name": "Statikk Shiv",
        "attribute": ["mana", "attack_speed"],
    },
    21: {
        "name": "Phantom Dancer",
        "attribute": ["armor", "attack_speed"],
    },
    22: {
        "name": "Cursed Blade",
        "attribute": ["mr", "attack_speed"],
    },
    23: {
        "name": "Titanic Hydra",
        "attribute": ["health", "attack_speed"],
    },
    24: {
        "name": "Repeating Crossbow",
        "attribute": ["crit_chance", "crit_chance", "attack_speed"],
    },
    25: {
        "name": "Blade of the Ruined Kind",
        "attribute": ["attack_speed", "attack_speed"],
    },
    26: {
        "name": "Rabadon's Deathcap",
        "attribute": ["ap", "ap"],
    },
    27: {
        "name": "Luden's Echo",
        "attribute": ["mana", "ap"],
    },
    28: {
        "name": "Locket of the Iron Solari",
        "attribute": ["armor", "ap"],
    },
    29: {
        "name": "Ionic Spark",
        "attribute": ["mr", "ap"],
    },
    30: {
        "name": "Morellonomicon",
        "attribute": ["health", "ap"],
    },
    31: {
        "name": "Jeweled Gauntlet",
        "attribute": ["crit_chance", "crit_chance", "ap"],
    },
    32: {
        "name": "Yuumi",
        "attribute": ["ap", "ap"],
    },
    33: {
        "name": "Seraph's Embrace",
        "attribute": ["mana", "mana"],
    },
    34: {
        "name": "Frozen Heart",
        "attribute": ["mana", "armor"],
    },
    35: {
        "name": "Hush",
        "attribute": ["mana", "mr"],
    },
    36: {
        "name": "Redemption",
        "attribute": ["mana", "health"],
    },
    37: {
        "name": "Hand of Justice",
        "attribute": ["mana", "crit_chance", "dodge_chance"],
    },
    38: {
        "name": "Darkin",
        "attribute": ["mana", "mana"],
    },
    39: {
        "name": "Thormail",
        "attribute": ["armor", "armor"],
    },
    40: {
        "name": "Sword Breaker",
        "attribute": ["armor", "mr"],
    },
    41: {
        "name": "Red Buff",
        "attribute": ["armor", "health"],
    },
    42: {
        "name": "Iceborn Gauntlet",
        "attribute": ["armor", "dodge_chance", "dodge_chance"],
    },
    43: {
        "name": "Knight's Vow",
        "attribute": ["armor", "armor"],
    },
    44: {
        "name": "Dragons Claw",
        "attribute": ["mr", "mr"],
    },
    45: {
        "name": "Zephyr",
        "attribute": ["mr", "health"],
    },
    46: {
        "name": "Quicksilver",
        "attribute": ["mr", "dodge_chance", "dodge_chance"],
    },
    47: {
        "name": "Runaan's Hurrican",
        "attribute": ["mr", "mr"],
    },
    48: {
        "name": "Warmog's Armor",
        "attribute": ["health", "health"],
    },
    49: {
        "name": "Trap Claw",
        "attribute": ["health", "dodge_chance", "dodge_chance"],
    },
    50: {
        "name": "Trap Claw",
        "attribute": ["health", "dodge_chance", "dodge_chance"],
    },
    51: {
        "name": "Frozen Mallet",
        "attribute": ["health", "health"],
    },
    52: {
        "name": "Thief's Gloves",
        "attribute": ["crit_chance", "crit_chance", "dodge_chance", "dodge_chance"],
    },
    53: {
        "name": "Mittens",
        "attribute": ["crit_chance", "crit_chance", "dodge_chance", "dodge_chance"],
    },
    54: {
        "name": "Force of Nature",
        "attribute": [],
    },
}

