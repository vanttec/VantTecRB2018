'''
	@name       	automatedDocking.py
    @desc 			Class for the Automated Docking challenge
	@author 		Alejandro Gonzalez alex_gg97@hotmail.com
	@created_at 	2018-06-06
	@dependecies	python3
'''

'''
	Required python libraries
'''
#Add python3 path
import os
import sys

#Basic libraries
import time
import math
import random
import datetime

from num_detection import xy_c
#Vision and communication libraries are missing

'''
	Required our project libraries
'''
import motors as motors.Motors

class AutoDock:
	def __init__(self):
		self.Display = 0 	#Display number seen by the UAV (1,2 or 3)
		self.Dock = 0		#Dock the boat has to dock on (Dock1, Dock2, Dock3)
		self.Dock1 = 0		#Horizontal pixel the Dock1 is on the camera
		self.Dock2 = 0		#Horizontal pixel the Dock2 is on the camera
		self.Dock3 = 0		#Horizontal pixel the Dock3 is on the camera
		self.Center = 240		#Horizontal pixel which is the center of the image (480 pixels)
		#Error margin of a 50 pixels
		#We need experiments to change it
		self.CenterMin = Center + 25
		self.CenterMax = Center - 25

	def get_docks_horizontal_coordinate():
		#Get the horizontal center of each dock
		#We need the 'xc' of each number, so the number changes with time

		Dock1 = xy_c[0]
		Dock2 = xy_c[1]
		Dock3 = xy_c[2]

	def get_dock_number():
		#we need to get the result coming from the phone, for now we can test giving it the number
		Display = 1

		if Display = 1:
			Dock = Dock1

		elif Display = 2:
			Dock = Dock2

		elif Display = 3:
			Dock = Dock3


	def run(self):
		if Dock < CenterMin and Dock > CenterMax :
			if Dock < CenterMin :
				motors.move(50,0)

			elif Dock > CenterMax :
				motors.move(0,50)

		else
			motors.move(50,50)

auto_dock = AutoDock()
