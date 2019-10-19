# Enviroment
> Tournament Enviroment. Recieves states and return simulated results.
### Research needed
- [ ] Reroll Probabilities
- [ ] Karusel Probabilities
- [ ] Drops (Items, Gold, Champs) -> which item drops
- [ ] How much dmg does the winner on the opponent? [Link](https://lolchess.gg/guide/damage)
- [ ] Number of champs in pool
- [ ] Win / Loose Strak Reward

### Actions
- [ ] Reroll
- [ ] buy exp
- [ ] Buy Champ
- [ ] Sell Champ
- [ ] Arrange Champs
- [ ] Ready for Fight
- [ ] equip item

### After Fight
- [ ] do damage
- [ ] give gold and (exp)
- [ ] update streak
- [ ] if hero dies -> release champs
- [ ] drop items, gold or champs

### Procedure
1. round_counter -> carousel or fight
2. recieve actions from agents
3. Fight -> After Fight
* on end return results

**Resources**:
* [Multi Agent Gym](https://github.com/openai/multiagent-particle-envs/tree/master/multiagent)

***

# RL Part
> This bot tries to combine Advanced and State of the Art Techniques used by AlphaStar, AlphaGoZero and other Game Changers in the RL Space.

## Intro Links
* [Spinning up in DRL](https://spinningup.openai.com/en/latest/index.html)
    1. [Key Concepts in RL](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html)
    2. [Kinds of Algorithms](https://spinningup.openai.com/en/latest/spinningup/rl_intro2.html)
    3. [Policy Optimization](https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html)
    4. [Learning Curriculum](https://spinningup.openai.com/en/latest/spinningup/spinningup.html)
* [DRL Bootcamp](https://sites.google.com/view/deep-rl-bootcamp/lectures)
* [Key Papers for DRL](https://spinningup.openai.com/en/latest/spinningup/keypapers.html)
* [Beginner Reinforcement Learning](https://medium.com/@jonathan_hui/rl-introduction-to-deep-reinforcement-learning-35c25e04c199)
* [DRL Algos with pytorch](https://github.com/p-christ/Deep-Reinforcement-Learning-Algorithms-with-PyTorch)
* [Intro book to DRL](https://arxiv.org/pdf/1811.12560.pdf)
* [Deep Q-Learning](https://www.analyticsvidhya.com/blog/2019/04/introduction-deep-q-learning-python/)
* [Uni Stuttgart DRL Course](https://ipvs.informatik.uni-stuttgart.de/mlr/teaching/deep-reinforcement-learning-ss-18/)
* [automated game theory](https://github.com/LY0708/Automated-Game-Theory)
* streamlit for interface

**Useful Reads**
* [Deep Reinforcement Learning Doesn't Work Yet](https://www.alexirpan.com/2018/02/14/rl-hard.html)
* [Deep Learning and Reward Designfor Reinforcement Learning](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/136931/guoxiao_1.pdf)
* [Algorithms for Reinforcement Learning](https://sites.ualberta.ca/~szepesva/RLBook.html)


## Overview of the Architecture
![image](https://drive.google.com/uc?export=view&id=1vczvMH9eGrQYm8N89a16vMosimWHgQlX)


## League
> Using an Evoulutional Algorithm as outer Optimization save computation while saving a diverse set of strategies. It can also adjusted to save older startegies and at the end a Nash distribution can be picked with the least exploitable strategies.

* Combine Modules or Agents based on correlated metrics for winning (Macroperspective, Goldmanagement, Fight Positioning, ...)

**Resources**:
* [Alphastar](https://arxiv.org/pdf/1902.01724.pdf)


## Tournament
> Agents do actions and recieve a custom reward based on how likely it is winning and other metrics. The Winner overrides the other agents.
> Observation Space consist of not spatial data (can be partly represented as image) and the available action space.

**Resources**:


## Agent
> A hyrachical Architecture makes modular Training possible (also enables replacement), reduces the variational state space and can adapt to macro strategies better. In contrast there is a alternating update needed for sub policies and the controller to prevent unforeseeable effects. 

* Get Round counter with health and remaining players -> time state -> replace controller for macro action

**Resources**:
* [Reinforcement Learning Starcraft](https://arxiv.org/pdf/1809.09095.pdf#Hfootnote.1)


### Controller
> Decides based on Global state which sub policy should perform the next action. Can decide in a set time interval or in this case lets the sub policy decide when to stop or gives steps based on the global state. Maybe a cap for actions is needed because of the time limit.

* choose acitons (sub policies) or idle

**Resources**:


### Sub Policy Networks
> Each implements it's own action space with a special optimized network for this state. 
1. Arrange Units (Sequence to Sequence LSTM)
2. Get new buys -> direct action
3. Buy
4. Sell Unit
5. Buy Exp -> direct action
6. Order carousel units
7. Give Unit Item

**Resources**:
* [Unit Arrangement](https://arxiv.org/pdf/1706.04972.pdf)


### Agent Training
> Agents recieves a sample from the Replay Memory for Training. This enables that an Agent gives older memories more attention. The Memory gets erased after each episode / iteration. For more stable training a target network is used, to not change policy too quick. Evaluation and Improvent Network who alternate updating can also be discussed.

**Resources**:
