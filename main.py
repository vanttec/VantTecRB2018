from communications.Xbee import xbee
from communications.thread_classes import DroneThread,DroneCheker, BoatXbThread
from mission_data import MissionBoatData

def main():
    main_data = MissionBoatData(xbee(), xbee())
    thread_drone = DroneThread(1, "DroneComm", main_data)
    thread_check = DroneCheker(2, "Drone Check", main_data.dock_num, main_data.map_data)
    thread_boat = BoatXbThread(3, "Boat", main_data.boat_xb)

    thread_drone.start()
    thread_check.start()
    thread_boat.start()

main()
