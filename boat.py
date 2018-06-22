from communications.Xbee.comunicacion import xbee
from communications.thread_classes import BoatXbThread
from mission_data import MissionBoatData
import threading
from communications.darknet.caller import main_caller


class CameraThread(threading.Thread):
    '''Class to access camera data'''
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        main_caller()

def main_boat():
    main_data = MissionBoatData(xbee())
    thread_boat = BoatXbThread(1, "Boat", main_data.boat_xb) #subscriber
    #thread_camera = CameraThread(2, "Camera")

    thread_boat.start()
    #thread_camera.start()

    thread_boat.join()
    #thread_camera.join()

main_boat()
