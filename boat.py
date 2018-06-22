from communications.Xbee.comunicacion import xbee
from communications.thread_classes import BoatXbThread, CameraThread
from mission_data import MissionBoatData

def main_boat():
    main_data = MissionBoatData(xbee())
    thread_boat = BoatXbThread(1, "Boat", main_data.boat_xb) #subscriber
    thread_camera = CameraThread(2, "Camera")

    thread_boat.start()
    thread_camera.start()

    thread_boat.join()
    thread_camera.join()

main_boat()
