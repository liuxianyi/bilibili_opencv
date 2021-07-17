'''
Author: goog
Date: 2021-07-16 10:50:38
LastEditTime: 2021-07-17 21:13:26
LastEditors: goog
Description: 
FilePath: /GithubSyn/bilibili_opencv/HandMarkRecognition/VolumeControl.py
Time Limit Exceeded!
'''
import cv2
import time
import numpy as np

import HandTrackingModule as htm
# detector = htm.handDetector(detectionCon=0.7)
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# 控制windows音量的组件
# https://github.com/AndreMiras/pycaw

# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0] 
maxVol = volRange[1] # 获取音量范围
vol = 0
volBar = 400
volPer = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img) 
    lmList,_ = detector.findPosition(img, draw=False) # 获取21个坐标xy
    #print(len(lmList))
    if len(lmList) > 8:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2] # 食指指尖xy
        x2, y2 = lmList[8][1], lmList[8][2] # 拇指指尖xy
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 # 中点

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3) # 连接第四个关键点和第八个关键点
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED) # 标记中点

        length = math.hypot(x2 - x1, y2 - y1) # 计算(x1,y1) (x2, y2)两点距离
        # print(length)

        # Hand range 50 - 300
        # Volume Range -65 - 0

        vol = np.interp(length, [50, 300], [minVol, maxVol]) # 线性一维插值, 大概意思：50-300里的length映射为范围为minVOl-maxVol音量的大小为多少
        volBar = np.interp(length, [50, 300], [400, 150]) 
        volPer = np.interp(length, [50, 300], [0, 100])
<<<<<<< HEAD
        print(int(length), vol)
=======
        # print(int(length), vol)
>>>>>>> c3d2402fc9a25e4d259f600d2e68a4baf3016ad6
        volume.SetMasterVolumeLevel(vol, None) # 设置音量

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED) 

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3) # 音量框
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED) # 实际音量
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    # 显示帧率
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)