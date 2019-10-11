# Teamfight Tactics Bot
> This project aims to build a fully automated Teamfight Tactics Bot

## Get started
* Download [PyCharm](https://www.jetbrains.com/pycharm/) or other IDE
* install the latest Anaconda version or any other python 3.7 version
***
* clone repository
* `pip install -r requirements.txt`
***
* if you have questions about the game that can't be solved on your own fell free to create a card in the [Trello board](https://trello.com/b/PiM2IKjo/team-fight-tactics-fragen) ([invite Link](https://trello.com/invite/b/PiM2IKjo/81dc0be800a58f3bba8084d4e450206a/team-fight-tactics-fragen), you can invite friends that want to contribute with their knowledge)

* The Project can split in mostly independent parts:
    1. Fight Simulation
    2. Game Enviroment (Fight Simulation + game mechanics)
    3. Client Interaction (Input and Retrieval) 
    4. Reinforcement Learning Part
    
    While i. and ii. are closely related, iii. can be written independently but is in fact needed for getting tests for the simulation.
    
    TLDR: simulation + client retrival in *parallel* &#8594; game env &#8594; RL &#8594; client input  


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

