import cv2
import numpy as np
#import deepnn as net
#import pytesseract as pt

def crop_aspect_center(img, aspect):
    '''Crops the image to the selected aspect ratio minimizing the lost area'''
    ow, oh = img.shape

    w = int(oh / aspect)
    h = int(ow * aspect)

    dw = ow - w
    dh = oh - h

    if dw > dh:
        off = int(dw // 2)
        return img[off:w,:]
    
    off = int(dh // 2)

    return img[:,off:h]

def search_number(img):
    minVal=50
    maxVal=100
    contourAreaThresh = 150
    white = [255,255,255]
    width, height, _ = img.shape
    size = (width, height, 1)
    target_size = (25, 35)
    target_aspect = float(target_size[0]) / float(target_size[1])

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny=cv2.Canny(img,minVal,maxVal,True)
    
    _, contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
    
    contour_img = np.zeros(size, dtype=np.uint8)

    for contour in contours:
        if cv2.contourArea(contour) > contourAreaThresh:
            cv2.drawContours(contour_img, [contour], 0, white, cv2.FILLED)

    inverted = cv2.bitwise_not(contour_img)
    inverted = cv2.resize(crop_aspect_center(inverted, target_aspect), target_size)

    cv2.namedWindow('contours', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('contours', 600, 600)
    cv2.imshow('contours', inverted)
    cv2.waitKey()

    return inverted

def search_display(img, template):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    min_matches = 10

    FLANN_INDEX_LSH = 6
    index_params= dict(
            algorithm = FLANN_INDEX_LSH,
            table_number = 6, # 12
            key_size = 12,     # 20
            multi_probe_level = 1 # 2
    )

    orb = cv2.ORB_create(edgeThreshold=10, patchSize=10)
    matcher = cv2.FlannBasedMatcher(index_params, dict())
    
    tkp, tdes = orb.detectAndCompute(template, None)
    qkp, qdes = orb.detectAndCompute(img, None)

    matches = matcher.knnMatch(qdes,tdes,2)

    good = []

    # ratio test as per Lowe's paper
    for m,n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > min_matches:
	src_pts = np.float32([ qkp[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
	dst_pts = np.float32([ tkp[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
	M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
	matchesMask = mask.ravel().tolist()
	h,w,d = img1.shape
	pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
	dst = cv.perspectiveTransform(pts,M)
	img = cv.polylines(img,[np.int32(dst)],True,255,3, cv.LINE_AA)
    else:
	print( "Not enough matches are found - {}/{}".format(len(good), min_matches) )
	matchesMask = None

    match_img = cv2.drawMatches(img,qkp,template,tkp,good,None, flags=2, matchesMask=matchesMask)

    cv2.namedWindow('matches', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('matches', 600, 600)
    cv2.imshow('matches', match_img)
    cv2.waitKey()

    return 0

def number_recognition(img):
    net.make_graph(img)

def main():
    img = cv2.imread('test.jpg')
    template = cv2.imread('test-crop.jpg')
    #display = search_display(img, template)
    number = search_number(template)
    #print(number_recognition(number))

if __name__ == '__main__':
    main()
