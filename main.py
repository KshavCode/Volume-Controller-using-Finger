import mediapipe as mp
import time 
import cv2 as cv
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

# Initialization
capture = cv.VideoCapture(0)
mpHand1 = mp.solutions.hands
mpHand2 = mpHand1.Hands()
mpDraw = mp.solutions.drawing_utils
startTime = 0
volumeInt = 0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
currentVolume = int(volume.GetMasterVolumeLevel())
oldVolume = 0
minVol, maxVol, _ = volume.GetVolumeRange()             # -63 to 0
while True : 
    success, img = capture.read()
    h, w, c = img.shape
    startLine = 40
    endLine = w-40
    lengthLine = endLine-startLine
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = mpHand2.process(imgRGB)
    if results.multi_hand_landmarks:
        for points in results.multi_hand_landmarks:
            for index, loc in enumerate(points.landmark) : 
                if index==4:
                    cx, cy = int(loc.x*w), int(loc.y*h)
                    if volumeInt != int((cx/lengthLine)*100):
                        volumeInt = int((cx/lengthLine)*100)
                        if volumeInt >= 100 :
                            volumeInt = 100
                        elif volumeInt <= 3 :
                            volumeInt = 3
                        currentVolume = volumeInt/100*(maxVol-minVol)+minVol
                        oldVolume = volume.SetMasterVolumeLevel(currentVolume, None)
                        
            mpDraw.draw_landmarks(img, points, mpHand1.HAND_CONNECTIONS)
    
    cv.putText(img, str(volumeInt), (int(volumeInt/100*lengthLine-10), h//2-20), cv.FONT_ITALIC, 1, (255,255,255), 2)
    cv.circle(img, (int(volumeInt/100*lengthLine), h//2), 20, (255, 200, 150), cv.FILLED)
    endTime = time.time()
    fps:int = int(1/(endTime-startTime))
    startTime = endTime
    cv.putText(img, f"FPS: {str(fps)}", (10, 50), cv.FONT_ITALIC, 1.5, (255,255,0), 3)
    cv.line(img, (startLine, h//2), (lengthLine, h//2), (0, 255, 250), 4)
    cv.imshow("Video", img)
    cv.waitKey(1)

