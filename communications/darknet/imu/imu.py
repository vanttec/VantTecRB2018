'''
	@name       	imu.py
    @desc 			Imu Controller.
					This file has all the necesary functions to access the imu for the
					autonomous navigation, such as position, orientation, velocity,
					acceleration, etc.
	@author 		Marcopolo Gil Melchor marcogil93@gmail.com
	@created_at 	2017-06-08 
	@updated_at 	2017-11-28 Restructuration and comments. 
	@dependecies	python3
'''

'''
	Required dependencies
'''
#Vector Nav library
import os
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages/vnpy')
from vnpy import *

#Basic libraries
import math
import time

#Debug libraries
from inspect import getmembers
from pprint import pprint

#	CONSTANTS
EARTH_RADIUOS = 6371000
PORT = 	'/dev/ttyUSB0'
'''
@desc 	Init imu module connection **
@params None
@return None
'''

class Imu:
	def __init__(self):
		self.northYaw = 0
		self.earthRadious = EARTH_RADIUOS
		self.vnSensor = VnSensor()
		self.baudRate = 115200
		self.get_port()
		self.connect()

	'''
	@desc 	Get imu port **
	@params None
	@return string
	'''
	def get_port(self):
		
		if os.path.exists(PORT):
			return 
			print("Port Found")
			return PORT
		else:
			sys.exit('IMU not found // Check if connected')

	'''
	@desc 	Get Imu model information **
	@params None
	@return string
	'''
	def print_model(self):
		return self.vnSensor.read_model_number()


	'''
	@desc Close Imu sensor
	@params None
	@return None
	'''
	def close_(self):
		self.vnSensor.disconnect()

	'''
	@desc Reconnect Imu
	@params None
	@return None
	'''
	def connect(self):
		self.vnSensor.connect(PORT,self.baudRate)
	'''
	@desc 	Get  number of listening Satellites**
	@params None
	@return integer 
	'''
	def get_num_satellites(self):
		#Return values of gps
		#'gps_fix', 'lla', 'ned_acc', 'ned_vel', 'num_sats', 'speed_acc', 'this', 'time', 'time_acc', 'week'
		return self.vnSensor.read_gps_solution_lla().num_sats

	'''
	@desc 	Get averages of latitude and longitud coords after 10 tests
	@params None
	@return dynamic array
				float longitud
				float latitude
	'''
	def get_gps_coords(self):
		coord_x = 0
		coord_y = 0

		#Get average coords of 10 tests
		for i in range(10):
			lla = self.vnSensor.read_gps_solution_lla()
			coord_x += lla.lla.x
			coord_y += lla.lla.y
		
		coord_x = coord_x / 10
		coord_y = coord_y / 10

		coords ={ 'latitude': coord_x , 'longitud': coord_y}

		return coords

	'''
	@desc 	Get  yaw pitch roll degrees
	@params None
	@return vec3f object
				float x 
				float y
				float z 
	'''
	def get_yaw_pitch_roll(self):
		return self.vnSensor.read_yaw_pitch_roll()

	'''
	@desc 	Get  yaw degree
	@params None
	@return float degree
	'''
	def get_yaw_orientation(self):
		degree = self.vnSensor.read_yaw_pitch_roll().x%360

		if(degree > 180):
			degree = degree - 360


		return degree

	'''
	@desc 	Get  magnetic fields measurements
	@params None
	@return vec3f object of cgs (centimetre–gram–second) units (Gaussian units)
				float x 
				float y
				float z 
	'''
	def get_magnetic_measurments(self):
		return self.vnSensor.read_magnetic_measurements()

	'''
	@desc 	Get  magnetic fields measurements
	@params None
	@return ???
	'''
	def get_magnetic_and_gravity_reference(self):
		return self.vnSensor.read_magnetic_and_gravity_reference_vectors()

	'''
	@desc 	Get  all imu measurments
	@params None
	@return ???
	'''
	def get_imu_measurements(self):
		return self.vnSensor.read_imu_measurements()

	'''
	@desc 	Get acceleration and velocity vectors
	@params None
	@return dynamic array
				vec3f acceleration
				vec3f velocity
	'''
	def get_gps_acceleration_velocity(self):
		lla = self.vnSensor.read_gps_solution_lla()

		return {
			'acceleration': lla.ned_acc,
			'velocity': lla.ned_vel
		}

	'''
	@desc Get acceleration and velocity vectors
	@params None
	@return dynamic array
				vec3f acceleration
				vec3f velocity
	'''
	def get_angular_rates(self):
		angles = self.vnSensor.read_angular_rate_measurements()

		return {
			'x': angles.x%360,
			'y': angles.y%360,
			'z': angles.z%360,
		}

	'''
	@desc Get acceleration
	@params None
	@return vec3f acceleration
	'''
	def get_acceleration(self):
		return self.vnSensor.read_acceleration_measurements()

	'''
	@desc Get delta theta
	@params None
	@return dynamic array
				x
				y
				z
	'''
	def get_delta_theta(self):
		angles = self.vnSensor.read_delta_theta_and_delta_velocity().delta_theta

		return {
			'x': angles.x%360,
			'y': angles.y%360,
			'z': angles.z%360,
		}

	'''
	@desc Get delta velocity
	@params None
	@return vec3f velocity
	'''
	def get_delta_velocity(self):
		return self.vnSensor.read_delta_theta_and_delta_velocity().delta_velocity

	'''
	@desc Get needed degrees to point north
	@params None
	@return float degree
	'''
	def get_degrees_to_north_orientation(self):
		degree = (self.get_yaw_orientation()%360) - self.northYaw

		if (degree > 180):
			degree = degree - 360


		return degree

	'''
	@desc get degrees and distance to gps coords
	@params goal latitude and longitud
	@return dynamic array
				float distance  meters
				float degrees 
	'''
	def get_degrees_and_distance_to_gps_coords(self, latitude2, longitud2):
		north = (self.get_yaw_orientation()%360) - self.northYaw

		if (north > 180):
			north = north - 360

		coords = self.get_gps_coords()
		latitude1 = coords['latitude']
		longitud1 = coords['longitud']

		#print(coords)
		#print(latitude2, longitud2)

		longitud_distance = (longitud1 - longitud2)
		y_distance = math.sin(longitud_distance) * math.cos(latitude2)
		x_distance = math.cos(latitude1) * math.sin(latitude2) - math.sin(latitude1) * math.cos(latitude2) * math.cos(longitud_distance)
		bearing = math.atan2(y_distance, x_distance)
		bearing = math.degrees(bearing) - north
		bearing = (bearing + 360) % 360

		if (bearing > 180):
			bearing = bearing - 360

		phi1 = math.radians(latitude1)
		phi2 = math.radians(latitude2)
		dphi = math.radians(latitude2 - latitude1)
		dlam = math.radians(longitud2 - longitud1)
		a = math.sin(dphi/2)*math.sin(dphi/2) + math.cos(phi1)*math.cos(phi2)* math.sin(dlam/2)*math.sin(dlam/2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		distance = self.earthRadious * c

		return {
			'distance': int(distance),
			'degree': int(bearing) * -1
		}
	def get_obstacle_gps_coords(boat_X, boat_y, path_x, path_y):

		coords = self.get_gps_coords(self)
		latitude1 = coords['latitude']
		longitud1 = coords['longitud']

		#print(coords);
		#print(latitude2, longitud2);

		y_distance = path_y - boat_y
		x_distance = path_x - boat_x

		latitude2  = latitude1  + (y_distance / EARTH_RADIUOS) * (180 / math.pi)
		longitude2 = longitude1 + (x_distance / EARTH_RADIUOS) * (180 / math.pi) / math.cos(latitude1 * math.pi/180)

		return {
			'latitude': latitude2
			'longitud': longitude2
		}
