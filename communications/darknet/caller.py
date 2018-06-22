import time
from random import randint
import numpy as np
import cv2
from glob import glob
import os
import sys
from distances.path import get_rois_data
from darknet import execute
from PIL import Image

def parse_data(data):
    results = []
    for val in data:
        if val[0] == 'b':
            results.append([1, val[2][0], val[2][2], val[2][1], val[2][3]])
        else:
            results.append([0, val[2][0], val[2][2], val[2][1], val[2][3]])
    return results


def main_caller():
    '''Main function to be threaded to call darknet and and get images'''
    #CALL METHOD FOR CAMERA CALIBRATION, receives a list with parameters for image undistortion.
    data_calib = calibration()
    print(data_calib)
    set_up = True
    num = 0
    img_path = '/home/vantec/Documents/VantTecRB2018/communications/darknet/Competencia/*.jpg'
    image_list = [cv2.imread(file) for file in glob(img_path)]
    #AQUI SE ARMA LA CARNita ASAdiuxx
    while True:
        print('-------DATOS DARKNET------')
        #execute, send image and datos para undistort la imagen(camera calibration), esto ultimo lo hace la funcion execute
        data = execute(data_calib, set_up, num)
        #data = execute(data_calib, set_up, num)
        print(data)

        if data is not None:
            data = parse_data(data)
            print(data)
            distances = get_rois_data(data) 
            print(distances)
        else:
            print('---------Nothing detected------------')
            #obtain_data()
        set_up = False
        num += 1

'''#Pruebas
def main(data_calib,images):
    #AQUI SE ARMA LA CARNita ASAdiuxx
    while True:
        print('-------DATOS DARKNET------')
        #execute, send image and datos para undistort la imagen(camera calibration), esto ultimo lo hace la funcion execute
        data = execute(data_calib,images.pop())
        print(data)
        if len(data):
            data = parse_data(data)
            print(data)
            distances = get_rois_data(data) 
            print(distances)
        else:
            print('---------Nothing detected------------')
            #obtain_data()

'''

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

    images = glob('/home/vantec/Documents/VantTecRB2018/communications/darknet/sample_images/*.jpg')

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
        

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    #Get new optimal camera matrix
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))



    data_calib = []
    data_calib.append(mtx)
    data_calib.append(dist)
    data_calib.append(None)
    data_calib.append(newcameramtx)

    return data_calib

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

main_caller()
