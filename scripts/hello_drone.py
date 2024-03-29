import numpy as np
import subprocess, sys
import airsim, os, tempfile, pprint, cv2, time

sys.path.append('D:\\DroneWorkspace\\DroneRL')

from Helper import helper
hp = helper.HP()

if __name__ == '__main__':

    env_path = hp.activate_env()
    os.startfile(env_path)
    time.sleep(10) # 等待15秒

    # connect to the AirSim simulator
    client = airsim.MultirotorClient(ip="127.0.0.1")
    client.confirmConnection()
    client.enableApiControl(True)

    state = client.getMultirotorState()
    print(state)
    s = pprint.pformat(state)
    print("state: %s" % s)

    imu_data = client.getImuData()
    s = pprint.pformat(imu_data)
    print("imu_data: %s" % s)

    barometer_data = client.getBarometerData()
    s = pprint.pformat(barometer_data)
    print("barometer_data: %s" % s)

    magnetometer_data = client.getMagnetometerData()
    s = pprint.pformat(magnetometer_data)
    print("magnetometer_data: %s" % s)

    gps_data = client.getGpsData()
    s = pprint.pformat(gps_data)
    print("gps_data: %s" % s)

    # airsim.wait_key('Press any key to takeoff')
    print("Taking off...")
    client.armDisarm(True)
    client.takeoffAsync().join()

    state = client.getMultirotorState()
    print("state: %s" % pprint.pformat(state))

    # airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
    client.moveToPositionAsync(40, -50, -10, 5).join()

    client.hoverAsync().join()

    state = client.getMultirotorState()
    print("state: %s" % pprint.pformat(state))

    # airsim.wait_key('Press any key to take images')

    # get camera images from the car
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.DepthVis),  # depth visualization image
        # airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True), # depth in perspective projection
        airsim.ImageRequest("1", airsim.ImageType.Scene), # scene vision image in png format
        airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])  # scene vision image in uncompressed RGBA array
    print('Retrieved images: %d' % len(responses))

    tmp_dir = os.path.join("D:\DroneWorkspace\DroneRL\Pictures")

    print ("Saving images to %s" % tmp_dir)
    try:
        os.makedirs(tmp_dir)
    except OSError:
        if not os.path.isdir(tmp_dir):
            raise

    for idx, response in enumerate(responses):

        filename = os.path.join(tmp_dir, str(idx))

        # if response.pixels_as_float:
        #     print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
        #     airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
        # el
        if response.compress: # png format
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
        else: #uncompressed array
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) # get numpy array
            img_rgb = img1d.reshape(response.height, response.width, 3) # reshape array to 4 channel image array H X W X 3
            cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb) # write to png
    
    airsim.wait_key('Press any key to reset to original state')

    client.reset()
    client.armDisarm(False)

    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False)