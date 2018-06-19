import socket

HOST = "127.0.0.1"
PORT = 5000
END = 'kthanksbye'

def main():
    # Make it a callback
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

        if eoh != -1:
            break
        # split the header and keep data (img)
        header, data = header[:eoh], header[eoh + len(END):]
        header = header.decode()
        # if mamalon
        # Dock number
        if header == "DockNum":
            # callback with base number
            pass
        # Map
        if header == "Map":
            # Positions List
            pass
        # Dock photo
        else:
            # TODO: Instead of writing, collect the binary and send it
            # Analyse header
            # "DockPhoto,12,424,532"
            try:
                start, length, offset, size = header.split(',')
            except ValueError:
                print("Unknown header", header)
                continue
            if start == "DockPhoto":
                length, offset, size = map(int, [length, offset, size])

                if offset + size == length:
                    fhand.write(img_data)
                    img_data = b''
                else:
                    img_data += data
           
    conn.close()

main()
