
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


items = {
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
    }
}
