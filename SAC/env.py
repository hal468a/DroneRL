import sys
sys.path.append("D:\\DroneWorkspace\\DroneRL\\")

import time
import math
import airsim
import numpy as np

from PIL import Image
from setting_folder import settings

MOVEMENT_INTERVAL = 1

class DroneEnv(object):
    """Drone environment class using AirSim python API"""

    def __init__(self, useDepth=False):
        self.client = airsim.MultirotorClient()
        self.last_dist = self.get_distance(self.client.getMultirotorState().kinematics_estimated.position)
        self.quad_offset = (0, 0, 0)
        self.useDepth = useDepth

        self.z = -0.9

    def step(self, action):
        """Step"""
        # print("new step ------------------------------")

        self.quad_offset = self.interpret_action(action)
        # print("quad_offset: ", self.quad_offset)

        quad_vel = self.client.getMultirotorState().kinematics_estimated.linear_velocity
        
        self.client.moveByVelocityAsync(
            quad_vel.x_val + self.quad_offset[0],
            quad_vel.y_val + self.quad_offset[1],
            quad_vel.z_val + self.quad_offset[2],
            MOVEMENT_INTERVAL
        ).join()
        collision = self.take_discrete_action(action)

        time.sleep(0.5)
        quad_state = self.client.getMultirotorState().kinematics_estimated.position
        quad_vel = self.client.getMultirotorState().kinematics_estimated.linear_velocity

        if quad_state.z_val < - 7.3:
            self.client.moveToPositionAsync(quad_state.x_val, quad_state.y_val, -7, 1).join()

        result, done = self.compute_reward(quad_state, quad_vel, collision)
        state, image = self.get_obs()

        return state, result, done, image

    def reset(self):
        self.client.reset()
        self.last_dist = self.get_distance(self.client.getMultirotorState().kinematics_estimated.position)
        self.client.enableApiControl(True)
        self.client.armDisarm(True)
        self.client.takeoffAsync().join()
        quad_state = self.client.getMultirotorState().kinematics_estimated.position
        self.client.moveToPositionAsync(quad_state.x_val, quad_state.y_val, -7, 1).join()

        obs, image = self.get_obs()

        return obs, image

    def get_obs(self):
        if self.useDepth:
            # get depth image
            responses = self.client.simGetImages(
                [airsim.ImageRequest(0, airsim.ImageType.DepthPlanar, pixels_as_float=True)])
            response = responses[0]
            img1d = np.array(response.image_data_float, dtype=np.float64)
            img1d = img1d * 3.5 + 30
            img1d[img1d > 255] = 255
            image = np.reshape(img1d, (responses[0].height, responses[0].width))
            image_array = Image.fromarray(image).resize((84, 84)).convert("L")
        else:
            # Get rgb image
            responses = self.client.simGetImages(
                [airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)]
            )
            response = responses[0]
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
            image = img1d.reshape(response.height, response.width, 3)
            image_array = Image.fromarray(image).resize((84, 84)).convert("L")

        obs = np.array(image_array)

        return obs, image

    def get_distance(self, quad_state):
        """Get distance between current state and goal state"""
        pts = np.array([40, -50, -10])
        quad_pt = np.array(list((quad_state.x_val, quad_state.y_val, quad_state.z_val)))
        dist = np.linalg.norm(quad_pt - pts)
        return dist

    def compute_reward(self, quad_state, quad_vel, collision):
        """Compute reward"""

        reward = -1

        if collision:
            reward = -50
        else:
            dist = self.get_distance(quad_state)
            diff = self.last_dist - dist

            if dist < 10:
                reward = 500
            else:
                reward += diff

            self.last_dist = dist

        done = 0
        if reward <= -10:
            done = 1
            time.sleep(1)
        elif reward > 499:
            done = 1
            time.sleep(1)

        return reward, done

    def interpret_action(self, action):
        """Interprete action"""
        scaling_factor = 3

        if action == 0:
            self.quad_offset = (scaling_factor, 0, 0)
        elif action == 1:
            self.quad_offset = (-scaling_factor, 0, 0)
        elif action == 2:
            self.quad_offset = (0, scaling_factor, 0)
        elif action == 3:
            self.quad_offset = (0, -scaling_factor, 0)

        return self.quad_offset

    def get_PRY(self):
        state = self.client.getMultirotorState() # 無人機狀態
        quaternion = state.kinematics_estimated.orientation # 四元數
        pitch, roll, yaw = airsim.to_eularian_angles(quaternion) # 取得 pitch, roll, yaw

        pitch_deg = math.degrees(pitch)
        roll_deg = math.degrees(roll)
        yaw_deg = math.degrees(yaw)

        return quaternion, state, pitch_deg, roll_deg, yaw_deg
    
    def straight(self, speed, duration):

        quaternion, state, pitch, roll, yaw = self.get_PRY()

        vx = math.cos(yaw) * speed
        vy = math.sin(yaw) * speed
        yaw_mode = airsim.YawMode(is_rate=False, yaw_or_rate=0)
        self.client.moveByVelocityZAsync(vx, vy, self.z, duration, 1, yaw_mode).join()

    def move_right(self, speed, duration):

        quaternion, state, pitch, roll, yaw = self.get_PRY()

        vx = math.sin(yaw) * speed
        vy = math.cos(yaw) * speed
        self.client.moveByVelocityZAsync(vx, vy, self.z, duration, 0).join()
        start = time.time()
        return start, duration

    def yaw_right(self, rate, duration):
        self.client.rotateByYawRateAsync(rate, duration).join()
        start = time.time()
        return start, duration

    def pitch_up(self, duration):
        self.client.moveByVelocityAsync(0, 0, 1, duration, 1).join()
        start = time.time()
        return start, duration

    def pitch_down(self, duration):
        # yaw_mode = airsim.YawMode(is_rate=False, yaw_or_rate=0)
        self.client.moveByVelocityAsync(0, 0, -1, duration, 1).join()
        start = time.time()
        return start, duration

    def move_forward_Speed(self, speed_x = 0.5, speed_y = 0.5, duration = 0.5):
        
        quaternion, state, pitch, roll, yaw = self.get_PRY()

        vel = state.kinematics_estimated.linear_velocity # 取得速度

        vx = math.cos(yaw) * speed_x + math.sin(yaw) * speed_y
        vy = math.sin(yaw) * speed_x - math.cos(yaw) * speed_y

        drivetrain = 1
        yaw_mode = airsim.YawMode(is_rate= False, yaw_or_rate = 0)

        self.client.moveByVelocityAsync(vx = (vx + vel.x_val) / 2 ,
                             vy = (vy + vel.y_val) / 2 , #do this to try and smooth the movement
                             vz = self.z,
                             duration = duration,
                             drivetrain = drivetrain,
                             yaw_mode=yaw_mode
                            ).join()
        start = time.time()
        return start, duration
    
    def take_discrete_action(self, action):

        if action == 0:
            self.straight(settings.mv_fw_spd_2, settings.rot_dur)
        if action == 1:
            self.straight(settings.mv_fw_spd_3, settings.rot_dur)
        if action == 2:
            # self.yaw_right(settings.yaw_rate_1_2, settings.rot_dur/2)
            # self.straight(settings.mv_fw_spd_3, settings.rot_dur/2)
            self.move_forward_Speed(settings.mv_fw_spd_2*math.cos(0.314),
                                    settings.mv_fw_spd_2*math.sin(0.314), settings.rot_dur)
        if action == 3:
            # self.yaw_right(settings.yaw_rate_1_2, settings.rot_dur / 2)
            # self.straight(settings.mv_fw_spd_4, settings.rot_dur / 2)
            self.move_forward_Speed(settings.mv_fw_spd_3 * math.cos(0.314),
                                    settings.mv_fw_spd_3 * math.sin(0.314), settings.rot_dur)
        if action == 4:
            # self.yaw_right(settings.yaw_rate_2_2, settings.rot_dur / 2)
            # self.straight(settings.mv_fw_spd_4, settings.rot_dur / 2)
            self.move_forward_Speed(settings.mv_fw_spd_2 * math.cos(0.314),
                                    -settings.mv_fw_spd_2 * math.sin(0.314), settings.rot_dur)
        if action == 5:
            # self.yaw_right(settings.yaw_rate_2_2, settings.rot_dur / 2)
            # self.straight(settings.mv_fw_spd_4, settings.rot_dur / 2)
            self.move_forward_Speed(settings.mv_fw_spd_3 * math.cos(0.314),
                                    -settings.mv_fw_spd_3 * math.sin(0.314), settings.rot_dur)
        if action == 6:
            self.yaw_right(settings.yaw_rate_1_2, settings.rot_dur )
        if action == 7:
            self.yaw_right(settings.yaw_rate_2_2, settings.rot_dur)

        collision = self.client.simGetCollisionInfo().has_collided

        return collision
    
    def take_continious_action(self, action):

        if(settings.control_mode=="moveByVelocity"):
            action=np.clip(action, -0.3, 0.3)

            detla_x = action[0]
            detla_y = action[1]
            v=self.drone_velocity()
            v_x = v[0] + detla_x
            v_y = v[1] + detla_y

            yaw_mode = airsim.YawMode(is_rate=False, yaw_or_rate=0)
            self.client.moveByVelocityZAsync(v_x, v_y, self.z, 0.35, 1, yaw_mode).join()

        else:
            raise NotImplementedError

        collision = self.client.simGetCollisionInfo().has_collided
        return collision
        # Todo : Stabilize drone