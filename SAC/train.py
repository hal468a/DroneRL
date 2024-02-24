import sys

sys.path.append("/home/louis/Desktop/DroneRL")
# sys.path.append("D:\\DroneWorkspace\\DroneRL")

import os, time, subprocess
from Helper import helper
# from agent import Agent
from SAC.sac import SAC_Agent

if __name__ == "__main__":

    hp = helper.HP()

    # windows
    # env_path = hp.activate_env_win()
    # os.startfile(env_path)
    # time.sleep(15)

    sac = SAC_Agent(useDepth=True)
    sac.train()