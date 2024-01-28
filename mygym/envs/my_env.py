import gym
import airsim
import keyboard
import numpy as np

from gym import spaces
from keyboard import KeyboardEvent

class MyAirSimEnv(gym.Env):

    def __init__(self, ip_address='127.0.0.1'):

        self.client = airsim.MultirotorClient(ip=ip_address)
        self.client.confirmConnection()
        self.client.armDisarm(True)

        self.client.enableApiControl(True)
        self.action_space = spaces.Discrete(8) # 定義動作空間
        self.observation_space = spaces.Box(0, 255, shape=(200, 200, 3), dtype=np.uint8)# 定義觀測空間

        self.action()

    def human_step(self, x:KeyboardEvent):
        # # Set home position and velocity
        # self.client.moveToPositionAsync(self.drone_pos[0], 
        #                                 self.drone_pos[1], 
        #                                 self.drone_pos[2], 
        #                                 self.drone_vel).join()
        
        # self.client.moveByVelocityAsync(1, -0.67, -0.8, 5).join()
        
        if x.event_type == 'down' and x.name == self.esc.name:
            self.client.enableApiControl(False)

        elif x.event_type == "down" and x.name == self.up.name:
            self.client.moveByVelocityBodyFrameAsync(0, 0, -20, 0.5)
            print("你按下了 " + x.name + " 鍵")

        elif x.event_type == "down" and x.name == self.down.name:
            #下降
            self.client.moveByVelocityBodyFrameAsync(0, 0, 0.5, 0.5)
            print("你按下了 " + x.name + " 鍵")

        elif x.event_type == "down" and x.name == self.left.name:
            #左轉
            self.client.rotateByYawRateAsync(-20, 0.5)
            print("你按下了 " + x.name + " 鍵")

        elif x.event_type == "down" and x.name == self.right.name:
            #右轉
            self.client.rotateByYawRateAsync(20, 0.5)
            print("你按下了 " + x.name + " 鍵")
        elif x.event_type == "down" and x.name == self.w.name:
            #前進
            self.client.moveByVelocityBodyFrameAsync(3, 0, 0, 0.5)  # 控制無人機x正方向移動，不等待完成
            print("你按下了 "+ x.name + " 鍵")

        elif x.event_type == "down" and x.name == self.a.name:
            #左移
            self.client.moveByVelocityBodyFrameAsync(0, -2, 0, 0.5)
            print("你按下了 " + x.name + " 鍵")
        elif x.event_type == "down" and x.name == self.s.name:
            #後退
            self.client.moveByVelocityBodyFrameAsync(-3, 0, 0, 0.5)

            print("你按下了 " + x.name + " 鍵")
        elif x.event_type == "down" and x.name == self.d.name:
            #右移
            self.client.moveByVelocityBodyFrameAsync(0, 2, 0, 0.5)
            print("你按下了 " + x.name + " 鍵")
        elif x.event_type == 'down' and x.name == self.enter.name:
            #enter
            print("你按下了 " + x.name + " 鍵")
        elif x.event_type == 'down' and x.name == self.k.name:
            # 獲得控制
            self.client.enableApiControl(True)
            print("獲得控制")
            # 解鎖
            self.client.armDisarm(True)
            print("解鎖")
            self.client.takeoffAsync().join()
            print("起飛")
            print("你按下了 " + x.name + " 鍵")
        elif x.event_type == 'down' and x.name == self.l.name:
            #降落
            self.client.landAsync(timeout_sec=30).join()
            print("降落")
            # 上鎖
            self.client.armDisarm(False)
            print("上鎖")
            # 釋放控制
            self.client.enableApiControl(False)
            print("釋放控制")

            print("你按下了 " + x.name + " 鍵")
        elif x.event_type == 'down' and x.name == self.r.name:
            self.client.reset()
            print("Rest!!!")
        else:  # 沒有按下按鍵
            self.client.moveByVelocityBodyFrameAsync(0, 0, 0, 0.5).join()
            self.client.hoverAsync().join()  # 第四階段：懸停6秒鐘
            print("停止 懸停")
                
    def action(self):
        self.w = KeyboardEvent('down', 28, 'w')
        self.s = KeyboardEvent('down', 28, 's')
        self.a = KeyboardEvent('down', 28, 'a')
        self.d = KeyboardEvent('down', 28, 'd')
        self.up = KeyboardEvent('down', 28, 'up')
        self.down = KeyboardEvent('down', 28, 'down')
        self.left = KeyboardEvent('down', 28, 'left')
        self.right = KeyboardEvent('down', 28, 'right')
        self.enter = KeyboardEvent('down', 28, 'enter')
        self.k = KeyboardEvent('down', 28, 'k')
        self.l = KeyboardEvent('down', 28, 'l')
        self.r = KeyboardEvent('down', 28, 'r')
        self.esc = KeyboardEvent("down", 28, 'esc')

    def reset(self):
        self.client.reset()
    
    def step(self, action):
        # 執行動作，獲取新狀態
        # 返回觀測、獎勵、完成狀態、其他信息
        pass

    def reset(self):
        # 重置環境
        pass

    def render(self, mode='human'):
        # 渲染環境（如果需要）
        pass

    def close(self):
        # 清理操作
        pass

# if __name__ == "__main__":
#     env = MyAirSimEnv(ip_address='127.0.0.1')
#     keyboard.hook(env.human_step)
#     keyboard.wait()