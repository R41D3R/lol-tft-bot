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
- [ ] Add abilities for 10 sample champs (3/10)
> Perfect Champ mechanic's til this
- [x] ADD all Champs (Stats)
- [ ] ADD all Abilities to Champs
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
- [ ] Add all items (stats)
- [ ] Add Passive to Item
- [ ] Activate Item Passive
- [ ] Show Items (active/passive)
> Items should work perfectly til here
- [ ] ADD all Items (Stats)
- [ ] ADD Passive for all Items
***
- [ ] Get Sample Synergies
> Synergies should work properly
- [ ] ADD all Synergies (Origins and Classes)
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

