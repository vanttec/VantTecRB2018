"""	
	OVER-ALL METHODS DESCRIPTIONS.

	Color detection.- Kmeans clustering algorithm.
	Distances to objects.- Triangle Similarity for Object/Marker to Camera Distance.
	Angles to objects.-
"""

# import the necessary packages
import random
import os
import  sys
import cv2
import numpy as np
from PIL import Image
from glob import glob
from datetime  import datetime
from skimage import io, color,exposure
from skimage.color import rgb2lab,deltaE_cie76
from matplotlib import pyplot as plt


"""
	KNOWN_DISTANCE -- initialize the known distance from the camera to the object(bouy,inches)

	KNOWN_WIDTH    -- initialize the known object width, which in this case is 15.35 for the competitions bouy.
					  	https://www.boatfendersdirect.co.uk/products/75-a2-polyform-buoy-20-x-16.html

	FOCAL_VIEW     -- the field of vision of the camera, derived from the diagonal FOV 78 degrees and an aspect ratio of 16:9 : 70.42 degrees. 
		
					  	https://stackoverflow.com/questions/25088543/estimate-visible-bounds-of-webcam-using-diagonal-fov?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
					  	http://vrguy.blogspot.com/2013/04/converting-diagonal-field-of-view-and.html

    WIDTH_DIM      -- dimensions of video frame
						720 x 1280 
"""

KNOWN_DISTANCE = 78.7402 #10.0   
KNOWN_WIDTH = 7.87402    #15.354331 
FOCAL_VIEW = 70.42       
WIDTH_DIM = 1280      




# check for values'integrity. return 1 if length of params is the expected.
def receive(values):
	
	if len(values) == 5:
        	return True


# bouy 1  post 0 [id, x1,y1,x2,y2]
# performs calculation on each region of interest found on the image (bouys and posts). 
# param: rois -- list of lists with description values for each roi [ID,x1,y1,x2,y2]
# return -- distances, angles, dominant color for each roi.
def get_rois_data(rois):

	
	#create output list of lists
	if not rois:
		return False
	
	#number of rois
	rowLength = len(rois)
	#meters,angles,color
	colLength = 3 
	output = [[[0] for i in range(colLength)] for i in range(rowLength)]

	#initialize focal length x2-x1
	width = int(rois[0][3] - rois[0][1])
	focalLength = (width * KNOWN_DISTANCE) / KNOWN_WIDTH
	
	#iterate through all of the rois row by row.
	for i in range(len(rois)):
	  #compute distances
		# substract x2 - x1
		width = int(rois[i][3] - rois[i][1])  
		#get inches to the object 
		inches = distance2camera(KNOWN_WIDTH, focalLength, width)
		#convert inches to meters
		meters = inches * .0254  
	  #compute angles
		#args x1,y1,x2,y2
		angle = angle2camera(rois[i][1],rois[i][2],rois[i][3],rois[i][4])
		#convert angles to radians 
		radians = angle * 0.0174533
		#trigonometric functions to get objects in a different position than the center
		realmeters = meters/cos(radians)  
	  #compute color of the object if needed(posts)
        #-1 means no color, 0 means red , 1 means green
		#colorofpost = -1  
		#if(rois[0] = 1):
		#	colorofpost = getColor(rois[i][1],rois[i][2],rois[i][3],rois[i][4],rois[i][5])  
	  #save results
		output[i][0] = realmeters 
		output[i][1] = radians
		#output[i][2] = colorofpost
		output[i][2] = 1
	  #print information for debugging
		print ("Distance to object " + str(i) + " is "  +  str(realmeters)  + " meters.")
		print ("Angle to object "    + str(i) + " is "  +  str(radians)   + " radians.")
		#optional put text in image
		#cv2.putText(image, str(round(inches,1)), (int(rois[i][2]),int(rois[i][3])), cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0) ,1)
    #return the results

	return output
	#print("Success")


# function to obtain distances to rois.
def distance2camera(C_WIDTH,C_FL,PIX_WIDTH):
	#Compute and return the distance from the maker to the camera
	return (C_WIDTH*C_FL)/PIX_WIDTH


# gets angle to camera
def angle2camera(x1,y1,x2,y2):
	pixel = (x1+(x2-x1))/2  #gets center pixel of roi
	preangle = (pixel*FOCAL_VIEW)/WIDTH_DIM
	return 0 - ((FOCAL_VIEW/2) - preangle)


# print ROI's parameters.
def prints(rois):
	
	for row in rois:
   		for val in row:
        		print('{:4}'.format(val))

 
class Cluster(object):

    def __init__(self):
        self.pixels = []
        self.centroid = None

    def addPoint(self, pixel):
        self.pixels.append(pixel)

    def setNewCentroid(self):

        R = [colour[0] for colour in self.pixels]
        G = [colour[1] for colour in self.pixels]
        B = [colour[2] for colour in self.pixels]

        R = sum(R) / len(R)
        G = sum(G) / len(G)
        B = sum(B) / len(B)

        self.centroid = (R, G, B)
        self.pixels = []

        return self.centroid


