import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import numpy
import math
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
    print(hands)

    cv.imshow("Output",frame)

    if cv.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv.destroyAllWindows()









