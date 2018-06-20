import time
from digi.xbee.devices import XBeeDevice
import json

def publisher(xbee):
    '''Xbee station'''
    #****************************************************************************************#
    # TODO: Replace with the serial port where your local module is connected to.
    PORT = "/dev/ttyUSB0" #La estacion
    # TODO: Replace with the baud rate of your local module.
    BAUD_RATE = 9600
    DATA_TO_SEND = "Starting conversation..." #Inicia la conversacion con esto
    REMOTE_NODE_ID = "vtecboat" #El remoto es el bote, Esta es la estacion
    #****************************************************************************************#

    print(" +--------------------------------------+")
    print(" |           Sender (Station)           |")
    print(" +--------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)
    try:
        device.open()
        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        print("Dame la latitud y longitud del waypoint donde se iniciara el challenge: ")
        lat = input("\n lat: ")
        lon = input("\n lon: ")
        xbee.set_latlong(lat,lon)
        device.send_data(remote_device, xbee.send())
        while True:
            xbee_message = device.read_data()
            if xbee_message is not None:
                jmessage = json.loads(xbee_message.data.decode()) ###### Guarda el json
                print(jmessage) #Imprime el json para prueba
                print ("\n")

                xbee_network = device.get_network()
                remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
                lat = input("\n lat: ")
                lon = input("\n lon: ")
                xbee.set_latlong(lat,lon)
                device.send_data(remote_device, xbee.send())

        print("Success")

    finally:
        if device is not None and device.is_open():
            device.close()
