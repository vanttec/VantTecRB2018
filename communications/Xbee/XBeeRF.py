# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import time
from digi.xbee.devices import XBeeDevice
import json
from comunicacion import *
xbee = xbee('modulos')

########################

def Sender():

 #****************************************************************************************#
    # TODO: Replace with the serial port where your local module is connected to.
    PORT = "COM3" #La estacion
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

        print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), DATA_TO_SEND))

        device.send_data(remote_device, DATA_TO_SEND)
        while True:
            xbee_message = device.read_data()
            if xbee_message is not None:
                jmessage = json.loads(xbee_message.data.decode()) ###### Guarda el json
                print(jmessage) #Imprime el json para prueba
                print ("\n")

                xbee_network = device.get_network()
                remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
                device.send_data(remote_device, DATA_TO_SEND)

        print("Success")

    finally:
        if device is not None and device.is_open():
            device.close()

def Receiver2Sender():
#Esto es para el bote, el bote envia a la estacion cada 500ms
     #****************************************************************************************#

    # TODO: Replace with the serial port where your local module is connected to.
    PORT = "COM4"
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

                REMOTE_NODE_ID = "vtecstation" #El nodo con el que se quiere comunicar.
                xbee_network = device.get_network()
                remote_device = xbee_network.discover_device(REMOTE_NODE_ID) #Aqui debe enviarlo al servidor
                print("Waiting to send for 500ms")
                time.sleep(.5)   # delays for 500 ms.
                device.send_data(remote_device, xbee.send())

    finally:
        if device is not None and device.is_open():
            device.close()

Sender()
Receiver2Sender()
#La conversacion comienza teniendo a uno de los dos escuchando y al otro dando la primer palabra
#El que escucha es Receiver2Server
