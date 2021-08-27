'''
Author: goog
Date: 2021-08-27 08:45:05
LastEditTime: 2021-08-27 09:08:59
LastEditors: goog
Description: 
FilePath: /GithubSyn/bilibili_opencv/FingerDount/count.py
Time Limit Exceeded!
'''
import cv2
import time
import sys
sys.path.append("..")
from HandMarkRecognition import HandTrackingModule as htm


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# folderPath = "FingerImages"
# myList = os.listdir(folderPath)
# print(myList)
# overlayList = []
# for imPath in myList:
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     # print(f'{folderPath}/{imPath}')
#     overlayList.append(image)

# print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
# 大拇指尖 食指指尖 中指指尖 无名指指尖 小指指尖

while True:
    success, img = cap.read()
    # 绘制手部关键点并连接
    img = detector.findHands(img)
    # 获取21个关键点坐标
    lmList, _ = detector.findPosition(img, draw=False)
    # print(len(lmList))

    if len(lmList) == 21:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            # 指尖y坐标比指尖向下两个单位y坐标小 则说明手指伸直，计数加一
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        # h, w, c = overlayList[totalFingers - 1].shape
        # img[0:h, 0:w] = overlayList[totalFingers - 1]

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)