import requests

import pandas as pd
from bs4 import BeautifulSoup


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

champs.append(["Kaisa", "Void", "Ranger Assassin", "5", "700 / 1260 / 2520", "69 / 124 / 248", "1.25", "55 / 99 / 198", "2", "20", "20"])
new_df = pd.DataFrame(champs, columns=names)
new_df.set_index("name", inplace=True)
df = df.append(new_df)

df.to_csv(file)

