import time
from digi.xbee.devices import XBeeDevice
import json
from comunicacion import *
from ..darknet
xbee = xbee()

def subscriber():
#Esto es para el bote, el bote envia a la estacion cada 500ms
     #****************************************************************************************#

    # TODO: Replace with the serial port where your local module is connected to.
    PORT = "/dev/ttyUSB0"
    # TODO: Replace with the baud rate of your local module.
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
                REMOTE_NODE_ID = "vtecstation" #El nodo con el que se quiere comunicar.
                xbee_network = device.get_network()
                remote_device = xbee_network.discover_device(REMOTE_NODE_ID) #Aqui debe enviarlo al servidor
                device.send_data(remote_device, xbee.send())

    finally:
        if device is not None and device.is_open():
            device.close()

#Sender()
subscriber()
#La conversacion comienza teniendo a uno de los dos escuchando y al otro dando la primer palabra
#El que escucha es Receiver2Server