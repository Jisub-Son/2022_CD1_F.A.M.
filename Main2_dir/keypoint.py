from utils import *

## 같은 로직 사용하면 하나로 묶기
class KEYPOINT:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    ###---------------------------- angles for push-up ----------------------------###

    def angle_of_the_left_elbow(self): # 푸쉬업 (왼쪽 어깨,팔꿈치,손목 각도) (푸쉬업, 이스터에그)
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        l_elbow = detection(self.landmarks, "LEFT_ELBOW")
        l_wrist = detection(self.landmarks, "LEFT_WRIST")
        if l_shoulder[2] >= REF_VISIBILITY and l_elbow[2]  >= REF_VISIBILITY and l_wrist[2] >= REF_VISIBILITY:
            return calculate_angle(l_shoulder, l_elbow, l_wrist)
        else:
            return 0

    def angle_of_the_right_elbow(self): # 푸쉬업 (오른쪽 어깨,팔꿈치,손목 각도) (푸쉬업, 이스터에그)
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        r_elbow = detection(self.landmarks, "RIGHT_ELBOW")
        r_wrist = detection(self.landmarks, "RIGHT_WRIST")
        if r_shoulder[2] >= REF_VISIBILITY and r_elbow[2]  >= REF_VISIBILITY and r_wrist[2] >= REF_VISIBILITY:
            return calculate_angle(r_shoulder, r_elbow, r_wrist)
        else:
            return 0
        
    def angle_of_the_left_spine(self):  # 푸쉬업 (왼쪽 척추(어깨, 허리, 무릎) 각도) (푸쉬업)
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        l_hip = detection(self.landmarks, "LEFT_HIP")
        l_knee = detection(self.landmarks, "LEFT_KNEE")
        if l_shoulder[2] >= REF_ROUGH_VISIBILITY and l_hip[2] >= REF_ROUGH_VISIBILITY and l_knee[2] >= REF_ROUGH_VISIBILITY:
            return calculate_angle(l_shoulder, l_hip, l_knee)
        else:
            return 0

    def angle_of_the_right_spine(self):  # 푸쉬업 (오른쪽 척추(어깨, 허리, 무릎) 각도) (푸쉬업)
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        r_hip = detection(self.landmarks, "RIGHT_HIP")
        r_knee = detection(self.landmarks, "RIGHT_KNEE")
        if r_shoulder[2] >= REF_ROUGH_VISIBILITY and r_hip[2] >= REF_ROUGH_VISIBILITY and r_knee[2] >= REF_ROUGH_VISIBILITY:
            return calculate_angle(r_shoulder, r_hip, r_knee)
        else:
            return 0
 

    ###---------------------------- angles for squat ----------------------------###

    def angle_of_the_left_leg(self): # 스쿼트 (왼쪽 허리, 무릎, 발목 각도)
        l_hip = detection(self.landmarks, "LEFT_HIP")
        l_knee = detection(self.landmarks, "LEFT_KNEE")
        l_ankle = detection(self.landmarks, "LEFT_ANKLE")
        if l_hip[2] >= REF_VISIBILITY and l_knee[2]  >= REF_VISIBILITY and l_ankle[2] >= REF_VISIBILITY:
            return calculate_angle(l_hip, l_knee, l_ankle)
        else:
            return 0

    def angle_of_the_right_leg(self): # 스쿼트 (오른쪽 허리, 무릎, 발목 각도)
        r_hip = detection(self.landmarks, "RIGHT_HIP")
        r_knee = detection(self.landmarks, "RIGHT_KNEE")
        r_ankle = detection(self.landmarks, "RIGHT_ANKLE")
        if r_hip[2] >= REF_VISIBILITY and r_knee[2]  >= REF_VISIBILITY and r_ankle[2] >= REF_VISIBILITY:
            return calculate_angle(r_hip, r_knee, r_ankle)
        else:
            return 0
    
    def angle_of_the_left_knee(self): # 스쿼트 (왼쪽 무릎, 발끝, 뒤꿈치 각도)
        l_knee = detection(self.landmarks, "LEFT_KNEE")
        l_ankle = detection(self.landmarks, "LEFT_ANKLE")
        l_foot_index = detection(self.landmarks, "LEFT_FOOT_INDEX")
        if l_knee[2] >= REF_VISIBILITY and l_ankle[2]  >= REF_VISIBILITY and l_foot_index[2] >= REF_VISIBILITY:
            return calculate_angle(l_knee, l_ankle, l_foot_index)
        else:
            return 0
    
    def angle_of_the_right_knee(self): # 스쿼트 (오른쪽 무릎, 발끝, 뒤꿈치 각도)
        r_knee = detection(self.landmarks, "RIGHT_KNEE")
        r_ankle = detection(self.landmarks, "RIGHT_ANKLE")
        r_foot_index = detection(self.landmarks, "RIGHT_FOOT_INDEX")
        if r_knee[2] >= REF_VISIBILITY and r_ankle[2]  >= REF_VISIBILITY and r_foot_index[2] >= REF_VISIBILITY:
            return calculate_angle(r_knee, r_ankle, r_foot_index)
        else:
            return 0
        
    def angle_of_right_foot_parallel(self): ## 스쿼트 오른발 11자
        r_foot_index = detection(self.landmarks, "RIGHT_FOOT_INDEX")
        r_heel = detection(self.landmarks, "RIGHT_HEEL")
        l_heel = detection(self.landmarks, "LEFT_FOOT_INDEX")
        if r_foot_index[2] >= REF_VISIBILITY and r_heel[2]  >= REF_VISIBILITY and l_heel[2] >= REF_VISIBILITY:
            return calculate_angle(r_foot_index, r_heel, l_heel)
        else:
            return 0
        
    def angle_of_left_foot_parallel(self): ## 스쿼트 왼발 11자
        r_foot_index = detection(self.landmarks, "RIGHT_FOOT_INDEX")
        l_foot_index = detection(self.landmarks, "LEFT_FOOT_INDEX")
        l_heel = detection(self.landmarks, "LEFT_HEEL")
        if r_foot_index[2] >= REF_VISIBILITY and l_foot_index[2]  >= REF_VISIBILITY and l_heel[2] >= REF_VISIBILITY:
            return calculate_angle(r_foot_index, l_foot_index, l_heel)
        else:
            return 0    
            
    ###---------------------------- length for push-up ----------------------------###
        
    def length_of_shoulder_to_shoulder(self):   # 양 어깨 사이 거리
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        if r_shoulder[2] >= REF_ROUGH_VISIBILITY and l_shoulder[2] >= REF_ROUGH_VISIBILITY:
            return calculate_length(r_shoulder, l_shoulder)
        else:
            return 0    

    def length_of_wrist_to_wrist(self):   # 양 손목 사이 거리
        r_wrist = detection(self.landmarks, "RIGHT_WRIST")
        l_wrist = detection(self.landmarks, "LEFT_WRIST")
        if r_wrist[2] >= REF_ROUGH_VISIBILITY and l_wrist[2] >= REF_ROUGH_VISIBILITY:
            return calculate_length(r_wrist, l_wrist)
        else:
            return 0


    ###---------------------------- length for squat ----------------------------###

    def length_of_ankle_to_ankle(self):   # 양 발목 사이 거리 (스쿼트, 사레레)
        r_ankle = detection(self.landmarks, "RIGHT_ANKLE")
        l_ankle = detection(self.landmarks, "LEFT_ANKLE")
        if r_ankle[2] >= REF_ROUGH_VISIBILITY and l_ankle[2] >= REF_ROUGH_VISIBILITY:
            return calculate_length(r_ankle, l_ankle)
        else:
            return 0
    
    def length_of_heel_to_heel(self):   # 양 발뒷꿈치 사이 거리 (스쿼트)
        r_heel = detection(self.landmarks, "RIGHT_HEEL")
        l_heel = detection(self.landmarks, "LEFT_HEEL")
        if r_heel[2] >= REF_ROUGH_VISIBILITY and l_heel[2] >= REF_ROUGH_VISIBILITY:
            return calculate_length(r_heel, l_heel)
        else:
            return 0
        
    def length_of_foot_to_foot(self):   # 양 발끝 사이 거리 (스쿼트)
        r_foot_index = detection(self.landmarks, "RIGHT_FOOT_INDEX")
        l_foot_index = detection(self.landmarks, "LEFT_FOOT_INDEX")
        if r_foot_index[2] >= REF_VISIBILITY and l_foot_index[2] >= REF_VISIBILITY:
            return calculate_length(r_foot_index, l_foot_index)
        else:
            return 0
        
    ###--------------------------- side lateral raise ---------------------------###    
    
    def angle_of_the_left_shoulder(self): # 왼쪽 어깨 각도 (사레레)
        l_elbow = detection(self.landmarks, "RIGHT_ELBOW")
        l_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        l_hip = detection(self.landmarks, "RIGHT_HIP")
        if l_elbow[2] >= REF_VISIBILITY and l_shoulder[2]  >= REF_VISIBILITY and l_hip[2] >= REF_VISIBILITY:
            return calculate_angle(l_elbow, l_shoulder, l_hip)
        else:
            return 0
        
    def angle_of_the_right_shoulder(self): # 오른쪽 어깨 각도 (사레레)
        r_elbow = detection(self.landmarks, "RIGHT_ELBOW")
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        r_hip = detection(self.landmarks, "RIGHT_HIP")
        if r_elbow[2] >= REF_VISIBILITY and r_shoulder[2]  >= REF_VISIBILITY and r_hip[2] >= REF_VISIBILITY:
            return calculate_angle(r_elbow, r_shoulder, r_hip)
        else:
            return 0
    
    def angle_of_the_left_elbow(self): # 왼쪽 팔꿈치 각도 (사레레)
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        l_elbow = detection(self.landmarks, "LEFT_ELBOW")
        l_wrist = detection(self.landmarks, "LEFT_WRIST")
        if l_shoulder[2] >= REF_VISIBILITY and l_elbow[2]  >= REF_VISIBILITY and l_wrist[2] >= REF_VISIBILITY:
            return calculate_angle(l_shoulder, l_elbow, l_wrist)
        else:
            return 0
        
    def angle_of_the_right_elbow(self): # 오른쪽 팔꿈치 각도
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        r_elbow = detection(self.landmarks, "RIGHT_ELBOW")
        r_wrist = detection(self.landmarks, "RIGHT_WRIST")
        if r_shoulder[2] >= REF_VISIBILITY and r_elbow[2]  >= REF_VISIBILITY and r_wrist[2] >= REF_VISIBILITY:
            return calculate_angle(r_shoulder, r_elbow, r_wrist)
        else:
            return 0         
        
    ###------------------------------- easter egg -------------------------------###
    


    def angle_of_the_right_shoulder(self): ## 경례할 때 오른쪽 어깨 각도
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        r_elbow = detection(self.landmarks, "RIGHT_ELBOW")
        if l_shoulder[2] >= REF_VISIBILITY and r_shoulder[2] >= REF_VISIBILITY and r_elbow[2] >= REF_VISIBILITY:
            return calculate_angle(l_shoulder, r_shoulder,r_elbow)
        else:
            return 0
        
    def angle_of_the_right_wrist(self): ## 경례할 때 손목 각도
        r_elbow = detection(self.landmarks, "RIGHT_ELBOW")
        r_wrist = detection(self.landmarks, "RIGHT_WRIST")
        r_pinky = detection(self.landmarks, "RIGHT_THUMB")
        if r_elbow[2] >= REF_VISIBILITY and r_wrist[2] >= REF_VISIBILITY and r_pinky[2] >= REF_VISIBILITY:
            return calculate_angle(r_elbow, r_wrist, r_pinky)
        else:
            return 0    
        
        
    def angle_of_the_left_shoulder(self): ## 경례할 때 오른쪽 어깨 각도
        r_shoulder = detection(self.landmarks, "RIGHT_SHOULDER")
        l_shoulder = detection(self.landmarks, "LEFT_SHOULDER")
        l_elbow = detection(self.landmarks, "LEFT_ELBOW")
        if r_shoulder[2] >= REF_VISIBILITY and l_shoulder[2] >= REF_VISIBILITY and l_elbow[2] >= REF_VISIBILITY:
            return calculate_angle(r_shoulder, l_shoulder, l_elbow)
        else:
            return 0    
    
    def angle_of_the_left_knee(self): # 왼쪽 무릎은 11자
        l_hip = detection(self.landmarks, "LEFT_HIP")
        l_knee = detection(self.landmarks, "LEFT_KNEE")
        l_ankle = detection(self.landmarks, "LEFT_ANKLE")
        if l_hip[2] >= REF_VISIBILITY and l_knee[2]  >= REF_VISIBILITY and l_ankle[2] >= REF_VISIBILITY:
            return calculate_angle(l_hip, l_knee, l_ankle)
        else:
            return 0

    def angle_of_the_right_knee(self): # 오른쪽 무릎은 11자
        r_hip = detection(self.landmarks, "RIGHT_HIP")
        r_knee = detection(self.landmarks, "RIGHT_KNEE")
        r_ankle = detection(self.landmarks, "RIGHT_ANKLE")
        if r_hip[2] >= REF_VISIBILITY and r_knee[2]  >= REF_VISIBILITY and r_ankle[2] >= REF_VISIBILITY:
            return calculate_angle(r_hip, r_knee, r_ankle)
        else:
            return 0 
