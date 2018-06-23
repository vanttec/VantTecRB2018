from motors import Motors
import serial
import time
def kill_me():
    ser = serial.Serial('/dev/ttyACM0', 115200)
    val = '%B,1600,1600%'
    val2 = '%B,1500,1500%'
    val = val.encode()
    val2 = val2.encode()
    ser.write(val)
    time.sleep(15)
    ser.write(val2)
    ser.close()
kill_me()