class Kmeans(object):

    def __init__(self, k=2, max_iterations=5, min_distance=5.0, size=200):
        self.k = k
        self.max_iterations = max_iterations
        self.min_distance = min_distance
        self.size = (size, size)

    def run(self, image):
        self.image = image
        self.image.thumbnail(self.size)
        self.pixels = np.array(image.getdata(), dtype=np.uint8)

        self.clusters = [None for i in range(self.k)]
        self.oldClusters = None

        randomPixels = random.sample(self.pixels, self.k)

        for idx in range(self.k):
            self.clusters[idx] = Cluster()
            self.clusters[idx].centroid = randomPixels[idx]

        iterations = 0

        while self.shouldExit(iterations) is False:

            self.oldClusters = [cluster.centroid for cluster in self.clusters]

            print(iterations)

            for pixel in self.pixels:
                self.assignClusters(pixel)

            for cluster in self.clusters:
                cluster.setNewCentroid()

            iterations += 1


        return [cluster.centroid for cluster in self.clusters]

    def assignClusters(self, pixel):
        shortest = float('Inf')
        for cluster in self.clusters:
            distance = self.calcDistance(cluster.centroid, pixel)
            if distance < shortest:
                shortest = distance
                nearest = cluster

        nearest.addPoint(pixel)

    def calcDistance(self, a, b):

        result = np.sqrt(sum((a - b) ** 2))
        return result

    def shouldExit(self, iterations):

        if self.oldClusters is None:
            return False

        for idx in range(self.k):
            dist = self.calcDistance(
                np.array(self.clusters[idx].centroid),
                np.array(self.oldClusters[idx]))
            
            if dist < self.min_distance:
                return True

        if iterations <= self.max_iterations:
            return False

        return True

    # The remaining methods are used for debugging
    def showImage(self):
        self.image.show()

    def showCentroidColours(self):

        for cluster in self.clusters:
            image = Image.new("RGB", (200, 200), cluster.centroid)
		#print len(self.pixels)
        #image.show()

    def showClustering(self):

        localPixels = [None] * len(self.image.getdata())

        for idx, pixel in enumerate(self.pixels):
                shortest = float('Inf')
                for cluster in self.clusters:
                    distance = self.calcDistance(cluster.centroid, pixel)
                    if distance < shortest:
                        shortest = distance
                        nearest = cluster

                localPixels[idx] = nearest.centroid

        w, h = self.image.size
        localPixels = np.asarray(localPixels)\
            .astype('uint8')\
            .reshape((h, w, 3))

        colourMap = Image.fromarray(localPixels)
        #colourMap.show()



def displayImage(screen, px, topleft, prior):

	# ensure that the rect always has positive width, height
	x, y = topleft
	width =  pygame.mouse.get_pos()[0] - topleft[0]
	height = pygame.mouse.get_pos()[1] - topleft[1]
	if width < 0:
		x += width
		width = abs(width)
	if height < 0:
		y += height
		height = abs(height)

	# eliminate redundant drawing cycles (when mouse isn't moving)
	current = x, y, width, height
	if not (width and height):
		return current
	if current == prior:
		return current

	# draw transparent box and blit it onto canvas
	screen.blit(px, px.get_rect())
	im = pygame.Surface((width, height))
	im.fill((128, 128, 128))
	pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
	im.set_alpha(128)
	screen.blit(im, (x, y))
	pygame.display.flip()

	# return current box extents
	return (x, y, width, height)



def setup(path):
    px = pygame.image.load(path)
    screen = pygame.display.set_mode( px.get_rect()[2:] )
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px


def mainLoop(screen, px):

 
	topleft = bottomright = prior = None
	n=0
	while n!=1:

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				if not topleft:
				    topleft = event.pos
				else:
				    bottomright = event.pos
				    n=1
				if topleft:
					prior = displayImage(screen, px, topleft, prior)
	return ( topleft + bottomright )




def ROI(fn):

	input_loc = fn
	screen, px = setup(input_loc)
	left, upper, right, lower = mainLoop(screen, px)

	#ROI Ensure output rect always has positive width, height
	if right < left:
		left, right = right, left
	if lower < upper:
		lower, upper = upper, lower

	im = Image.open(input_loc)
	return left,upper,right,lower




def getColor(left,upper,right,lower,fn):

	original = cv2.imread(fn)
	print(left,upper,right,lower)
	centroidx = int(left + ((right-left)/2))
	centroidy = int(upper + ((lower-upper)/2))
	heigth = lower - upper
	width = right - left
	shiftright = int((width/2)/5)
	shiftleft =  int((heigth/2)/5)
	left = centroidx - shiftright
	right = centroidx + shiftright
	upper = centroidy - shiftleft
	lower = centroidy + shiftleft
	print(left,upper,right,lower)
	print(centroidx)
	print(centroidy)

	#Crop ROI 
	image_obj = Image.open(fn)
	coords = (left,upper,right,lower)
	cropped_image = image_obj.crop(coords)
	#cropped_image.show()
	#Run Kmeans
	k = Kmeans()
	result = k.run(cropped_image)
	print(result)
	



