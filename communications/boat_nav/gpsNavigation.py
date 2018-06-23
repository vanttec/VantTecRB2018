'''
	@name       	gpsNavigation.py
    @desc 			Principal file for the vantec boat.
	@author  	   	Alejandro Gonzalez
	@created_at     2018-06-22
'''

'''
	Required python libraries 
'''

#Basic libraries

'''
	Required our project libraries 
''' 
from .navigation import Navigation



class GPSNavigation:
	def __init__(self, imu):
		self.imu = imu
		self.navigation = Navigation(imu)

	def update_nav(self, lat, lon):
		destiny = self.imu.get_degrees_and_distance_to_gps_coords(lat, lon)
		self.navigation.navigate(destiny,lat,lon)

	def auto_nav(self, pdistance, pdegree):
		self.navigation.visnavigate(pdistance,pdegree)
