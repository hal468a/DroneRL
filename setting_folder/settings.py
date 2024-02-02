# ---------------------------
# parameters
# ---------------------------
vel_duration=0.4
double_dqn = False
mv_fw_dur = 0.4
mv_fw_spd_1 = 1* 0.5
mv_fw_spd_2 = 2* 0.5
mv_fw_spd_3 = 3* 0.5
mv_fw_spd_4 = 4* 0.5
mv_fw_spd_5 = 5* 0.5
rot_dur = 0.1 #0.15
# yaw_rate = (180/180)*math.pi #in degree
yaw_rate_1_1 = 108.  # FOV of front camera
yaw_rate_1_2 = yaw_rate_1_1 * 0.5  # yaw right by this angle
yaw_rate_1_4 = yaw_rate_1_2 * 0.5
yaw_rate_1_8 = yaw_rate_1_4 * 0.5
yaw_rate_1_16 = yaw_rate_1_8 * 0.5
yaw_rate_2_1 = -108.  # -2 time the FOV of front camera
yaw_rate_2_2 = yaw_rate_2_1 * 0.5  # yaw left by this angle
yaw_rate_2_4 = yaw_rate_2_2 * 0.5
yaw_rate_2_8 = yaw_rate_2_4 * 0.5
yaw_rate_2_16 = yaw_rate_2_8 * 0.5


# ---------------------------
# general params
# ---------------------------
nb_max_episodes_steps = 512*3  # pay attention
success_distance_to_goal = 2
slow_down_activation_distance =  2*success_distance_to_goal  # detrmines at which distance we will punish the higher velocities