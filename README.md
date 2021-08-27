<!--
 * @Author: goog
 * @Date: 2021-07-17 09:33:10
 * @LastEditTime: 2021-08-27 13:37:06
 * @LastEditors: goog
 * @Description: #
 * @FilePath: /GithubSyn/bilibili_opencv/README.md
 * Time Limit Exceeded!
-->
# bilibili_opencv
![](./resources/mediapipe_small.png)
## Requirement
🌟 opencv-pyhton  
🌟 mediapipe  
🌟 ctypes  
🌟 pycaw      
🌟 autopy    
## [Face Detection](https://google.github.io/mediapipe/solutions/face_detection.html)
- 6 landmarks   
- multi-face support     

![face detection](./resources/face_detection_android_gpu.gif)
## [Face Mesh](https://google.github.io/mediapipe/solutions/face_mesh.html)
- 468 3D face landmarks  
- real-time 

A detector that operates on the full image and computes face locations and a 3D face landmark model that operates on those locations and predicts the approximate surface geometry via regression.   
![face mesh](./resources/face_mesh_ar_effects.gif)  

[paper🔗](https://arxiv.org/abs/1907.06724)
## [Iris](https://google.github.io/mediapipe/solutions/iris.html)
- iris
- pupil
- eye contours
- real-time
- Through use of iris landmarks, the solution is also able to determine the **metric distance between the subject and the camera** with relative error less than 10%. 
- **Note:** that iris tracking does **not infer the location** at which people are looking, **nor does it provide any form of identity recognition**.      

![iris](./resources/iris_tracking_eye_and_iris_landmarks.png)  

[paper🔗](https://arxiv.org/abs/2006.11341)
## 21 hand landmarks
![hand landmakrs](./resources/hand_landmarks.png)

## Pose
- 33 3D landmark

![pose landmark](./resources/pose_tracking_full_body_landmarks.png)


## Holistic
- integrate
- pose
- face
- hand
- multi-stage pipeline
- 540+ landmark
![](./resources/holistic_pipeline_example.jpg)
步骤：
<ol>
    <li>对整幅图利用pose检测器和landmark检测器实现姿态估计</li>
    <li>利用第一步的landmark获取三部分ROI（1. two hands 2. face）</li>
    <li>使用re-crop改进ROI选取</li>
    <li>裁剪</li>
    <li>使用特定任务模型实现face、hand估计对应的landmark</li>
    <li>合并所有的landmark</li>
</ol>

## selfie Segmentation  
- close(<2m) to the camera
- real time  

<video id="video" controls="" preload="none" poster="作者(图片地址)">
<source id="mp4" src="./resources/selfie_segmentation_web.mp4" type="video/mp4">
</video>

步骤：
<ol>
    <li>two models: general and landscape</li>
    <li>general model: output segmentation mask</li>
    <li>landscape(Background): 1. similar to the general model 2.runs faster</li>
</ol>

## [ObjectDetection](./ObjectDetection)
|类别|class|类别|class|类别|class|类别|class|类别|class|类别|class|类别|class|类别|class|类别|class|类别|class|
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|person|人|bicycle|自行车|car|汽车|motorcycle|摩托车|airplane|飞机|bus|公共汽车|train|火车|truck|卡车|boat|船|traffic light|交通灯|
|fire hydrant|消防栓|street sign|路牌|stop sign|停车标志|parking meter|停车计时器|bench|长凳|bird|鸟|cat|猫|dog|狗|horse|马|sheep|羊|
|cow|牛|elephant|大象|bear|熊|zebra|斑马|giraffe|长颈鹿|hat|帽子|backpack|背包|umbrella|雨伞|shoe|鞋子|eye glasses|眼镜|
|handbag|手提包|tie|领带|suitcase|手提箱|frisbee|飞盘|skis|滑雪板|snowboard|滑雪板|sports ball|运动球|kite|风筝|baseball bat|棒球棒|baseball glove|棒球手套|
|skateboard|滑板|surfboard|冲浪板|tennis racket|网球拍|bottle|瓶子|plate|盘|wine glass|酒杯|cup|杯子|fork|叉子|knife|刀|spoon|勺子|
|bowl|碗|banana|香蕉|apple|苹果|sandwich|三明治|orange|橙子|broccoli|西兰花|carrot|胡萝卜|hot dog|热狗|pizza|披萨|donut|甜甜圈|
|cake|蛋糕|chair|椅子|couch|沙发|potted plant|盆栽|bed|床|mirror|镜子|dining table|餐桌|window|窗户|desk|书桌|toilet|厕所|
|door|门|tv|电视|laptop|笔记本电脑|mouse|鼠标|remote|遥控器|keyboard|键盘|cell phone|手机|microwave|微波炉|oven|烤箱|toaster|烤面包机|
|sink|水槽|refrigerator|冰箱|blender|搅拌机|book|书|clock|时钟|vase|花瓶|scissors|剪刀|teddy bear|泰迪熊|hair drier|吹风机|toothbrush|牙刷|
|hair brush|毛刷|

## [Face Recognition](./FaceAttendance)
```python
import cv2
import numpy as np
import face_recognition
```
本项目face_recognition是一个强大、简单、易上手的人脸识别开源项目，并且配备了完整的开发文档和应用案例，特别是兼容树莓派系统。
[➡️more Details](https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md)





## synchronize bilibili [xiao liu time grocery store](https://space.bilibili.com/144585110)  opencv code
【计算机视觉OpenCV】【中英字幕】Opencv实现手部轮廓识别 [code🔗](https://github.com/liuxianyi/bilibili_opencv/blob/main/HandMarkRecognition/HandTrackingMdule.py) [video🔗](https://www.bilibili.com/video/BV1Hv411n7LK?t=146)  
【计算机视觉OpenCV】「中文字幕」手势控制音量 [code🔗](./HandMarkRecognition/VolumeControl.py) [video🔗](https://www.bilibili.com/video/BV1jK4y1u7AB)   
【计算机视觉OpenCV】「中文字幕」手势控制音量**高级** [code🔗](./HandMarkRecognition/VolumeControlAdvance.py) [video🔗](https://www.bilibili.com/video/BV1qM4y1K7Un)    
【计算机视觉OpenCV】「中文字幕」虚拟鼠标**手指控制电脑鼠标** [code🔗](./HandMarkRecognition/AIVirtualMouseProject.py) [video🔗](https://www.bilibili.com/video/BV1ZV411W7T8)   
【计算机视觉OpenCV】「中文字幕」卷积神经网络实现交通标志识别 [train code🔗](./TrafficSignClassifation/TrainCode.py) [test code🔗](./TrafficSignClassifation/TestCode.py)[video🔗](https://www.bilibili.com/video/BV11U4y1379f) [数据集🔗 提取码: 39q4](https://pan.baidu.com/s/15v14ieSPZntBTDzKVckEgA)   
【计算机视觉OpenCV】「中文字幕」人脸识别实现**出勤率统计** [code🔗](./FaceAttendance/recognition.py) [video🔗](https://www.bilibili.com/video/BV1Dv411J7st)    
【计算机视觉OpenCV】「中文字幕」目标检测**高精度实时** [code🔗](./ObjectDetection/detection.py) [非极大值抑制code🔗](./ObjectDetection/NMSDetection.py)[video🔗](https://www.bilibili.com/video/BV1ZV411H7KS) [训练模型🔗提取码: mvxs](https://pan.baidu.com/s/1gr_2bl8zlYHF6cG-K3JVZw)    
【计算机视觉OpenCV】「中文字幕」实现背景替换**仿照腾讯会议** [<a style="color:red">待更</a>code🔗]() [video🔗](https://www.bilibili.com/video/BV1vM4y1T765/)    
【计算机视觉OpenCV】「中文字幕」FaceMesh**多个人脸 面部468个关键点** [code🔗](./FaceMesh/FaceMeshMoudle.py) [video🔗](https://www.bilibili.com/video/BV1bb4y1r7n7/)  
【计算机视觉OpenCV】「中文字幕」人脸关键点检测**多个人脸 面部六个关键点** [code🔗](./FaceDetection/FaceDetectionMoudle.py)   
【计算机视觉OpenCV】「中文字幕」手指数量识别 [code🔗](./FingerDount/count.py) [video🔗](https://www.bilibili.com/video/BV1Th411z73s/)  
【计算机视觉OpenCV】「中文字幕」创建一个自己的python包 [code🔗<a style="color:red">待更</a>]() [video🔗](https://www.bilibili.com/video/BV1wP4y1t7Hk/)  
【计算机视觉OpenCV】「中文字幕」人脸检测 [code🔗](./FaceDetection/FaceDetectionMoudle.py) [video🔗](https://www.bilibili.com/video/BV1MM4y1N7Zq/)  
【计算机视觉OpenCV】「中文字幕」姿势估计 [code🔗](./PoseEstimation/PoseModule.py) [video🔗](https://www.bilibili.com/video/BV1qy4y1j7Gy/)  

## [MediaPipe Python Github🔗](https://github.com/google/mediapipe/tree/master/mediapipe/python)



