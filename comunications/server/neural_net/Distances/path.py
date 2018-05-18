
"""MODULES IMPORT."""
import numpy as np
import cv2

"""CONSTANTS.
	KNOWN_DISTANCE -- Initialize the known distance from the camera to the object, which in this case is 10 inches.
	KNOWN_WIDTH --Initialize the known object width, which in this case, the piece of paper is 11 inches width.
	FOCAL_VIEW = 78.0
"""

KNOWN_DISTANCE = 10.0
KNOWN_WIDTH = 15.354331
FOCAL_VIEW = 78.0
 
"""Checks values integrity. If length of parameters of list equals 5 returns True."""
def receive(values):
	if len(values) == 5:
        	return True

"""Performs calculation on each region of interest found on the image (bouys and posts). 
    Keyword arguments:
    rois -- List of lists with description values of the ROIS, one ROI list e.g  Object ID,x1,y1,x2,y2.
    Return -- Distances, Angles, Dominant color of each ROI.
"""

def get_distances(rois):
   
	focalLength = initializeFocalLength(rois)
	for i in range(len(rois)):
		width = int(rois[i][3] - rois[i][1])
		inches = distance2camera(KNOWN_WIDTH, focalLength, width)
		angle = angle2camera(x1,y1,x2,y2)
		print ("Distance to object " + i + "is "  +  inches  + " inches.")
		print ("Angle to object " + i + "is "  +  angle  + " angle.")
		#cv2.putText(image, str(round(inches,1)), (int(rois[i][2]),int(rois[i][3])), cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0) ,1)


"""Function to obtain distances."""
def distance2camera(C_WIDTH,C_FL,PIX_WIDTH):
	#compute and return the distance from the maker to the camera
	return (C_WIDTH*C_FL)/PIX_WIDTH

""" Initialize  the focal length of the camera."""
def initializeFocalLength(rois):

	width = int(rois[0][3] - rois[0][1])
	return (width * KNOWN_DISTANCE) / KNOWN_WIDTH


def angle2camera(x1,y1,x2,y2):
	pixel = (x1+(x2-x1))/2
	preangle = (pixel*FOCAL_VIEW)/1280
	return 0 - ((FOCAL_VIEW/2) - preangle)


"""
Print ROI's parameters.
def print(rois):
	
	for row in rois:
   		for val in row:
        		print('{:4}'.format(val))
    		print('\n')
"""


	
