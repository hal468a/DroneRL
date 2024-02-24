import tkinter as tk
from tkinter import filedialog

class HP():
    def __init__(self):
        self.name = "helper"
    
    # 選擇要啟動的環境
    def activate_env_win(self):

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