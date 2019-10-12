# Fight Simulation

## Get started
* run `./fight/data/champ_base_stats_scraper.py` to scrape champion base stats
* run the `./fight/main.py` to test the fight (visually)
***
![image](https://drive.google.com/uc?export=view&id=1nc-A5zWH-M1DJtQDtXCaNKJhQ8obSlLo)
***
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
| Gangplank | yes | yes |
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
| Statikk Shiv | yes | yes |
| Phantom Dancer | yes | yes |
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
| Quicksilver | yes | yes |
| Runaan's Hurrican | yes | need more info on item interaction |
| Warmog's Armor | yes | yes |
| Trap Claw | yes | yes |
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
| Wild | yes |
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
