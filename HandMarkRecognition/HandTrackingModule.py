"""
Hand Tracing Module
By: Murtaza Hassan
conmmeted by: goog
MediaPipe Hands简介：
1. 它利用机器学习可以识别出单帧图片中手部21个3D关键点
2. 桌面端可以达到SOTA
3. 手机端到达实时的效果
4. 支持多个手掌检测 

5. 它由手掌检测器（平均精度95.7%）和手部关键点检测器组成

"""

import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands # 加载 MediaPipe Hands文件
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
        self.detectionCon, self.trackCon) # 初始化Hands模块 设置图片输入为视频流处理 识别最多手数目 手部检测置信 手部关键点置信
        self.mpDraw = mp.solutions.drawing_utils # 记载MediaPipe自带绘图工具
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 通道转化为RGB
        self.results = self.hands.process(imgRGB) # 两个对象 MULTI_HAND_LANDMARKS MULTI_HANDEDNESS
        """
        MULTI_HAND_LANDMARKS
        输出包含每个手的(x,y)坐标、z(深度)
        landmark {
            x: 0.22855499386787415
            y: 0.8988580703735352
            z: -0.053629666566848755
        }

        MULTI_HANDEDNESS
        左手/右手（label）：score（置信）

        """
        # print(self.results.multi_hand_landmarks)

        # 正是因为self.mode 设置为false ， 故输入一张图片会检测出一个landmark list
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # 将手部21个关键点绘制连接出来
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
                    # self.mpHands.HAND_CONNECTIONS代表手部21个关键点 详细(https://github.com/google/mediapipe/blob/master/mediapipe/python/solutions/hands.py)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo] # 获取图片中第组handmark信息
            for id, lm in enumerate(myHand.landmark): # 遍历21个handmark
                # print(id, lm)
                h, w, c = img.shape # 摄像头图像高宽
                cx, cy = int(lm.x * w), int(lm.y * h) # 反归一化
                xList.append(cx)
                yList.append(cy) # 保存21handmark xy坐标
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED) # 21个点描绘出, 蓝色
            xmin, xmax = min(xList), max(xList) # 获取最大最下x
            ymin, ymax = min(yList), max(yList) # 获取最大最小y
            bbox = xmin, ymin, xmax, ymax # 作为手部框取坐标

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
            (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2) # 绘制方框框中手掌
        #print(len(self.lmList))
        return lmList, bbox # 返回坐标及框坐标

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img, draw=True):

        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img)
        #print(len(lmList))
        if len(lmList) >= 4:
            
            print(lmList[4])
    
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime # 计算帧率
        
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
        (255, 0, 255), 3) # 显示帧率
        
        cv2.imshow("Image", img) # 显示画面

        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
