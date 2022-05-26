import mediapipe as mp ## 스켈레톤
import pandas as pd ## keypoint간 빠른계산
import numpy as np ## 스켈레톤 다차원배열 구현
from utils import * ## utils 불러오기

class KEYPOINT:
    def __init__(detect, landmarks):
        detect.landmarks = landmarks

    def angle_of_the_left_arm(detect): ## 푸쉬업 (왼쪽 어깨,팔꿈치,손목 각도)
        l_shoulder = detection(detect.landmarks, "LEFT_SHOULDER")
        l_elbow = detection(detect.landmarks, "LEFT_ELBOW")
        l_wrist = detection(detect.landmarks, "LEFT_WRIST")
        if l_shoulder[2] >= 0.7 and l_elbow[2]  >= 0.7 and l_wrist[2] >= 0.7:
            ##print("left arm visible")
            return calculate_angle(l_shoulder, l_elbow, l_wrist)
        else:
            return 0
    def angle_of_the_right_arm(detect): ## 푸쉬업 (오른쪽 어깨,팔꿈치,손목 각도)
        r_shoulder = detection(detect.landmarks, "RIGHT_SHOULDER")
        r_elbow = detection(detect.landmarks, "RIGHT_ELBOW")
        r_wrist = detection(detect.landmarks, "RIGHT_WRIST")
        if r_shoulder[2] >= 0.7 and r_elbow[2]  >= 0.7 and r_wrist[2] >= 0.7:
            ##print("right arm visible")
            return calculate_angle(r_shoulder, r_elbow, r_wrist)
        else:
            return 0

    def angle_of_the_left_leg(detect): ## 스쿼트 (왼쪽 허리, 무릎, 발목 각도)
        l_hip = detection(detect.landmarks, "LEFT_HIP")
        l_knee = detection(detect.landmarks, "LEFT_KNEE")
        l_ankle = detection(detect.landmarks, "LEFT_ANKLE")
        if l_hip[2] >= 0.7 and l_knee[2]  >= 0.7 and l_ankle[2] >= 0.7:
            ##print("left leg visible")
            return calculate_angle(l_hip, l_knee, l_ankle)
        else:
            return 0

    def angle_of_the_right_leg(detect): ## 스쿼트 (오른쪽 허리, 무릎, 발목 각도)
        r_hip = detection(detect.landmarks, "RIGHT_HIP")
        r_knee = detection(detect.landmarks, "RIGHT_KNEE")
        r_ankle = detection(detect.landmarks, "RIGHT_ANKLE")
        if r_hip[2] >= 0.7 and r_knee[2]  >= 0.7 and r_ankle[2] >= 0.7:
            ##print("right leg visible")
            return calculate_angle(r_hip, r_knee, r_ankle)
        else:
            return 0


    def angle_of_the_left_spine(detect):  ## 푸쉬업 (왼쪽 척추(어깨, 허리, 무릎) 각도)
        l_shoulder = detection(detect.landmarks, "LEFT_SHOULDER")
        l_hip = detection(detect.landmarks, "LEFT_HIP")
        l_knee = detection(detect.landmarks, "LEFT_KNEE")
        if l_shoulder[2] >= 0.7 and l_hip[2]  >= 0.7 and l_knee[2] >= 0.7:
            ##print("left spine visible")
            return calculate_angle(l_shoulder, l_hip, l_knee)
        else:
            return 0

    
    def angle_of_the_right_spine(detect):  ## 푸쉬업 (오른쪽 척추(어깨, 허리, 무릎) 각도)
        r_shoulder = detection(detect.landmarks, "RIGHT_SHOULDER")
        r_hip = detection(detect.landmarks, "RIGHT_HIP")
        r_knee = detection(detect.landmarks, "RIGHT_KNEE")
        if r_shoulder[2] >= 0.7 and r_hip[2]  >= 0.7 and r_knee[2] >= 0.7:
            ##print("right spine visible")
            return calculate_angle(r_shoulder, r_hip, r_knee)
        else:
            return 0
  
    def angle_of_the_left_knee(detect): ## 스쿼트 (왼쪽 무릎, 발끝, 뒤꿈치 각도)
        l_knee = detection(detect.landmarks, "LEFT_KNEE")
        l_ankle = detection(detect.landmarks, "LEFT_ANKLE")
        l_foot_index = detection(detect.landmarks, "LEFT_FOOT_INDEX")
        if l_knee[2] >= 0.7 and l_ankle[2]  >= 0.7 and l_foot_index[2] >= 0.7:
            ##print("left knee visible")
            return calculate_angle(l_knee, l_ankle, l_foot_index)
        else:
            return 0

    def angle_of_the_right_knee(detect): ## 스쿼트 (오른쪽 무릎, 발끝, 뒤꿈치 각도)
        r_knee = detection(detect.landmarks, "RIGHT_KNEE")
        r_ankle = detection(detect.landmarks, "RIGHT_ANKLE")
        r_foot_index = detection(detect.landmarks, "RIGHT_FOOT_INDEX")
        if r_knee[2] >= 0.7 and r_ankle[2]  >= 0.7 and r_foot_index[2] >= 0.7:
            ##print("right knee visible")
            return calculate_angle(r_knee, r_ankle, r_foot_index)
        else:
            return 0