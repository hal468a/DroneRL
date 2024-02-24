import sys

sys.path.append("/home/louis/Desktop/DroneRL")
# sys.path.append("D:\\DroneWorkspace\\DroneRL")

import os, time, subprocess
from Helper import helper
# from agent import Agent
from ddqn_agent import DDQN_Agent

if __name__ == "__main__":

    hp = helper.HP()

    # windows
    # env_path = hp.activate_env_win()
    # os.startfile(env_path)
    # time.sleep(15)

    ddqn_agent = DDQN_Agent(useDepth=True)
    ddqn_agent.train()