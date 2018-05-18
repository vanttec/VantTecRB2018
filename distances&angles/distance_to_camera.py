
import numpy as np
import cv2

def distance2camera(C_WIDTH,C_FL,PIX_WIDTH):
	#compute and return the distance from the maker to the camera
	return (C_WIDTH*C_FL)/PIX_WIDTH

# initialize the known distance from the camera to the object, which
# in this case is 10 inches
KNOWN_DISTANCE = 10.0
 
# initialize the known object width, which in this case, the piece of
# paper is 11 inches wide
KNOWN_WIDTH = 12.0
 
# initialize the list of images that we'll be using
IMAGE_PATHS = ['test_distances.png']
 
# load the first image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the paper marker in the image, and initialize
# the focal length
image = cv2.imread(IMAGE_PATHS[0])

#read information about bounding boxes
raw = []
with open('widths.txt','r') as f:
    for line in f:
        raw.append(line.split())

for i in range(13):
    for j in range(4):
        print '{:4}'.format(raw[i][j]),
    print

#initialize  the focal length
focalLength = (float(raw[0][1]) * KNOWN_DISTANCE) / KNOWN_WIDTH

# load the image, find the marker in the image, then compute the
# distance to the marker from the camera
image = cv2.imread(IMAGE_PATHS[0])
print focalLength
#loop over boxes
for i in range(13):
	# then compute the distance to the marker from the camera
	inches = distance2camera(KNOWN_WIDTH, focalLength, float(raw[i][1]))
	print inches
	cv2.putText(image, str(round(inches,1)), (int(raw[i][2]),int(raw[i][3])), cv2.FONT_HERSHEY_SIMPLEX,.5, (0,0,0) ,1)
cv2.imwrite('test.png',image)


