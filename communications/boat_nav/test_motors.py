from motors import Motors

def kill_me():
    motors = Motors()
    while True:
        motors.move_thrusters(1600,1600)

kill_me()
