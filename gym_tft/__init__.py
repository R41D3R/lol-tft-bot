from gym.envs.registration import register

register(
    id='tft-v0',
    entry_point='gym_tft.envs:TFTEnv',
)
register(
    id='tft-carousel-v0',
    entry_point='gym_tft.envs:TFTCarouselEnv',
)