from math import fabs
import time
from unittest.mock import DEFAULT
from keypoint import KEYPOINT   
from utils import *            

# 전역 변수 초기화
cur = 0.0                   # timer 변수
prev = 0.0
timeElapsed = 0.0

left_leg_angle = 180.0      # 스쿼트 무릎 각도
right_leg_angle = 180.0
avg_leg_angle = 180.0

left_knee_angle = 180.0     # 스쿼트 발목 각도 
right_knee_angle = 180.0
avg_knee_angle = 180.0

left_arm_angle = 180.0      # 푸쉬업 팔꿈치 각도
right_arm_angle = 180.0
avg_arm_angle = 0.0

left_spine_angle = 180.0    # 푸쉬업 허리 각도
right_spine_angle = 180.0
avg_spine_angle = 0.0

left_foot_parallel = 90.0
right_foot_parallel = 90.0
avg_foot_parallel = 90.0

class EXERCISE(KEYPOINT):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    # timer function
    def Rest_timer(self, reps, status, sets, feedback, timer):
        global cur, prev, timeElapsed   
        cur = time.time()               # current time
        
        timeElapsed = cur - prev        # calculate time difference
        
        if timeElapsed >= 1:            # after 1 second
            timer -= 1                  
            timeElapsed = 0             
            prev += 1                   
            if timer <= 0:              # when timer is done
                timer = REF_TIMER       
                reps = 0                
                sets += 1               
                status = 'Up'
        
        return [reps, status, sets, feedback, timer]
                            
    # squat function
    def squat(self, reps, status, sets, feedback, timer, camID):
        global prev, left_knee_angle, right_knee_angle, avg_knee_angle, left_leg_angle, right_leg_angle, avg_leg_angle, left_foot_parallel, right_foot_parallel, avg_foot_parallel
        
        # reference angles
        REF_KNEE_ANGLE = 130.0
        REF_LEG_ANGLE = 120.0
        MORE_LEG_ANGLE = 155.0
        LESS_LEG_ANGLE = 50.0
        DEFAULT_KNEE_ANGLE = 160.0
        DEFAULT_LEG_ANGLE = 170.0      
        FOOT_PARALLEL = 90.0 ########################################################
        
        # get angles from eact camID
        if camID == 0: ## 노트북 CAM 왼쪽
            left_leg_angle = self.angle_of_the_right_leg()
            left_knee_angle = self.angle_of_the_left_knee()
            left_foot_parallel = self.angle_of_left_foot_parallel() ########################################################
        elif camID == 1: ## USB CAM 오른쪽
            right_leg_angle = self.angle_of_the_left_leg()
            right_knee_angle = self.angle_of_the_right_knee()
            right_foot_parallel = self.angle_of_right_foot_parallel() #######################################################
            
        # get average    
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2
        avg_knee_angle = (left_knee_angle + right_knee_angle) // 2  
        avg_foot_parallel = fabs(left_foot_parallel - right_foot_parallel) ########################################################
        
        # make table for avg_angles
        table_angle("leg", avg_leg_angle, "knee", avg_knee_angle, "parallel", avg_foot_parallel) ########################################################
                
        # how to make count
        # 무릎이 발끝보다 뒤에 있고 and 무를을 충분히 굽혔을 때 count
        if (status == 'Up' and feedback != 'Bend your legs less' and feedback != 'Place your knees behind toes') and avg_foot_parallel < FOOT_PARALLEL and LESS_LEG_ANGLE < avg_leg_angle < REF_LEG_ANGLE and avg_knee_angle > REF_KNEE_ANGLE:    
            voiceFeedback('buzzer')
            reps += 1
            status = 'Down'
            feedback = 'Success'
            prev = time.time()
        else:
            # 우선순위1 : 무릎을 충분히 굽히지 않았을 때 + 무릎이 발끝보다 뒤에
            if (feedback != 'Bend your legs more' and feedback != 'Bend your legs less' and feedback != 'Place your knees behind toes' and feedback !='Success') and  REF_LEG_ANGLE < avg_leg_angle < MORE_LEG_ANGLE and avg_knee_angle > REF_KNEE_ANGLE:  
                voiceFeedback('moredown') ## 더 내려가
                status = 'Up'
                feedback = 'Bend your legs more'
            # 우선순위2 : 무릎이 발끝보다 앞쪽에 있을 때 
            elif (feedback != 'Place your knees behind toes' and feedback != 'start exercise') and avg_knee_angle < REF_KNEE_ANGLE:
                voiceFeedback('kneedown') ## 무릎 집어넣어라
                status = 'Up'
                feedback = 'Place your knees behind toes'
            ## 우선순위3 : 발 11자 아닐때
            elif (feedback != 'Parallel your feet'): ########################################################
                voiceFeedback('parallel')
                status = 'Up'
                feedback = 'Parallel your feet'    
            # 우선순위4 : 너무 내려갔을 때
            elif (status == 'Down' and feedback != 'Bend your legs less' and feedback != 'Place your knees behind toes') and avg_leg_angle < LESS_LEG_ANGLE and avg_knee_angle > REF_KNEE_ANGLE:
                voiceFeedback('lessdown') ## 너무 내려갔어 + 무릎이 발끝보다 뒤에
                reps -= 1
                status = 'Up'
                feedback = 'Bend your legs less'    
            elif (feedback != 'Success' or status == 'Down') and avg_leg_angle > DEFAULT_LEG_ANGLE and avg_knee_angle > DEFAULT_KNEE_ANGLE:
                status = 'Up'
                feedback = 'Start'      
                
        # after each set
        if reps == REF_REPS:
            if timer == 5 and camID == 0:
                voiceFeedback('rest')
            status = 'Rest'
            feedback = 'Take a breathe..'
            reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # run timer function
        
        # when exercise is finished
        if sets == REF_SETS:
            voiceFeedback('end')
            reps = 0
            status = 'All done'
            sets = 0
            feedback = "Well done!"
            
        return [reps, status, sets, feedback, timer, camID]

    # pushup function
    def pushup(self, reps, status, sets, feedback, timer, camID):
        global prev, left_arm_angle, right_arm_angle, avg_arm_angle, left_spine_angle, right_spine_angle, avg_spine_angle
        
        # reference angles
        REF_ARM_ANGLE = 90.0
        REF_SPINE_ANGLE = 170.0
        
        # get angles from eact camID
        if camID == 0: ## 노트북 CAM 왼쪽
            left_spine_angle = self.angle_of_the_left_spine()
            left_arm_angle = self.angle_of_the_left_arm()
            # length_shoudler = self.length_of_shoulder_to_shoulder()
            # length_foot = self.length_of_foot_to_foot()
        elif camID == 1: ## USB CAM 오른쪽
            right_spine_angle = self.angle_of_the_right_spine()
            right_arm_angle = self.angle_of_the_right_arm()
        
        # get average
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 
        avg_spine_angle = (left_spine_angle + right_spine_angle) // 2 

        # make table for avg_angles
        # table_angle("arm", avg_arm_angle, "spine", avg_spine_angle, "shoudler", length_shoudler, "foot", length_foot)
        table_angle("arm", avg_arm_angle, "spine", avg_spine_angle)
                
        # how to make count
        # 팔꿈치를 충분히 굽히고 and 허리가 일직선일 때
        if status == 'Up' and avg_arm_angle < REF_ARM_ANGLE and avg_spine_angle > REF_SPINE_ANGLE:     
            voiceFeedback('buzzer')
            reps += 1
            status = 'Down'
            feedback = 'Success'
            prev = time.time()
        else:
            # 우선순위1 : 팔을 충분히 굽히지 않은 경우
            if (status != 'Rest' and status != 'All done') and avg_arm_angle > REF_ARM_ANGLE:     
                status = 'Up'
                feedback = 'Bend your elbows'
            # 우선순위2 : 척추가 일자가 아닐 경우
            elif (status != 'Rest' and status != 'All done') and avg_spine_angle < REF_SPINE_ANGLE:
                status = 'Up'
                feedback = 'Straight your spine'
                
        # after each set
        if reps == REF_REPS:
            if timer == 5 and camID == 0:
                voiceFeedback('rest')
            status = 'Rest'
            feedback = 'Take a breathe..'
            reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)   # run timer function
        
        # when exercise is finished
        if sets == REF_SETS:
            voiceFeedback('end')
            reps = 0
            status = 'All done'
            sets = 0
            feedback = "Well done!"
        
        return [reps, status, sets, feedback, timer, camID]
  
    # select mode
    def calculate_exercise(self, exercise, reps, status, sets, feedback, timer, camID): 
        if exercise == "pushup":
            reps, status, sets, feedback, timer, camID = EXERCISE(self.landmarks).pushup(
                reps, status, sets, feedback, timer, camID)
        elif exercise == "squat":
            reps, status, sets, feedback, timer, camID = EXERCISE(self.landmarks).squat(
                reps, status, sets, feedback, timer, camID)
        
        return [reps, status, sets, feedback, timer, camID]