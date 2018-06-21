'''
	@name       	gpsNavigation.py
    @desc 			Principal file for the vantec boat.
	@author  	   	Alejandro Gonzalez
	@created_at     2018-03-07
'''

'''
	Required python libraries 
'''

#Basic libraries

'''
	Required our project libraries 
''' 
from navigation import Navigation
from imu import Imu


class GPSNavigation:
	def __init__(self):
		self.imu = Imu()
		self.navigation = Navigation()

	def update_nav(self, lat, lon):
		destiny = self.imu.get_degrees_and_distance_to_gps_coords(lat, lon)
		self.navigation.navigate(destiny,lat,lon)

if __name__ == '__main__':

	gps_navigation = GPSNavigation()
	gps_navigation.update_nav(25.653326,-100.291307)  # First Waypoint
	#gps_navigation.update_nav(29.15168, -81.01726)	# Second Waypoint
	#gps_navigation.update_nav(29.15168, -81.01726)	# Third Waypoint
