'''
Author: goog
Date: 2021-08-27 11:28:21
LastEditTime: 2021-08-27 13:31:06
LastEditors: goog
Description: 
FilePath: /GithubSyn/bilibili_opencv/FaceAttendance/recognition.py
Time Limit Exceeded!
'''
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
# from PIL import ImageGrab


# 加载文件夹中定义好的要进行识别的人脸图片，为之后检测时做对比提供依据
# ImagesAttendance 文件夹用于装 label人脸，文件名为l人名
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

# face_encodings 面部 编码
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Given an image, return the 128-dimension face encoding for each face in the image.
        # 会找到128维的面部编码信息
        encode = face_recognition.face_encodings(img)[0]
        
        encodeList.append(encode)
    return encodeList


# 添加用户 到csv文件中 如果不存在的话  代表签到了，并记录了签到时间
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'n{name},{dtString}')
 
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

# 获取已定义已知图片-姓名的人 label 的编码信息
encodeListKnown = findEncodings(images)
print('Encoding Complete')
 
cap = cv2.VideoCapture(0)
 
while True:
    success, img = cap.read()
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25) # 并且对图像进行了缩放
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    # 获取当前摄像头前人物的面部边界框信息，以及面部编码信息
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        # Compare a list of face encodings against a candidate encoding to see if they match.
        # A list of True/False values  返回 true or false list值
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace) # 与已经定义好的图片做对比看是否匹配
     
        # Given a list of face encodings, compare them to a known face encoding and get a euclidean distance
        # for each comparison face. The distance tells you how similar the faces are.
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace) # 根据面部编码 计算 欧式距离，代表相似度
        #print(faceDis)
        matchIndex = np.argmin(faceDis)
 
        # 如果相似度最小的且刚好也匹配
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc # 获取面部框
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4 # 这里对应之前对图片imgS进行了1/4的缩放，所以这里坐标进行4倍的放大，才是最终正确的位置
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED) # 定义一块区域显示识别结果
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
 
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)