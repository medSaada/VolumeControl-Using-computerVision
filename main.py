import cv2 as cv
import requests
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from cvzone.HandTrackingModule import HandDetector
import numpy
import math
import os
from time import sleep

# from utilities import *

#instantating the detector object
ObjetHandDetector=HandDetector(detectionCon=0.8,maxHands=1)




# Getting the image from the WebCam


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,None)

volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
# print(f"{minVol},{maxVol}")


#getting the video


camera_url = 'http://172.20.10.2:81/stream'
cap=cv.VideoCapture(0)

while True:
    try:
        response = requests.get(camera_url, stream=True)
        if response.status_code == 200:
            bytes_data = bytes()
            for chunk in response.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b + 2]
                    bytes_data = bytes_data[b + 2:]
                    frame = cv.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv.IMREAD_COLOR)

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
                        DownFingerShrink = DownFinger[0:2]
                        projections = []
                        for a, b in zip(UpFingerShrink, DownFingerShrink):
                            projections.append(a - b)
                        distance = pow(projections[0], 2) + pow(projections[1], 2)

                        if distance > 30000:
                            distance = 30000
                        elif distance < 450:
                            distance = 450
                        distance += 1
                        distance = ((distance - 450) / (30000 - 450))
                        # print(f"{int(distance)}")
                        cv.circle(frame, tuple(UpFingerShrink), radius=5, color=(255, 0, 0), thickness=-1)
                        cv.circle(frame, tuple(DownFingerShrink), radius=5, color=(255, 0, 0), thickness=-1)
                        # adapting the normalized value to the function
                        distance = distance * (0 + 64.25) - 64.25
                        # volume.SetMasterVolumeLevel(distance, None)
                        if distance > 0:
                            distance = 0.0
                        print(distance)
                        volume.SetMasterVolumeLevel(distance, None)
                    cv.imshow('ESP32 Camera Stream', frame)
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        break
    except Exception as e:
        print("Error:", e)
        continue

cv.destroyAllWindows()
