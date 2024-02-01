import os, time
import tkinter as tk

# from agent import Agent
from tkinter import filedialog
from ddqn_agent import DDQN_Agent

def choose_env_path():

    env_path = ""
    file_type = [("exe file", '*.exe')]

    while env_path == "":
        root = tk.Tk()
        root.withdraw()
        env_path = filedialog.askopenfilename(filetypes=file_type)

        if env_path == "":
            print(f"Please select an Env file! (.exe)!!!")
    
    print(f"Selected Env: {env_path}")
    return env_path

if __name__ == "__main__":

    # agent = Agent(useGPU=True, useDepth=True)
    # agent.train()
    
    env_path = choose_env_path()
    os.startfile(env_path)
    time.sleep(15)

    ddqn_agent = DDQN_Agent(useDepth=True)
    ddqn_agent.train()

