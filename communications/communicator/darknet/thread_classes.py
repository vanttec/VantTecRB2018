'''
Module to define the thread classes
'''
#For multithreading
import threading
from rx import Observable
from drone_communication import drone_communicate, PrintObserver

class DroneThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.source = Observable.create(drone_communicate)

    def run(self):
        self.source.subscribe(PrintObserver())

drone_thread = DroneThread(1, "Drone")
drone_thread.start()
