import numpy as np
import cv2
from matplotlib import pyplot as plt
import argparse
import datetime

start = datetime.datetime.now()

parser = argparse.ArgumentParser(description='Sift sample')
parser.add_argument('-r','--ref', help='reference image', required=True)
parser.add_argument('-i','--img', help='imput image', required=True)
args = vars(parser.parse_args())
img1 = cv2.imread(args["ref"],0)          # queryImage
img2 = cv2.imread(args["img"],0)          # queryImage

# img1 = cv2.imread('box.png',0)          # queryImage
# img2 = cv2.imread('box_in_scene.png',0) # trainImage
# img1 = cv2.imread('ref.png',0)
# img2 = cv2.imread('photo.jpg',0)

# Initiate SIFT detector
#sift = cv2.SIFT()
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

# Apply ratio test
good = []
for m,n in matches:
    # print "dist: " + str(m.distance) + " < 0.75*" + str(n.distance) + " => " + str(m.distance < 0.75*n.distance)
    if m.distance < 0.75*n.distance:
        good.append([m])
stop = datetime.datetime.now()
delta = stop - start
print '' + str(int(delta.total_seconds() * 1000)) + ' ms, ' +  str(len(good)) + " matchs"


# cv2.drawMatchesKnn expects list of lists as matches.
# img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good, None, flags=2)
# plt.imshow(img3),plt.show()
