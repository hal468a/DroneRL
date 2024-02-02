import sys
sys.path.append("D:\\DroneWorkspace\\DroneRL")

import os, time

from Helper import helper
# from agent import Agent
from SAC.sac import SAC_Agent

hp = helper.HP()

if __name__ == "__main__":

    # agent = Agent(useGPU=True, useDepth=True)
    # agent.train()
    
    env_path = hp.activate_env()
    os.startfile(env_path)
    time.sleep(15)

    sac = SAC_Agent(useDepth=True)
    sac.train()