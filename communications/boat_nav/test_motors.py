from motors import Motors

motors = Motors()
while True:
    motors.move_thrusters(1600,1600)