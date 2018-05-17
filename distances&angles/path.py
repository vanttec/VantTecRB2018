
from glob import glob
import os
import pygame, sys
from PIL import Image
from datetime  import datetime
import cv2
from matplotlib import pyplot as plt
import numpy as np
pygame.init()
from skimage import io, color,exposure
from skimage.color import rgb2lab,deltaE_cie76


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



if __name__ == "__main__":


	#for fn in glob('/home/charlesdickens/Documents/vantTEC/Camera_calibration/Dataset/Boat/*.png'):

          
	   print "DRAW/KEEP DRAWING ... C"
	   print "TO SAVE ... S"
	   print "NEXT PICTURE ... N"
	   print "EXIT ... E"
	   fn = 'tagging.png'
	   original = cv2.imread('tagging.png')
	   count = 1
	   while(1):
		    k = cv2.waitKey(0)
		    cv2.imshow('drawing',original)

		    if k == 99: 
			 cv2.destroyWindow('drawing')
		    	 left,upper,right,lower = ROI(fn)
			 print(left,upper,right,lower)
			 cv2.rectangle(original,(left,upper),(right,lower),(0,255,0),2)
			 cv2.putText(original, str(count), (left,upper), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0) ,1)
			 width = right-left
			 with open("widths.txt", "a") as text_file:
				 text_file.write("%d %d %d %d\n" % (count,width,int(left+(right-left)/2), int(upper+(lower-upper)/2)))
				 count+=1
		    elif k == 115:
			 cv2.destroyWindow('drawing')
			 filename = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.png'
			 output_loc = os.getcwd() + '/' + filename
			 cv2.imwrite(output_loc ,original)
			 pygame.quit()
			 break
		    elif k == 110: 
			 cv2.destroyWindow('drawing')
                         pygame.quit()
			 break
		    elif k==101: 
			cv2.destroyWindow('drawing')
                        pygame.quit()
			exit()
		 

	

