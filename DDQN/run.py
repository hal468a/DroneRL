import os, time
import tkinter as tk

from tkinter import filedialog
# from agent import Agent
from ddqn_agent import DDQN_Agent

def choose_env_path():
    root = tk.Tk()
    root.withdraw()
    env_path = filedialog.askopenfilename()
    print(env_path)

    return env_path

if __name__ == "__main__":

    # agent = Agent(useGPU=True, useDepth=True)
    # agent.train()
    
    env_path = choose_env_path()
    os.startfile(env_path)
    time.sleep(15)

    ddqn_agent = DDQN_Agent(useDepth=True)
    ddqn_agent.train()

