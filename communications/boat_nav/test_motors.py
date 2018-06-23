from motors import Motors


motors = Motors()
while True:
	motors.move(50,50)
	print("mover motor")
