import mediapipe as mp
import time 
import cv2 as cv

# Initialization
capture = cv.VideoCapture(0)
mpHand1 = mp.solutions.hands
mpHand2 = mpHand1.Hands()
mpDraw = mp.solutions.drawing_utils
volume = 0
startTime = 0
while True : 
    success, img = capture.read()
    h, w, c = img.shape
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = mpHand2.process(imgRGB)
    if results.multi_hand_landmarks:
        for points in results.multi_hand_landmarks:
            for index, loc in enumerate(points.landmark) : 
                if index==4:
                    cx, cy = int(loc.x*w), int(loc.y*h)
                    if cx <= 20 :
                        cx = 20
                    if cx >= 600:
                        cx = 600
                    if int((cx/w)*100) != volume:
                        volume = int((cx/w)*100)

            mpDraw.draw_landmarks(img, points, mpHand1.HAND_CONNECTIONS)
    
    cv.putText(img, str(volume), (int(volume/100*w-10), h//2-20), cv.FONT_ITALIC, 1, (255,255,255), 2)
    cv.circle(img, (int(volume/100*w), h//2), 20, (255, 200, 150), cv.FILLED)
    endTime = time.time()
    fps:int = int(1/(endTime-startTime))
    startTime = endTime
    cv.putText(img, f"FPS: {str(fps)}", (10, 50), cv.FONT_ITALIC, 1.5, (255,255,0), 3)
    cv.line(img, (20, h//2), (w-40, h//2), (0, 255, 250), 4)
    cv.imshow("Video", img)
    cv.waitKey(1)

