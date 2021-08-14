import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

folderPath = "img"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
#print(len(overlayList))

header = overlayList[4]
drawcolor =(0, 0, 255)
eraserThickness= 50

brushThickness = 20

cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionCon=0.80)
xp, yp = 0, 0
imgCanvas = np.zeros((480, 640, 3), np.uint8)
pTime = 0
cTime = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList)

        x1,y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        #print(fingers)
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

            print("Selection Mode")
            if y1< 63:
                if 125<x1<225:
                    header = overlayList[4]
                    drawcolor =(0, 0, 255)
                elif 275 < x1 < 375:
                        header = overlayList[0]
                        drawcolor = (255, 0, 0)
                elif 400 < x1 < 475:
                        header = overlayList[2]
                        drawcolor = (0, 128, 0)
                elif 525 < x1 < 600:
                        header = overlayList[1]
                        drawcolor = (0, 0, 0)
                elif 0< x1 < 125:
                    header = overlayList[3]
                    cv2.imwrite("untiled.jpg",imgCanvas)
                    cv2.putText(img, 'Imaged Saved',(300,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawcolor, cv2.FILLED)

        if fingers[1] and fingers[2]==False:
            cv2.circle(img, (x1, y1),15, drawcolor, cv2.FILLED)
            print("Draw Mode")
            if xp==0 and yp==0:
                xp, yp = x1, y1

            if drawcolor ==(0,0,0):
                #cv2.line(img, (xp, yp), (x1, y1), drawcolor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, eraserThickness)
            else:

                #cv2.line(img, (xp, yp), (x1, y1), drawcolor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, brushThickness)
            xp, yp = x1, y1
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

    img[0:63, 0:640] = header
    img= cv2.addWeighted(img,0.5,imgCanvas, 0.5, 0)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    #cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)