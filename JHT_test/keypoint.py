import mediapipe as mp ## 스켈레톤
import pandas as pd ## keypoint간 빠른계산
import numpy as np ## 스켈레톤 다차원배열 구현
from utils import * ## utils 불러오기

class KEYPOINT:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    def angle_of_the_left_arm(self): ## 푸쉬업 (왼쪽 어깨,팔꿈치,손목 각도)
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        l_elbow = detection(self.landmarks, "LEFT_ELBOW")
        l_wrist = detection(self.landmarks, "LEFT_WRIST")
        return calculate_angle(l_shoulder, l_elbow, l_wrist)

    def angle_of_the_right_arm(self): ## 푸쉬업 (오른쪽 어깨,팔꿈치,손목 각도)
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        r_elbow = detection(self.landmarks, "RIGHT_ELBOW")
        r_wrist = detection(self.landmarks, "RIGHT_WRIST")
        return calculate_angle(r_shoulder, r_elbow, r_wrist)

    def angle_of_the_left_leg(self): ## 스쿼트 (왼쪽 허리, 무릎, 발목 각도)
        l_hip = detection(self.landmarks, "LEFT_HIP")
        l_knee = detection(self.landmarks, "LEFT_KNEE")
        l_ankle = detection(self.landmarks, "LEFT_ANKLE")
        return calculate_angle(l_hip, l_knee, l_ankle)

    def angle_of_the_right_leg(self): ## 스쿼트 (오른쪽 허리, 무릎, 발목 각도)
        r_hip = detection(self.landmarks, "RIGHT_HIP")
        r_knee = detection(self.landmarks, "RIGHT_KNEE")
        r_ankle = detection(self.landmarks, "RIGHT_ANKLE")
        return calculate_angle(r_hip, r_knee, r_ankle)

    def angle_of_the_right_spine(self):  ## 스쿼트 + 푸쉬업 (오른쪽 척추(허리, 어깨 목) 각도)
        r_knee = detection(self.landmarks, "RIGHT_KNEE")
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        r_hip = detection(self.landmarks, "RIGHT_HIP")
        return calculate_angle(r_knee, r_shoulder, r_hip, "RIGHT_SPINE")
    
    def angle_of_the_left_spine(self):  ## 스쿼트 + 푸쉬업 (왼쪽 척추(허리, 어깨 목) 각도)
        l_knee = detection(self.landmarks, "LEFT_MOUTH")
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        l_hip = detection(self.landmarks, "LEFT_HIP")
        return calculate_angle(l_knee, l_shoulder, l_hip, "LEFT_SPINE")

    def angle_of_the_elbow(self):
        l_elbow = detection(self.landmarks, "LEFT_ELBOW")
        r_elbow = detection(self.landmarks, "RIGHT_ELBOW")
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        return calculate_angle(l_elbow, l_shoulder, r_elbow)



    def angle_of_the_abdomen(self):
        # calculate angle of the avg shoulder
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        shoulder_avg = [(r_shoulder[0] + l_shoulder[0]) / 2,
                        (r_shoulder[1] + l_shoulder[1]) / 2]

        # calculate angle of the avg hip
        r_hip = detection(self.landmarks, "RIGHT_HIP")
        l_hip = detection(self.landmarks, "LEFT_HIP")
        hip_avg = [(r_hip[0] + l_hip[0]) / 2, (r_hip[1] + l_hip[1]) / 2]

        # calculate angle of the avg knee
        r_knee = detection(self.landmarks, "RIGHT_KNEE")
        l_knee = detection(self.landmarks, "LEFT_KNEE")
        knee_avg = [(r_knee[0] + l_knee[0]) / 2, (r_knee[1] + l_knee[1]) / 2]

        return calculate_angle(shoulder_avg, hip_avg, knee_avg)

