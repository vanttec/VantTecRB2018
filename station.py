from communications.Xbee import xbee
from communications.thread_classes import DroneThread, DroneCheker, StationXbThread
from mission_data import MissionStationData

def main_station():
    main_data = MissionStationData(xbee())
    thread_drone = DroneThread(1, "DroneComm", main_data)
    thread_check = DroneCheker(2, "Drone Check", main_data.dock_num, main_data.map_data)
    thread_station = StationXbThread(3, "Station", main_data.station_xb)

    thread_drone.start()
    thread_check.start()
    thread_station.start()

main_station()
