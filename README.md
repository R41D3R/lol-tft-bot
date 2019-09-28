# lol-tft-bot

## Content
1. [Plan](#plan)
    * [Actions](#actions)
    * [Fight Simulaiton](#fight-simulation)
    * [Game Info](#game-info)
    * [Game Mechanics (Gym)](#Game-Mechanics-(Gym))
2. [Resourcen](#resourcen)
3. [Github Repos](#github-repos)

# Plan
### Actions
- [ ] Reroll
- [ ] Level Up
- [ ] Buy Champ
- [ ] Sell Champ
- [ ] *Select best Champ from Karusel (with Item)*
- [ ] Place Champs (Bank and Board)
- [ ] Ready for Fight

### Game Info
- [ ] Champs to buy
- [ ] Champs on Board + Champs in Bank => All Champs *(include Items, Rank,)*
- [ ] Karusel Champs with Items
- [ ] Items in Bank
- [ ] *Random View on enemys (Champs) each Round + Gold Pots, Level*
- [ ] Gold
- [ ] EXP
- [ ] Level (Max Champs)
- [ ] Health Bars from all Players
- [ ] Round counter
- [ ] Win Loose (from Health Bars or is there a option to get status with survived Champs)
- [ ] Win/ Loose Streek Counter
Do I need to include Champ Stats, Synergies ... ?

### Fight Simulation
- [x] Board with Cells (+ Neighbors)
- [x] Place Champs on Board 
- [x] Move to closest enemy
- [x] Autoattack if in Range
- [x] Defensive Stats
- [x] Add ranges >1
- [ ] smooth moving
- [x] Use Abylities if Mana is enough
- [x] Show damage numbers
- [x] Show Abilitys
- [ ] Merge DummyChamp with real one and get perfect game mechanic
- [ ] ADD 10 sample champs with real stats
- [ ] Add abilities for 10 sample champs
> Perfect Champ mechanic's til this
- [ ] ADD all Champs (Stats)
- [ ] ADD all Abilities to Champs
***
- [ ] Add 10 Test Items and give them champs
- [ ] Add Passive to Item
- [ ] Activate Item Passiv
- [ ] Show Items (activ/passiv)
> Items should work perfectly til here
- [ ] ADD all Items (Stats)
- [ ] ADD Passiv for all Items
***
- [ ] Get Sample Synergies
> Synergies should work properly
- [ ] ADD all Synergies (Origins and Classes)
***
- [ ] Update Database with Patchnotes
- [ ] Test Simulation with Game Info (Win Loose from Positions with all Variables(Champ, Item, Rank, ...)
- [ ] **finally** remove pygame and for HPC

### Game Mechanics (Gym)
- [ ] Reroll Probabilties (Max Champs in Pool vs Enemies + Level) -> Do perfect Probs. but Agent uses only Approximations
- [ ] *Karusel Probabilities*
- [ ] Drops (Items, Gold, Champs)
- [ ] *Wich Players get matched?*
- [ ] How much dmg does the winner on the opponent?


### Resourcen
* [Champion Mechanics](https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:Champions)
* [Rolling, Rounds, Database](https://tftactics.gg/db/rolling)
* [Champion Stats](https://rankedboost.com/league-of-legends/teamfight-tactics/akali/)
* [Patchnotes](https://leagueoflegends.fandom.com/wiki/Teamfight_Tactics:V9.18)


* [lolchess.gg - champs, items, meta, synergies](https://lolchess.gg/champions/blitzcrank) -> nicht aktuell
* [drop rates and other useful guides](https://www.rockpapershotgun.com/2019/08/02/teamfight-tactics-champions-hextech-new-tft-champions/#hextech)

### Github Repos
* [TFT Statistical Analysis](https://github.com/Strafos/TFT)
* [TFT Search for Synergies](https://github.com/deckar01/teamfight-tactics-synergy)
* [TFT Team Picker](https://github.com/timomak/TeamFightTactics-TeamPicker)
* [TFT Wiki Scraper](https://github.com/LNTech/TeamfightTactics_Simulator9)
* [TFT Bot (get and send actions)](https://github.com/ConnorWolanski/TeamFightTacticsBot)
* [TFT Champion Masking](https://github.com/tufanYavas/LoL-TFT-Champion-Masking)

