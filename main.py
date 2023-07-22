import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import numpy
import math
from time import  sleep

# from utilities import *

#instantating the detector object
ObjetHandDetector=HandDetector(detectionCon=0.8,maxHands=1)


# Getting the image from the WebCam
cap =cv.VideoCapture(0)
# wCam, hCam = 100, 100
# cap.set(3,wCam)
# cap.set(4,hCam)
#getting the video

while True:
    ret,frame=cap.read()
    hands, img = ObjetHandDetector.findHands(frame)
    # try :
    #     print(hands[8])
    # except :
    #     print("nothing now")
    if len(hands):
        listPositions = hands[0]
        points = listPositions["lmList"]
        UpFinger = points[8]
        DownFinger = points[4]
        UpFingerShrink = UpFinger[0:2]
        DownFingerShrink=DownFinger[0:2]
        projections=[]
        for a, b in zip(UpFingerShrink, DownFingerShrink):
            projections.append(a - b)
        distance=pow(projections[0],2)+pow(projections[1],2)
        print(distance)
        cv.circle(frame,tuple(UpFingerShrink),radius=5,color=(255,0,0),thickness=-1)
        cv.circle(frame, tuple(DownFingerShrink), radius=5, color=(255, 0, 0), thickness=-1)




    cv.imshow("Output", frame)
    if cv.waitKey(10)&0xFF==ord('q'):
        break
cap.release()
cv.destroyAllWindows()









