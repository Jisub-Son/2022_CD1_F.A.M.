# import mediapipe as mp ## 스켈레톤
# import pandas as pd ## keypoint간 빠른계산
# import numpy as np ## 스켈레톤 다차원배열 구현
from utils import * ## utils 불러오기

class KEYPOINT:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    def angle_of_the_left_arm(self): ## 푸쉬업 (왼쪽 어깨,팔꿈치,손목 각도)
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        l_elbow = detection(self.landmarks, "LEFT_ELBOW")
        l_wrist = detection(self.landmarks, "LEFT_WRIST")
        if l_shoulder[2] >= 0.8 and l_elbow[2]  >= 0.8 and l_wrist[2] >= 0.8:
            # print("left arm visible")
            return calculate_angle(l_shoulder, l_elbow, l_wrist)
        else:
            return 0

    def angle_of_the_right_arm(self): ## 푸쉬업 (오른쪽 어깨,팔꿈치,손목 각도)
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        r_elbow = detection(self.landmarks, "RIGHT_ELBOW")
        r_wrist = detection(self.landmarks, "RIGHT_WRIST")
        if r_shoulder[2] >= 0.8 and r_elbow[2]  >= 0.8 and r_wrist[2] >= 0.8:
            # print("right arm visible")
            return calculate_angle(r_shoulder, r_elbow, r_wrist)
        else:
            return 0
        
    def angle_of_the_left_spine(self):  ## 푸쉬업 (왼쪽 척추(어깨, 허리, 무릎) 각도)
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        l_hip = detection(self.landmarks, "LEFT_HIP")
        l_knee = detection(self.landmarks, "LEFT_KNEE")
        '''if l_shoulder[2] >= 0.8 and l_hip[2] >= 0.8 and l_knee >= 0.8:
            print("left spine visible")
            return calculate_angle(l_shoulder, l_hip, l_knee)
        else:
            return 0'''
        # print("left spine visible")
        return calculate_angle(l_shoulder, l_hip, l_knee)

    def angle_of_the_right_spine(self):  ## 푸쉬업 (오른쪽 척추(어깨, 허리, 무릎) 각도)
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        r_hip = detection(self.landmarks, "RIGHT_HIP")
        r_knee = detection(self.landmarks, "RIGHT_KNEE")
        '''if r_shoulder[2] >= 0.8 and r_hip[2] >= 0.8 and r_knee >= 0.8:
            print("right spine visible")
            return calculate_angle(r_shoulder, r_hip, r_knee)
        else:
            return 0'''
        # print("right spine visible")
        return calculate_angle(r_shoulder, r_hip, r_knee)

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
    
    def angle_of_the_left_knee(self): ## 스쿼트 (왼쪽 무릎, 발끝, 뒤꿈치 각도)
        l_knee = detection(self.landmarks, "LEFT_KNEE")
        l_ankle = detection(self.landmarks, "LEFT_ANKLE")
        l_foot_index = detection(self.landmarks, "LEFT_FOOT_INDEX")
        return calculate_angle(l_knee, l_ankle, l_foot_index)
    
    def angle_of_the_right_knee(self): ## 스쿼트 (오른쪽 무릎, 발끝, 뒤꿈치 각도)
        r_knee = detection(self.landmarks, "RIGHT_KNEE")
        r_ankle = detection(self.landmarks, "RIGHT_ANKLE")
        r_foot_index = detection(self.landmarks, "RIGHT_FOOT_INDEX")
        return calculate_angle(r_knee, r_ankle, r_foot_index)