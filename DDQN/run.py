import os, time

from agent import Agent
from ddqn_agent import DDQN_Agent

if __name__ == "__main__":

    # agent = Agent(useGPU=True, useDepth=True)
    # agent.train()
    
    os.startfile("D:\\DroneWorkspace\\Enviroments\\Blocks\\Blocks.exe")
    time.sleep(15)

    ddqn_agent = DDQN_Agent(useDepth=True)
    ddqn_agent.train()