import gym
import numpy as np
import pygame

env = gym.make("MountainCar-v0", render_mode="human") # （1）
observation, info = env.reset(seed=42)  # （2）
for _ in range(1000):
   action = 0  # User-defined policy function
   observation, reward, terminated, truncated, info = env.step(action) # （3）

   if terminated or truncated:
      observation, info = env.reset()

env.close()
pygame.quit()