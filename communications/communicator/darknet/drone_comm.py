'''
Module to communicate drone and the station
'''
import socket
from rx import Observable
from my_observable import PrintObserver

HOST = "127.0.0.1"
PORT = 5000
END = 'kthanksbye'

def drone_communicate(observer):
    '''Socket with rx python'''
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((HOST, PORT))
    my_socket.listen(1)
    conn, addr = my_socket.accept()
    print("Connection from: " + str(addr))
    header = b''
    fhand = open("file.jpg", "wb")
    img_data = b''

    while True:
        data = conn.recv(1024)
        if not data:
            raise RuntimeError("No header/data")
        header += data
        # end-of-header in buffer yet_
        eoh = header.find(b'kthanksbye')

        print("Received data")
        conn.send("holi".encode())

        if eoh == -1:
            continue
        # split the header and keep data
        header, data = header[:eoh], header[eoh + len(END):]
        header = header.decode()

        # Dock number
        if header == "DockNum":
            observer.on_next(data)

        # Map
        elif header == "Map":
            observer.on_next(data)

        # Dock photo
        else:
            # Analyse header
            # "DockPhoto,12,424,532"
            try:
                start, length, offset, size = header.split(',')
            except ValueError:
                observer.on_error("Unknow header")
                observer.on_error(header)
                # print("Unknown header", header)
                continue
            if start == "DockPhoto":
                length, offset, size = map(int, [length, offset, size])

                if offset + size == length:
                    fhand.write(img_data)
                    img_data = b''
                    observer.on_next("Image")
                else:
                    img_data += data
    conn.close()
    observer.on_completed()

source = Observable.create(drone_communicate)

source.subscribe(PrintObserver())
