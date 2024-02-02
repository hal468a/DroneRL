import os, time

from Helper import helper
# from agent import Agent
from ddqn_agent import DDQN_Agent

hp = helper()

if __name__ == "__main__":

    # agent = Agent(useGPU=True, useDepth=True)
    # agent.train()
    
    env_path = hp.activate_env()
    os.startfile(env_path)
    time.sleep(15)

    ddqn_agent = DDQN_Agent(useDepth=True)
    ddqn_agent.train()