from gym.envs.registration import register

register(
    id="DroneRL-v0",
    entry_point="mygym.envs:MyAirSimEnv"
)