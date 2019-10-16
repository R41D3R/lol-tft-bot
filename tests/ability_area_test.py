from fight_sim.champ_fabric import ChampionFabric
from fight_sim.fight import Fight

fabric = ChampionFabric()
fight = Fight(fabric)

target_dict = fabric._get_champ_item_from_name("Ahri")

target = fabric._get_champ((0,4), target_dict, 2, None)
champ = fabric._get_champ((7,3), target_dict, 2, None)
area = fight.get_line_area(target, champ, hexrange=3)
print([cell.id for cell in area])