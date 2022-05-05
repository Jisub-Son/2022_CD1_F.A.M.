import mediapipe as mp
import pandas as pd
import numpy as np
import cv2
from utils import *

class BodyPartDistance:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    def distance_of_the_shoulder(self):
        l_shoulder = detection_body_part(self.landmarks, "LEFT_SHOULDER")
        r_shoulder = detection_body_part(self.landmarks, "RIGHT_SHOULDER")
        return calculate_distance(l_shoulder, r_shoulder)

    def distance_between_knee(self):
        l_knee = detection_body_part(self.landmarks, "LEFT_KNEE")
        r_knee = detection_body_part(self.landmarks, "RIGHT_KNEE")
        return calculate_distance(l_knee, r_knee)

    def distance_between_heel(self):
        l_heel = detection_body_part(self.landmarks, "LEFT_HEEL")
        r_heel = detection_body_part(self.landmarks, "RIGHT_HEEL")
        return calculate_distance(l_heel, r_heel)
    
    def distance_between_foot_index(self):
        l_foot_index = detection_body_part(self.landmarks, "LEFT_FOOT_INDEX")
        r_foot_index = detection_body_part(self.landmarks, "RIGHT_FOOT_INDEX")
        return calculate_distance(l_foot_index, r_foot_index)

    def distance_between_hand(self):
        l_wrist = detection_body_part(self.landmarks, "LEFT_WRIST")
        r_wrist = detection_body_part(self.landmarks, "RIGHT_WRIST")
        return calculate_distance(l_wrist, r_wrist)