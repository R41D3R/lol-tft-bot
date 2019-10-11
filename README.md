# lol-tft-bot


### Get started
* Download [PyCharm](https://www.jetbrains.com/pycharm/) or other IDE

***
* clone repository
* `pip install pygame` or `pip install -r requirements.txt`
* install `beautifulsoup4`, `requests` and `pandas` if they are not already installed
* run `champ_base_stats.py` to scrape champion base stats
* run the `main.py` to test the fight (visually)
***
* if you have questions about the game that can't be solved on your own fell free to create a card in the [Trello board](https://trello.com/b/PiM2IKjo/team-fight-tactics-fragen) ([invite Link](https://trello.com/invite/b/PiM2IKjo/81dc0be800a58f3bba8084d4e450206a/team-fight-tactics-fragen), you can invite friends that want to contribute with their knowledge)

* The Project can split in mostly independent parts:
    1. Fight Simulation
    2. Game Enviroment (Fight Simulation + game mechanics)
    3. Client Interaction (Input and Retrieval) 
    4. Reinforcement Learning Part
    
    While i. and ii. are closely related, iii. can be written independently but is in fact needed for getting tests for the simulation.
    
    TLDR: simulation + client retrival in *parallel* &#8594; game env &#8594; RL &#8594; client input  

## Content
1. [Plan](#plan)
    * [Fight Simulaiton](#fight-simulation)
    * [Game Mechanics (Gym)](#Game-Mechanics-(Gym))
    * [Game Info](#game-info)
    * [Actions](#actions-in-game)
2. [Resourcen](#resourcen)
3. [Github Repos](#github-repos)

## Plan
### Fight Simulation
- [x] Board with Cells (+ Neighbors)
- [x] Place Champs on Board 
- [x] Move to closest enemy
- [x] Autoattack if in Range
- [x] Defensive Stats
- [x] Add ranges >1
- [x] smooth moving
- [x] Use Abilities if Mana is enough
- [x] Show damage numbers
- [x] Show Abilities
- [x] ADD 10 sample champs with real stats
- [x] Improve Damage Reduction (Mr and Armor)
> Perfect Champ mechanic's til this
- [x] ADD all Champs (Stats)
- [ ] ADD all Abilities to Champs (41/57, not tested)
- [ ] ADD NPC like champ (spiders, golem, enemy quest npc's)

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;www.draw.io\&quot; modified=\&quot;2019-10-11T14:11:16.564Z\&quot; agent=\&quot;Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0\&quot; etag=\&quot;9nNGF5x1tpQl2ZAKuy4S\&quot; version=\&quot;12.1.0\&quot; type=\&quot;google\&quot; pages=\&quot;1\&quot;&gt;&lt;diagram id=\&quot;ExYBfqPelXIVMq3trY13\&quot; name=\&quot;Page-1\&quot;&gt;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&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
<script type="text/javascript" src="https://www.draw.io/js/viewer.min.js"></script>

<table>
<tr><td>

| Name | Stats | Ability |
| ---- | ----- | ------- |
| Aatrox | yes | yes |
| Ahri | yes | yes |
| Akali | yes | yes |
| Anivia | yes | yes |
| Ashe | yes | yes |
| Aurelion | yes | yes |
| Blitzcrank | yes | yes |
| Brand | yes | yes |
| Braum | yes | missles + direction? |
| Camille | yes | yes |
| ChoGath | yes | yes |
| Darius | yes | yes |
| Draven | yes | yes |
| Elise | yes | yes |
| Evelynn | yes | yes |
| Fiora | yes | yes |
| Gangplank | yes | split on-hit and aa first |
| Garen | yes | old |
| Gnar | yes | no |
| Graves | yes | no |



</td><td>

| Name | Stats | Ability |
| ---- | ----- | ------- |
| Jayce | yes | old |
| Jinx | yes | yes |
| Kaisa | yes | yes |
| Karthus | yes | yes |
| Kassadin | yes | yes |
| Kararina | yes | yes |
| Kayle | yes | yes |
| Kennen | yes | yes |
| Khazix | yes | yes |
| Kindred | yes | yes |
| Leona | yes | yes |
| Lissandra | yes | implement untargetable first |
| Lucian | yes | old |
| Lulu | yes | yes |
| Miss Fortune | yes | yes |
| Mordekaiser | yes | yes |
| Morgana | yes | no |
| Nidalee | yes | no |
| Pantheon | yes | no |
| Poppy | yes | yes |


</td>
<td>

| Name | Stats | Ability |
| ---- | ----- | ------- |
| Pyke | yes | yes |
| Reksai | yes | untargetable first |
| Rengar | yes | yes |
| Sejuani | yes | yes |
| Shen | yes | yes |
| Shyvana | yes | no |
| Swain | yes | no |
| Tristana | yes | yes |
| Twisted Fate | yes | yes |
| Varus | yes | yes |
| Vayne | yes | yes |
| Veigar | yes | yes |
| Vi | yes | no |
| Volibear | yes | no |
| Warwick | yes | no |
| Yasuo | yes | yes |
| Zed | yes | yes |


</td></tr>
</table>

- [x] ADD Status Effect to Champs
    * Effect List
    - [x] Mana-lock
    - [x] banish
    - [x] grievous wounds
    - [x] disarm
    - [x] stealth
    - [x] shrink
    - [x] Stun
    - [x] Root
    - [x] Airborne
- [x] Add displacement (Airborne, Knockback)
***
- [x] Add Base Items
- [x] Add all items (stats)
- [x] Add Passive to Item
- [x] Show Items
- [ ] Show Item Effects (Visual)


<table>
<tr>
<td>

| Name | Stats | Effect |
| ---- | ----- | ------- |
| B.F. Sword | yes | None |
| Recursive Bow | yes | None |
| Chain West | yes | None |
| Negatron Cloak | yes | None |
| Needlessly Large Rod | yes | None |
| Tear of the Goddess | yes | None |
| Giant's Belt | yes | None |
| Spatula | yes | None |
| Sparring Gloves | yes | None |
| Deathblade | yes | yes |
| Giant Slayer | yes | yes |
| Hextech Gunblade | yes | yes |
| Spear of Shojin | yes | yes |
| Guardian Angel | yes | yes |
| Bloodthirster | yes | yes |
| Zeke's Herald | yes | yes |
| Infinity Edge | yes | yes |
| Youmuu's Ghostblade | yes | yes |
| Rapidfire Cannon | yes | yes |
| Guinsoo's Rageblade | yes | yes |
| Statikk Shiv | yes | need more info |
| Phantom Dancer | yes | need more info |
| Cursed Blade | yes | yes |
| Titanic Hydra | yes | yes |
| Repeating Crossbow | yes | yes |
| Blade of the Ruined Kind | yes | yes |
| Rabadon's Deathcap | yes | yes |

</td><td>

| Name | Stats | Effect |
| ---- | ----- | ------- |
| Luden' Echo | yes | yes |
| Locket of the Iron Solari | yes | yes |
| Ionic Spark | yes | yes |
| Morellonomicon | yes | yes |
| Jeweled Gauntlet | yes | yes |
| Yuumi | yes | yes |
| Seraph's Embrace | yes | yes |
| Frozen Heart | yes | yes |
| Hush | yes | yes |
| Redemption | yes | implement aoe first |
| Hand of Justice | yes | need more info (heal part done) |
| Darkin | yes | yes |
| Thormail | yes | yes |
| Sword Breaker | yes | yes |
| Red Buff | yes | yes |
| Iceborn Gauntlet | yes | first implement Aoe |
| Knight's Vow | yes | yes |
| Dragons Claw | yes | yes |
| Zephyr | yes | yes |
| Quicksilver | yes | need to refactor to dummy.get_cc() |
| Runaan's Hurrican | yes | need more info on item interaction |
| Warmog's Armor | yes | yes |
| Trap Claw | yes | need to refactor to dummy.get_cc() |
| Frozen Mallet | yes | yes |
| Thief's Gloves | yes | need tier list first |
| Mittens | yes | yes |
| Force of Nature | yes | implemented in game env |
</td>
</tr>
</table>

***
- [ ] ADD all Synergies 20/24
- [x] Show Synergies
<table><tr>
<td>

| Origin | Implemented | 
| ---- | ----- | 
| Demon | yes |
| Dragon | yes |
| Exile | yes |
| Glacial | yes |
| Hextech | yes |
| Imperial | refactor to deal damage |
| Ninja | yes |
| Noble | yes |
| Phantom | yes |
| Pirate | implemented in game env |
| Robot | yes |
| Void | yes |
| Wild | implement undodgeable aa |
| Yordle | yes |
</td><td>

| Class | Implemented |
| ---- | ----- |
| Assasin | yes |
| Blademaster | yes |
| Brawler | yes |
| Elementalist | implement golem + summon |
| Guardian | yes |
| Gunslinger | yes |
| Knight | yes |
| Ranger | yes |
| Shapeshifter | yes |
| Sorcerer | yes |
</td>
</tr>
</table>

***
- [ ] Does Pathfinding work properly?
- [ ] Update Database with Patchnotes
- [ ] Test Simulation with Game Info (Win Loose from Positions with all Variables(Champ, Item, Rank, ...)
- [ ] **finally** remove pygame for HPC

### Game Mechanics (Gym)
- [ ] Reroll Probabilities (Max Champs in Pool vs Enemies + Level) -> Do perfect Probs. but Agent uses only Approximations
- [ ] *Karusel Probabilities*
- [ ] Drops (Items, Gold, Champs)
- [ ] *Which Players get matched?*
- [ ] How much dmg does the winner on the opponent? [Link](https://lolchess.gg/guide/damage)
> same from in game actions
- [ ] Reroll
- [ ] Level Up
- [ ] Buy Champ
- [ ] Sell Champ
- [ ] *Select best Champ from Karussell (with Item)*
- [ ] Place Champs (Bank and Board)
- [ ] Ready for Fight
> same from game info
- [ ] Champs to buy
- [ ] Champs on Board + Champs in Bank => All Champs *(include Items, Rank,)*
- [ ] Karusel Champs with Items
- [ ] Items in Bank
- [ ] *Random View on enemies (Champs) each Round + Gold Pots, Level*
- [ ] Gold
- [ ] EXP
- [ ] Level (Max Champs)
- [ ] Health Bars from all Players
- [ ] Round counter
- [ ] Win Loose (from Health Bars or is there a option to get status with survived Champs)
- [ ] Win/ Loose Streak Counter
Do I need to include Champ Stats, Synergies ... ?

### Game Info
- [ ] Champs to buy
- [ ] Champs on Board + Champs in Bank => All Champs *(include Items, Rank,)*
- [ ] Karusel Champs with Items
- [ ] Items in Bank
- [ ] *Random View on enemies (Champs) each Round + Gold Pots, Level*
- [ ] Gold
- [ ] EXP
- [ ] Level (Max Champs)
- [ ] Health Bars from all Players
- [ ] Round counter
- [ ] Win Loose (from Health Bars or is there a option to get status with survived Champs)
- [ ] Win/ Loose Streak Counter
Do I need to include Champ Stats, Synergies ... ?

### Actions in Game
- [ ] Reroll
- [ ] Level Up
- [ ] Buy Champ
- [ ] Sell Champ
- [ ] *Select best Champ from Karusel (with Item)*
- [ ] Place Champs (Bank and Board)
- [ ] Ready for Fight


### Resourcen
**Other Stuff**
* [Coordinate System](https://www.redblobgames.com/grids/hexagons/#coordinates)
* [PyGame Primer](https://realpython.com/pygame-a-primer/)
* [PyGame Drawing](https://sites.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/)
* [Beatiful Soap First Steps](https://riptutorial.com/de/beautifulsoup)
* [Automate basic tasks in games](https://www.tautvidas.com/blog/2018/02/automating-basic-tasks-in-games-with-opencv-and-python/)

**TFT**
* [Champion Mechanics (__best site__)](https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:Champions)
* [Rolling, Rounds, Database](https://tftactics.gg/db/rolling)
* [Champion Stats](https://rankedboost.com/league-of-legends/teamfight-tactics/akali/)
* [Patchnotes](https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:V9.18)

> old
* [lolchess.gg - champs, items, meta, synergies](https://lolchess.gg/champions/blitzcrank) -> nicht aktuell
* [drop rates and other useful guides](https://www.rockpapershotgun.com/2019/08/02/teamfight-tactics-champions-hextech-new-tft-champions/#hextech)

### Github Repos
* [TFT Statistical Analysis](https://github.com/Strafos/TFT)
* [TFT Search for Synergies](https://github.com/deckar01/teamfight-tactics-synergy)
* [TFT Team Picker](https://github.com/timomak/TeamFightTactics-TeamPicker)
* [TFT Wiki Scraper](https://github.com/LNTech/TeamfightTactics_Simulator9)
* [TFT Bot (get and send actions)](https://github.com/ConnorWolanski/TeamFightTacticsBot)
* [TFT Champion Masking](https://github.com/tufanYavas/LoL-TFT-Champion-Masking)

