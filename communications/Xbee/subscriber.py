import time
from digi.xbee.devices import XBeeDevice
import json

def subscriber(xbee, imu):
    '''Esto es para el bote, el bote envia a la estacion cada 500ms'''
    #****************************************************************************************#
    # Replace with the serial port where your local module is connected to.
    PORT = "/dev/ttyUSB1"
    # Replace with the baud rate of your local module.
    BAUD_RATE = 9600
     #****************************************************************************************#

    print(" +-------------------------------------------------+")
    print(" |                       Bote                      |")
    print(" +-------------------------------------------------+\n")
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()
        device.flush_queues()

        print("Waiting conversation...\n")
        while True:
            xbee_message = device.read_data()
            if xbee_message is not None:
                #Imprime el json para prueba
                jmessage = json.loads(bytes(xbee_message.data).decode()) 
                print(jmessage)
                coords = imu.get_gps_coords()
                lat = coords['latitude']
                lon = coords['longitud']
                xbee.set_target(lat,lon)
                REMOTE_NODE_ID = "vtecstation" #El nodo con el que se quiere comunicar.
                xbee_network = device.get_network()
                remote_device = xbee_network.discover_device(REMOTE_NODE_ID) #Aqui debe enviarlo al servidor
                device.send_data(remote_device, xbee.send())

    finally:
        if device is not None and device.is_open():
            device.close()
