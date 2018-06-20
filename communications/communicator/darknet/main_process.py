'''
	@name       	main.py
    @desc 			Principal file for the vantec boat.
	@author 		TODOS
	@created_at 	2018-06-19
	@updated_at 	2018-06-19
	@dependecies	python3
'''

'''
	Required python libraries 
'''
from thread_classes import DroneThread

#Basic libraries
'''
	Required our project libraries 
'''

class MainProgram:
	def __init__(self):
		# destiny_coords = [29.15168, -81.01726]
		# partial_degree = 0
		imu = Imu()
		navigation = Navigation()

		destiny = imu.get_degrees_and_distance_to_gps_coords(29.15168, -81.01726)

		# Create new threads
		thread_drone = DroneThread(1, "DroneThread")
        
		thread_lidar = LidarThread(2, "LidarThread")
		thread_navigation = NavigationThread(3, "NavigationThread")
		thread_main = MainThread(4, "MainThread")

		# Start Threads
		thread_camera.start()
		thread_lidar.start()
		thread_main.start()
		thread_navigation.start()

		thread_camera.join()
		thread_lidar.join()
		thread_main.join()
		thread_navigation.join()

		print("Terminating Main Program")


class LidarThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name

	def run(self):
		main_program.lidar.run()


class CameraThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name

	def run(self):
		while 1:
			self.frame = main_program.camera.read(False)


class NavigationThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name

	def run(self):
		main_program.navigation.navigate()


class CommunicationThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name

	def run(self):
		print("communication running")


class MainThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name

	def run(self):
		radar = Radar()
		destiny_pixel = radar.get_boat_pixel()

		while 1:
			#if distance is more than 3 meters (imu error is 2 meters)
			if(main_program.destiny['distance'] > 3)
				destiny_pixel = radar.get_destiny_pixel(
					main_program.destiny['distance'], main_program.destiny['distance'])

			mapa = radar.set_obstacles(
				main_program.lidar.get_obstacles(),
				main_program.camera.get_obstacles(main_program.camera_frame)
			)

			#radar partial degree updated if further than 50 cm;
			mapa, partial_degree = radar.set_route(
				mapa, destiny_pixel[0], destiny_pixel[1])
			radar.draw_radar(mapa)

			#Update course
			main_program.navigation.update_degree(partial_degree)


'''
' Inicio del programa
'''
main_program = MainProgram()
