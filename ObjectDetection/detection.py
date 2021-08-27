'''
Author: goog
Date: 2021-08-27 10:29:11
LastEditTime: 2021-08-27 10:39:16
LastEditors: goog
Description: 
FilePath: /GithubSyn/bilibili_opencv/ObjectDetection/detection.py
Time Limit Exceeded!
'''
import cv2
thres = 0.45 # Threshold to detect object 置信概率

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,70)

classNames= []
classFile = 'coco.names'
# 读取类别信息
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
print(classNames)
# 网络配置
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
# 网络权重
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
# 设置网络输入尺寸, 归一化, 均值 ，交换RB通道位置
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    success,img = cap.read()
    # 检测
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    # 获取类别与框
    print(classIds,bbox)

    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            cv2.rectangle(img,box,color=(0,255,0),thickness=2) # 给目标加框
            cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
            cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2) # 目标打上类别
            cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
            cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2) # 目标打上置信概率

    cv2.imshow("Output",img)
    cv2.waitKey(1)