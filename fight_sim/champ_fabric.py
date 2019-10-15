import copy
import pandas as pd

from fight_sim.champ.champs import *
from fight_sim.config import logger
from fight_sim.item.item import Item
from fight_sim.data.items_base_stats import all_items


# @todo: Do checks before you place champs and assign champs + pos
# @body: Spatula items (only on non class, unique), valid champ position, number of champs, number of same champs, ...
class ChampionFabric:
    def __init__(self, test=False):
        self.possible_positions = [(x, y) for x in range(7) for y in range(3)]  # rows 0..2, cols 0..6
        file = "fight_sim/data/champ_database.csv"
        champs = pd.read_csv(file, index_col="name")
        self.champ_dict = champs.to_dict("index")
        self.base_top = None
        self.base_bot = None
        self.test = test

    def get_teams(self, reset=False):
        if self.base_bot is None and self.base_top is None:
            if not reset:
                self.base_top = self._get_team()
                self.base_bot = self._get_team()
        return copy.deepcopy(self.base_bot), copy.deepcopy(self.base_top)

    def get_real_team(self, champion_list_info):
        champs = []
        for champ in champion_list_info:
            items = [self._get_item_from_id(i) for i in champ[3]]
            champ_item = self._get_champ_item_from_name(champ[0])
            champs.append(self._get_champ(champ[1], champ_item, champ[2], None, items=items))
        print([champ.pos for champ in champs])
        return champs

    def _get_team(self, special_champ_name=None, special_item_id=None):
        logger.info("Team gets initialized.")
        k = 3
        k_picks = random.sample(list(self.champ_dict.items()), k)
        k_pos = random.sample(self.possible_positions, k)
        k_ranks = [random.choices([1, 2, 3], weights=[0.85, 0.1, 0.05])[0] for _ in range(k)]
        champs = [self._get_champ(pos, item, rank, None) for pos, item, rank in zip(k_pos, k_picks, k_ranks)]
        for champ in champs:
            print(champ.name)
        return champs

    def _get_champ_item_from_name(self, name):
        return name, self.champ_dict[name]

    @staticmethod
    def _get_item_from_id(id_):
        return [Item(all_items[id_]["attribute"], all_items[id_]["name"])]

    @staticmethod
    def _get_items():
        items = []
        n_items = random.choices([0, 1, 2, 3], weights=[0.5, 0.3, 0.1, 0.1])[0]
        for i in range(n_items):
            random_item = random.choice(list(all_items.items()))
            items.append(Item(random_item[1]["attribute"], random_item[1]["name"]))
        return items

    def _get_champ(self, pos, champ_item, rank, fight, items=None):
        if items is None:
            items = self._get_items()
        if champ_item[0] == "Aatrox":
            return Aatrox(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Ahri":
            return Ahri(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Akali":
            return Akali(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Anivia":
            return Anivia(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Ashe":
            return Ashe(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Aurelion-Sol":
            return AurelionSol(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Blitzcrank":
            return Blitzcrank(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Brand":
            return Brand(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Braum":
            return Braum(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Camille":
            return Camille(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "ChoGath":
            return ChoGath(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Darius":
            return Darius(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Draven":
            return Draven(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Elise":
            return Elise(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Evelynn":
            return Evelyn(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Fiora":
            return Fiora(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Gangplank":
            return Gangplank(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Garen":
            return Garen(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Gnar":
            return Gnar(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Graves":
            return Graves(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Jayce":
            return Jayce(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Jinx":
            return Jinx(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "KaiSa":
            return Kaisa(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Karthus":
            return Karthus(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Kassadin":
            return Kassadin(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Katarina":
            return Kataring(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Kayle":
            return Kayle(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Kennen":
            return Kennen(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "KhaZix":
            return Khazix(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Kindred":
            return Kindred(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Leona":
            return Leona(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Lissandra":
            return Lissandra(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Lucian":
            return Lucian(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Lulu":
            return Lulu(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Miss-Fortune":  # check name
            return MissFortune(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Mordekaiser":  # check name
            return Mordekaiser(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Morgana":  # check name
            return Morgana(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Nidalee":  # check name
            return Nidalee(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Pantheon":  # check name
            return Pantheon(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Poppy":  # check name
            return Poppy(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Pyke":  # check name
            return Pyke(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "RekSai":  # check name
            return Reksai(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Rengar":  # check name
            return Rengar(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Sejuani":  # check name
            return Sejuani(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Shen":  # check name
            return Shen(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Shyvana":  # check name
            return Shyvana(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Swain":  # check name
            return Swain(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Tristana":  # check name
            return Tristana(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Twisted-Fate":  # check name
            return TwistedFate(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Varus":  # check name
            return Varus(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Vayne":  # check name
            return Vayne(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Veigar":  # check name
            return Veigar(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Vi":  # check name
            return Vi(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Volibear":  # check name
            return Volibear(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Warwick":  # check name
            return Warwick(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Yasuo":  # check name
            return Yasuo(pos, champ_item, rank, fight, items=items)
        if champ_item[0] == "Zed":  # check name
            return Zed(pos, champ_item, rank, fight, items=items)
        print(champ_item[0])
