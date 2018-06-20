'''
Helper module to have PrintObserver class
'''
from rx import Observer

class PrintObserver(Observer):
    '''Auxiliar class to print values published by observable'''
    def on_next(self, value):
        print("Received {0}".format(value))

    def on_completed(self):
        print("Done!")

    def on_error(self, error):
        print("Error Occurred: {0}".format(error))
