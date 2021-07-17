'''
Author: goog
Date: 2021-07-16 10:51:01
LastEditTime: 2021-07-17 21:20:04
LastEditors: goog
Description: 
FilePath: /GithubSyn/bilibili_opencv/HandMarkRecognition/VolumeControlAdvance.py
Time Limit Exceeded!
'''
import cv2
import time
import numpy as np
import HandTrackingModule as htm
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

# 手掌检测器类
detector = htm.handDetector(detectionCon=0.7, maxHands=1)

# 音量控制
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255, 0, 0)

while True:
    success, img = cap.read()

    # Find Hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)
    if len(lmList) != 0:

        # Filter based on size
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100 # 计算手部框的面积
        # print(area)
        if 250 < area < 1000: # 当手掌正常展开才能进行识别，过滤不正常手的状态

            # Find Distance between index and Thumb
            length, img, lineInfo = detector.findDistance(4, 8, img) # 获取距离，图像，坐标信息
            # print(length)

            # Convert Volume 转化为音量值
            volBar = np.interp(length, [50, 200], [400, 150])
            volPer = np.interp(length, [50, 200], [0, 100])

            # Reduce Resolution to make it smoother
            smoothness = 10
            volPer = smoothness * round(volPer / smoothness) # 舍去volPer的个位，稳定，是音量都是10的倍数

            # Check fingers up
            fingers = detector.fingersUp() # 判断手指状态
            #print(fingers)

            # If pinky is down set volume
            if not fingers[4]: # 小指弯曲设置改变音量
                volume.SetMasterVolumeLevelScalar(volPer / 100, None) # 设置音量
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

    # Drawings
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3) # 音量框
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED) # 实际音量
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3) # 显示音量百分比
    cVol = int(volume.GetMasterVolumeLevelScalar() * 100) # 显示当前音量
    cv2.putText(img, f'Vol Set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, colorVol, 3)

    # Frame rate 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)