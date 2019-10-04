# lol-tft-bot

## Content
1. [Plan](#plan)
    *  :on: [Fight Simulaiton](#fight-simulation)
    *  :soon: [Game Mechanics (Gym)](#Game-Mechanics-(Gym))
    *  :soon: [Game Info](#game-info)
    *  :soon: [Actions](#actions-in-game)
2. [Resourcen](#resourcen)
3. [Github Repos](#github-repos)

> [Emoji List](https://www.webfx.com/tools/emoji-cheat-sheet/)

# Plan
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
- [ ] ADD all Champs (Stats)
- [ ] ADD all Abilities to Champs
- [ ] ADD NPC like champ (spiders, golem, enemy quest npc's)

<table>
<tr><td>

| Name | Stats | Ability |
| ---- | ----- | ------- |
| Aatrox | no | no |
| Ahri | no | no
| Akali | no | no |
| Anivia | no | no |
| Ashe | no | no |
| Aurelion | no | no |
| Blitzcrank | no | no |
| Brand | no | no |
| Braum | no | no |
| Camille | no | no |
| ChoGath | no | no |
| Darius | no | no |
| Draven | no | no |
| Elise | no | no |
| Evelynn | no | no |
| Fiora | no | no |
| Gangplank | no | no |
| Garen | no | no |
| Gnar | no | no |
| Graves | no | no |



</td><td>

| Name | Stats | Ability |
| ---- | ----- | ------- |
| Jayce | no | no |
| Jinx | no | no |
| Kaisa | no | no |
| Karthus | no | no |
| Kassadin | no | no |
| Kararina | no | no |
| Kayle | no | no |
| Kennen | no | no |
| Khazix | no | no |
| Leona | no | no |
| Lissandra | no | no |
| Lucian | no | no |
| Lulu | no | no |
| Miss Fortune | no | no |
| Mordekaiser | no | no |
| Morgana | no | no |
| Nidalee | no | no |
| Pantheon | no | no |
| Poppy | no | no |


</td>
<td>

| Name | Stats | Ability |
| ---- | ----- | ------- |
| Pyke | no | no |
| Reksai | no | no |
| Rengar | no | no |
| Sejuani | no | no |
| Shen | no | no |
| Shyvana | no | no |
| Swain | no | no |
| Tristana | no | no |
| Twisted Fate | no | no |
| Varus | no | no |
| Vayne | no | no |
| Veigar | no | no |
| Vi | no | no |
| Volibear | no | no |
| Warwick | no | no |
| Yasuo | no | no |
| Zed | no | no |


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
- [ ] Add displacement (Airborne, Knockback)
***
> dont forget to add status effect mechanics when implementing
- [x] Add Base Items
- [x] Add all items (stats)
- [ ] Add Passive to Item
- [x] Show Items
- [ ] Show Item Effects


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
| Infinity Edge | yes | no |
| Youmuu's Ghostblade | yes | yes |
| Rapidfire Cannon | yes | yes |
| Guinsoo's Rageblade | yes | yes |
| Statikk Shiv | yes | need more info |
| Phantom Dancer | yes | need more info |
| Cursed Blade | yes | need shrink effect first |
| Titanic Hydra | yes | yes |
| Repeating Crossbow | yes | insert fight first in get_damage |
| Blade of the Ruined Kind | yes | yes |
| Rabadon's Deathcap | yes | yes |

</td><td>

| Name | Stats | Effect |
| ---- | ----- | ------- |
| Luden' Echo | yes | insert fight first in get_damage |
| Locket of the Iron Solari | yes | implement shield_effect first |
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
| Zephyr | yes | need mirror position info |
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

- [ ] Add Passive to Item
- [ ] Activate Item Passive
- [ ] Show Items (active/passive)
> Items should work perfectly til here
- [ ] ADD all Items (Stats)
- [ ] ADD Passive for all Items
***
- [ ] ADD all Synergies (Origins and Classes)
- [ ] Show Synergies
<table><tr>
<td>

| Origin | Implemented | 
| ---- | ----- | 
| Demon | no |
| Dragon | no |
| Exile | no |
| Glacial | no |
| Hextech | no |
| Imperial | no |
| Ninja | no |
| Noble | no |
| Phantom | no |
| Pirate | no |
| Robot | no |
| Void | no |
| Wild | no |
| Yordle | no |
</td><td>

| Class | Implemented |
| ---- | ----- |
| Assasin | no |
| Blademaster | no |
| Brawler | no |
| Elementalist | no |
| Guardian | no |
| Gunslinger | no |
| Knight | no |
| Ranger | no |
| Shapeshifter | no |
| Sorcerer | no |
</td>
</tr>
</table>
> Synergies should work properly
***
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
* [Champion Mechanics](https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:Champions)
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

