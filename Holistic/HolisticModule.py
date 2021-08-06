'''
Author: goog
Date: 2021-08-06 09:27:58
LastEditTime: 2021-08-06 10:10:38
LastEditors: goog
Description: 
FilePath: /GithubSyn/bilibili_opencv/Holistic/HolisticModule.py
Time Limit Exceeded!
'''
import mediapipe as mp
import numpy as np
import cv2
class HolisticModule():

    def __init__(self, mode=False, model_complexity=1,
    smooth=True, detection_con=0.5, tracking_con=0.5) -> None:
        self._holistic = mp.solutions.holistic
        self.holistic = self._holistic.Holistic(mode, model_complexity, smooth, detection_con, tracking_con)
        self.draw_util = mp.solutions.drawing_utils
        self.dic_landmark_pos = {
            'face': self._holistic.FACE_CONNECTIONS,
            'hand': self._holistic.HAND_CONNECTIONS,
            'pose': self._holistic.POSE_CONNECTIONS
        }
    def process(self, image: np.ndarray):
        self.result = self.holistic.process(image)

    def no_result_throw(self):
        if not self.result:
            raise RuntimeError('The medthod prosess was not called! ')

    
    def get_pose_landmarks(self):
        self.no_result_throw()
        return self.result.pose_landmarks

    def get_pose_world_landmarks(self):
        self.no_result_throw()
        return self.result.pose_world_landmarks
    def get_left_hand_landmarks(self):
        self.no_result_throw()
        return self.result.left_hand_landmarks
    def get_right_hand_landmarks(self):
        self.no_result_throw()
        return self.result.right_hand_landmarks
    def get_face_landmarks(self):
        self.no_result_throw()
        return self.result.face_landmarks
    
    def draw_landmark(self, image:np.ndarray, landmark, landmark_pos='face'):
        self.draw_util.draw_landmarks(image, landmark, self.dic_landmark_pos[landmark_pos])


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    


    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue 
            
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        holistic = HolisticModule()
        holistic.process(image)
        face_landmark = holistic.get_face_landmarks()
        holistic.draw_landmark(image, face_landmark, 'face')
        cv2.imshow('holistic', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()