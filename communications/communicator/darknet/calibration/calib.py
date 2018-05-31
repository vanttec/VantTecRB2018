import numpy as np
import cv2
from glob import glob
import os
import sys
from datetime  import datetime


def calibration():

	#Termination criteria
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

	#Checkboard size
	cbrow = 8
	cbcol = 6

	#Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
	objp = np.zeros((cbrow*cbcol,3), np.float32)
	objp[:,:2] = np.mgrid[0:cbcol,0:cbrow].T.reshape(-1,2)

	#Arrays to store object points and image points from all the images.
	objpoints = [] # 3d point in real world space
	imgpoints = [] # 2d points in image plane.

	images = glob('sample_images/*.jpg')

	for fname in images:
		img = cv2.imread(fname)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

		#Find the chess board corners
		ret, corners = cv2.findChessboardCorners(gray, (cbcol,cbrow),None)

		#If found, add object points, image points (after refining them)
		if ret == True:
		objpoints.append(objp)

		corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		imgpoints.append(corners2)

		#Draw and display the corners
		img = cv2.drawChessboardCorners(img, (cbcol,cbrow), corners2,ret)
	
		#cv2.imshow('img',img)
		#cv2.waitKey(100)


	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

	#Uncomment this for displa and save image before calibration
	#Show image before calibration
	#img = cv2.imread('CalibImg/1.jpg')
	#cv2.imshow('img_before',img)
	#cv2.imwrite(os.getcwd() +'/beforecalib.jpg',img)


	#Get new optimal camera matrix
	h,  w = img.shape[:2]
	newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

	data_calib = []
	data_calib.append(mtx)
	data_calib.append(dist)
	data_calib.append(None)
	data_calib.append(newcameramtx)

	return data_calib


def undistorted_image(img,data_calib):
	#Uncomment this for reading from videocamera

		mtx = data_calib[0]
		dist = data_calib[1] 
		newcameramtx = data_calib[3] 
	'''
	#Undistort video
	cap = cv2.VideoCapture(0)
	while(True):
		# Capture frame-by-frame
		ret, distort = cap.read()
		frame = cv2.undistort(distort, mtx, dist, None, newcameramtx)
		# Display the resulting frame
		cv2.imshow('video',frame)
	   
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break
	'''

	#Process competition images
	#for fn in glob('Dataset/Boat/*.png'):
		#Read image
		#ret, img = cap.read()
		#Undistort
		new_image = cv2.undistort(img, mtx, dist, None, newcameramtx)
		return new_image
		#Display image
		#cv2.imshow('video',frame)
		#Save image
		#filename = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.png'
		#cv2.imwrite(cwd  + '/HSV/'  + filename, frame)	 
		#cv2.waitKey(100)


	#Optional
	'''
	#Crop the image
	x,y,w,h = roi
	dst = dst[y:y+h, x:x+w]
	cv2.imwrite(os.getcwd() +'/calibresult.jpg',dst)
	cv2.destroyAllWindows()
	'''


