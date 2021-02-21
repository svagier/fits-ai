from gym.envs.registration import register

register(
    id='fits-v1',
    entry_point='ai.env:FitsEnv',
)
