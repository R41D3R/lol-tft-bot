import requests

import pandas as pd
from bs4 import BeautifulSoup

# Starting Mana and Mana

mana_url = "https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:Champions#Stat%20List"
site = requests.get(mana_url)
mana_soup = BeautifulSoup(site.text, "html.parser")
table = mana_soup.find("div", title="Stat List")
c_rows = table.find_all("tr")
c_dict = {}
for row in c_rows[1:]:
    stats = row.find_all("td")
    name_split = stats[0].text.split()
    if len(name_split) == 1:
        name = name_split[0]
    else:
        name = name_split[0] + "-" + name_split[1]

    if name.split("'")[0] != name:
        name_list = name.split("'")
        name = name_list[0] + name_list[1].title()
        print(name)

    print(name)

    c_dict[name] = {"mana": stats[2].text.split()[0],
                    "starting_mana": stats[3].text.split()[0]}
df2 = pd.DataFrame(c_dict).transpose()


# rest of stats

main_url = "https://rankedboost.com/league-of-legends/teamfight-tactics/champion-stats/"
req = requests.get(main_url)
soup = BeautifulSoup(req.text, "html.parser")

names = ["name", "origin", "class", "cost", "hp", "dps", "atk_speed", "dmg", "range", "armor", "mr"]
file = "./champ_database.csv"

df = pd.DataFrame(columns=names)
df.set_index("name", inplace=True)

rows = soup.find_all("tr", class_="rb-build-overview-tr")
champs = []
for champ in rows:
    stats = champ.find_all("td")
    champ_stats = []
    for stat in stats:
        champ_stats.append(stat.text)
    champs.append(champ_stats)

# clean scraped champs
for champ in champs:
    champ[0] = champ[0][1:]
    champ[1] = champ[1][1:]
    if champ[1][-1] == " ":
        champ[1] = champ[1][:-1]
    champ[2] = champ[2][1:]
    if champ[2][-1] == " ":
        champ[2] = champ[2][:-1]
    champ[3] = champ[3][1:]
    champ[-3] = champ[-3][:1]

champs.append(["KaiSa", "Void", "Ranger Assassin", "5", "700 / 1260 / 2520", "69 / 124 / 248", "1.25", "55 / 99 / 198", "2", "20", "20"])
new_df = pd.DataFrame(champs, columns=names)
new_df.set_index("name", inplace=True)
df = df.append(new_df)
df.sort_index(inplace=True)

result = pd.concat([df, df2], axis=1, sort=True).reindex(df.index)

result.to_csv(file)
