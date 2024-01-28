from pymavlink import mavutil
import time

vehicle = mavutil.mavlink_connection("udpin:10.8.1.20:14551")

vehicle.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (vehicle.target_system, vehicle.target_component))

while True:
    msg = vehicle.recv_match(blocking=True)
    print(msg)
    print("------------------------------------\n")