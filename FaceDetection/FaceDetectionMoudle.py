'''
Author: goog
Date: 2021-07-17 22:52:44
LastEditTime: 2021-07-21 16:59:41
LastEditors: goog
Description: 
FilePath: /GithubSyn/bilibili_opencv/FaceDetection/FaceDetectionMoudle.py
Time Limit Exceeded!
'''
import cv2
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, minDetectionCon=0.5):

        self.minDetectionCon = minDetectionCon # 检测到人脸置信

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon) # 加载人脸检测模块
        # 参数说明
        # min_detection_confidence
        # 0-1 代表识别为人脸的置信 ， 默认0.5
        # model_selection
        # 默认为0 代表识别两米内的人脸 （可选1 代表5米内的人脸）
    def findFaces(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # BGR-》RGB
        self.results = self.faceDetection.process(imgRGB) # 获取检测结果
        print(self.results)
        bboxs = []
        if self.results.detections:
            # 输出为
            """
            a bounding box and 6 key points (right eye, left eye, nose tip, mouth center, right ear tragion, and left ear tragion)
            """
            # 边界框的四个值 xmin width ymin height
            # 六个面部关键点 右眼 左眼 鼻子 嘴巴 右耳 左耳
            for id, detection in enumerate(self.results.detections): # 可检测到多个人脸
                bboxC = detection.location_data.relative_bounding_box # 获取检测的位置信息
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih) # 反归一化
                bboxs.append([id, bbox, detection.score])
                if draw:
                    img = self.fancyDraw(img,bbox)

                    cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                            (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 2)
        return img, bboxs

    def fancyDraw(self, img, bbox, l=30, t=5, rt= 1):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h

        cv2.rectangle(img, bbox, (255, 0, 255), rt) # 人脸框
        # Top Left  x,y
        cv2.line(img, (x, y), (x + l, y), (255, 0, 255), t) # 左上部 标记
        cv2.line(img, (x, y), (x, y+l), (255, 0, 255), t)
        # Top Right  x1,y
        cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 255), t) 
        cv2.line(img, (x1, y), (x1, y+l), (255, 0, 255), t)
        # Bottom Left  x,y1
        cv2.line(img, (x, y1), (x + l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - l), (255, 0, 255), t)
        # Bottom Right  x1,y1
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), t)
        return img


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()
    while True:
        success, img = cap.read()
        img, bboxs = detector.findFaces(img)
        print(bboxs)

        # 帧率
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()