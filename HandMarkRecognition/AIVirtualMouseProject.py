'''
Author: goog
Date: 2021-07-17 22:18:26
LastEditTime: 2021-07-17 22:36:56
LastEditors: goog
Description: 
FilePath: /GithubSyn/bilibili_opencv/HandMarkRecognition/AIVirtualMouseProject.py
Time Limit Exceeded!
'''


import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

##########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingersUp() # 获取手指状态
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0: # 食指伸直，中指弯曲
            # 5. Convert Coordinates 转化为屏幕坐标
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values 相对于上次移动的距离 平滑+上次移动距离
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse  # 坐标切换，电脑屏幕的原点位置在左下边， 而detector获取的左边原点在左上
            autopy.mouse.move(wScr - clocX, clocY) 
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY # 记录上次位置

        # 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1: # 食指和中指伸直间距大于40 点击
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # print(length)
            # 10. Click mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
