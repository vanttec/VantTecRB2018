'''
	@name       	navigation.py
    @desc 			Navigation file. integration of boat movement 
	@author 		Marcopolo Gil Melchor marcogil93@gmail.com
	@created_at 	2017-11-28 
	@updated_at 	2017-11-28
	@dependecies	python3
'''

'''
	Required python libraries 
'''
#Basic libraries
import time
import math
import random
import datetime

'''
	Required our project libraries 
''' 
from .motors import Motors
from .imu import Imu

class Navigation:
	def __init__(self):
		self.frame = None
		self.stopNavigation = False

	def navigate(self, destiny, lat, lon):
		lastOrientationDegree = 0
		turn_degrees_needed   = 0
		turn_degrees_accum    = 0
		distance = destiny['distance']
		orientationDegree = destiny['degree']

		imu = Imu()
		motors = Motors()
		#clean angle
		imu.get_delta_theta()

		#Condition distance more than 2 meters. 
		while distance > 2 and not self.stopNavigation:
			#print("degrees: ", imu.NORTH_YAW)
			#print("coords: ", imu.get_gps_coords())
			#print("orientation degrees", orientationDegree)
			if lastOrientationDegree != orientationDegree:
				turn_degrees_needed = orientationDegree
				turn_degrees_accum  = 0

				#clean angle
				imu.get_delta_theta()
				lastOrientationDegree = orientationDegree

			#If same direction, keep route
			#while math.fabs(turn_degrees_needed) > 10:
			imu_angle = imu.get_delta_theta()['z']%360

			if imu_angle > 180:
				imu_angle = imu_angle - 360
			#print("grados imu: ", imu_angle)

			#threshold
			if math.fabs(imu_angle) > 1:
				turn_degrees_accum += imu_angle

			#print("grados acc: ", turn_degrees_accum)
			turn_degrees_needed = (orientationDegree + turn_degrees_accum)%360

			if turn_degrees_needed > 180 : 
				turn_degrees_needed = turn_degrees_needed - 360
			elif  turn_degrees_needed < -180:
				turn_degrees_needed = turn_degrees_needed + 360
			
			#print("grados a voltear: ", turn_degrees_needed)

			if math.fabs(turn_degrees_needed) < 10: 
				print("Tengo un margen menor a 10 grados")
				velocity = distance * 10

				if  velocity > 40:
					velocity = 30

				motors.move(velocity, velocity)

			else:
				#girar
				if turn_degrees_needed > 0:
					print("Going to move left")
					motors.move(30, -30)
				else: 
					print("Going to move right")
					motors.move(-30, 30)
			#ir derecho
			#recorrer 2 metros
			destiny = imu.get_degrees_and_distance_to_gps_coords(lat, lon)
			#time.sleep(1)
		motors.move(0,0)
