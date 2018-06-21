from communications.Xbee import xbee
from communications.thread_classes import BoatXbThread
from mission_data import MissionBoatData

def main_boat():
    main_data = MissionBoatData(xbee())
    thread_boat = BoatXbThread(1, "Boat", main_data.boat_xb)

    thread_boat.start()

main_boat()
