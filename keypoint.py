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
        return calculate_angle(l_shoulder, l_elbow, l_wrist)

    def angle_of_the_right_arm(detect): ## 푸쉬업 (오른쪽 어깨,팔꿈치,손목 각도)
        r_shoulder = detection(detect.landmarks, "RIGHT_SHOULDER")
        r_elbow = detection(detect.landmarks, "RIGHT_ELBOW")
        r_wrist = detection(detect.landmarks, "RIGHT_WRIST")
        return calculate_angle(r_shoulder, r_elbow, r_wrist)

    def angle_of_the_left_leg(detect): ## 스쿼트 (왼쪽 허리, 무릎, 발목 각도)
        l_hip = detection(detect.landmarks, "LEFT_HIP")
        l_knee = detection(detect.landmarks, "LEFT_KNEE")
        l_ankle = detection(detect.landmarks, "LEFT_ANKLE")
        return calculate_angle(l_hip, l_knee, l_ankle)

    def angle_of_the_right_leg(detect): ## 스쿼트 (오른쪽 허리, 무릎, 발목 각도)
        r_hip = detection(detect.landmarks, "RIGHT_HIP")
        r_knee = detection(detect.landmarks, "RIGHT_KNEE")
        r_ankle = detection(detect.landmarks, "RIGHT_ANKLE")
        return calculate_angle(r_hip, r_knee, r_ankle)

    def angle_of_the_right_spine(detect):  ## 스쿼트 + 푸쉬업 (오른쪽 척추(허리, 어깨 목) 각도)
        r_knee = detection(detect.landmarks, "RIGHT_KNEE")
        r_shoulder = detection(detect.landmarks, "RIGHT_SHOULDER")
        r_hip = detection(detect.landmarks, "RIGHT_HIP")
        return calculate_angle(r_knee, r_shoulder, r_hip, "RIGHT_SPINE")
    
    def angle_of_the_left_spine(detect):  ## 스쿼트 + 푸쉬업 (왼쪽 척추(허리, 어깨 목) 각도)
        l_knee = detection(detect.landmarks, "LEFT_MOUTH")
        l_shoulder = detection(detect.landmarks, "LEFT_SHOULDER")
        l_hip = detection(detect.landmarks, "LEFT_HIP")
        return calculate_angle(l_knee, l_shoulder, l_hip, "LEFT_SPINE")