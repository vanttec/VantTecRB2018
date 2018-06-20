'''
Module to define the thread classes
'''
#For multithreading
import threading
import socket
from Xbee import subscriber
from drone_communication import MAP_DATA, DOCK_NUM, receive

class DroneThread(threading.Thread):
    '''Class to access drone data'''
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        '''Function running the thread listnening for drone data'''
        receive()

thread_drone = DroneThread(1, "Drone")
thread_drone.start()

class DroneCheker(threading.Thread):
    '''Class to test changes in global variables'''
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        '''Printing data of the drone'''
        while True:
            print('Dock num ', DOCK_NUM)
            print('Map data ', MAP_DATA)

thread_check = DroneCheker(2, "Check")
thread_check.start()

class BoatXbThread(threading.Thread):
    '''Class to access xbee data'''
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        subscriber()
