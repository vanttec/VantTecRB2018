from communications.Xbee.comunicacion import xbee
from communications.thread_classes import BoatXbThread
from mission_data import MissionBoatData

def main_boat():
    main_data = MissionBoatData(xbee())
    thread_boat = BoatXbThread(1, "Boat", main_data.boat_xb) #subscriber

    thread_boat.start()
    thread_boat.join()

main_boat()
