'''
Module to define the thread classes
'''
#For multithreading
import threading
import socket
from .Xbee.subscriber import subscriber
from .drone_communication.drone_server import receive
from .boat_nav.imu import Imu
from .darknet.caller import main_caller

class DroneThread(threading.Thread):
    '''Class to access drone data'''
    def __init__(self, thread_id, name, mission_data):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.data = mission_data

    def run(self):
        '''Function running the thread listnening for drone data'''
        receive(self.data)

class DroneCheker(threading.Thread):
    '''Class to test changes in global variables'''
    def __init__(self, thread_id, name, dock_num, map_data):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.dock_num = dock_num
        self.map_data = map_data

    def run(self):
        '''Printing data of the drone'''
        while True:
            print('Dock num ', self.dock_num)
            print('Map data ', self.map_data)


class BoatXbThread(threading.Thread):
    '''Class to access xbee data from boat, uses subscriber function'''
    def __init__(self, thread_id, name, boat_xb):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.boat_xb = boat_xb

    def run(self):
        subscriber(self.boat_xb, Imu())

class CameraThread(threading.Thread):
    '''Class to access camera data'''
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        main_caller()
