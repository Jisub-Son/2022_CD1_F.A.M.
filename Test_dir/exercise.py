import time
from unittest.mock import DEFAULT
from keypoint import KEYPOINT   
from utils import *  
from math import fabs          

# 전역 변수 초기화
cur = 0.0                   # timer 변수
prev = 0.0
timeElapsed = 0.0

left_leg_angle = 180.0      # 스쿼트 무릎 각도
right_leg_angle = 180.0
avg_leg_angle = 0.0

left_knee_angle = 180.0     # 스쿼트 발목 각도 
right_knee_angle = 180.0
avg_knee_angle = 0.0

left_arm_angle = 180.0      # 푸쉬업 팔꿈치 각도
right_arm_angle = 180.0
avg_arm_angle = 0.0

left_spine_angle = 180.0    # 푸쉬업 허리 각도
right_spine_angle = 180.0
avg_spine_angle = 0.0

left_elbow_angle = 90.0    #푸쉬업 내려가면서 팔꿈치 각도
right_elbow_angle = 90.0
avg_elbow_angle = 0.0

left_wrist_angle = 90.0
right_wrist_angle = 90.0
avg_wrist_angle = 0.0

left_foot_parallel = 90.0   # 발 11자 각도
right_foot_parallel = 90.0
avg_foot_parallel = 90.0

shoulder_length = 0.0   # 어깨, 발 사이 거리
wrist_length = 0.0
elbow_length = 0.0
heel_length = 0.0
foot_length = 0.0

elbow_shoulder_ratio = 0.0
wrist_shoulder_ratio = 0.0
heel_foot_ratio = 0.0

color = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

class EXERCISE(KEYPOINT):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    # timer function
    def Rest_timer(self, reps, status, sets, feedback, timer):
        global cur, prev, timeElapsed, flag
        cur = time.time()               # current time
        
        timeElapsed = cur - prev        # calculate time difference
        
        if timeElapsed >= 1:            # after 1 second
            # print(timer)
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
        global left_knee_angle, right_knee_angle, avg_knee_angle,\
                left_leg_angle, right_leg_angle, avg_leg_angle,\
                left_foot_parallel, right_foot_parallel, avg_foot_parallel,\
                heel_length, foot_length, heel_foot_ratio,\
                prev, color
        
        # reference angles
        REF_KNEE_ANGLE = 110.0
        REF_LEG_ANGLE = 140.0
        MORE_LEG_ANGLE = 160.0
        LESS_LEG_ANGLE = 60.0
        LESS_PARALLEL_ANGLE = 0.0
        MORE_PARALLEL_ANGLE = 60.0
        LESS_HEEL_FOOT_RATIO = 0.8
        MORE_HEEL_FOOT_RATIO = 1.2 
        
        # conditions
        AFTER_SET_CONDITION = (reps == REF_REPS and status == 'Up')     # 한 세트 이후 조건
        AFTER_ALL_SET_CONDITION = (sets == REF_SETS)                    # 전체 세트 이후 조건
        KNEEDOWN_CONDITION = (status != 'Rest' and feedback != 'Place your knees behind toes' and feedback != 'Parallel your feet') # 무릎이 발끝 앞으로 나갔을 경우
        PARALLEL_CONDITION = (status != 'Rest' and feedback != 'Parallel your feet' and feedback != 'Place your knees behind toes') # 발 11자를 못했을 경우
        DEFAULT_CONDITION = (status != 'Rest')  # 운동 중인데 아무것도 아닌 경우
        MOREDOWN_CONDITION = (status != 'Rest' and feedback == 'Start') # 더 구부려야 하는 경우
        COUNT_CONDITION = (status != 'Rest' and feedback == 'Bend your legs more')  # 적절한 경우
        LESSDOWN_CONDITION = (status != 'Rest' and feedback == 'Success')   # 덜 구부려야 하는 경우
        
        # angles in conditions -> '만족하는' 각도
        KNEEDOWN_ANGLE = (avg_knee_angle > REF_KNEE_ANGLE)
        PARALLEL_ANGLE = (LESS_PARALLEL_ANGLE < avg_foot_parallel < MORE_PARALLEL_ANGLE)
        PARALLEL_RATIO = (LESS_HEEL_FOOT_RATIO < heel_foot_ratio < MORE_HEEL_FOOT_RATIO)
        DEFAULT_ANGLE = (avg_leg_angle > MORE_LEG_ANGLE)
        MOREDOWN_ANGLE = (REF_LEG_ANGLE < avg_leg_angle < MORE_LEG_ANGLE)
        COUNT_ANGLE = (LESS_LEG_ANGLE < avg_leg_angle < REF_LEG_ANGLE)
        LESSDOWN_ANGLE = (avg_leg_angle < LESS_LEG_ANGLE)
        
        # get angles from eact camID
        if camID == LEFT_CAM:
            left_leg_angle = self.angle_of_the_right_leg()
            left_knee_angle = self.angle_of_the_left_knee() 
            left_foot_parallel = self.angle_of_left_foot_parallel()  
        elif camID == RIGHT_CAM:
            right_leg_angle = self.angle_of_the_left_leg()
            right_knee_angle = self.angle_of_the_right_knee()
            right_foot_parallel = self.angle_of_right_foot_parallel()
            heel_length = self.length_of_heel_to_heel()
            foot_length = self.length_of_foot_to_foot()
            
            # get average    
            avg_leg_angle = (left_leg_angle + right_leg_angle) // 2
            avg_knee_angle = (left_knee_angle + right_knee_angle) // 2 
            avg_foot_parallel = fabs(left_foot_parallel - right_foot_parallel) 
            
            #get ratio
            foot_length = round(foot_length, 4)
            heel_foot_ratio = heel_length / foot_length
            # heel_foot_ratio = fabs(heel_length - foot_length)
                
            # count logic
            if KNEEDOWN_ANGLE and PARALLEL_ANGLE:       # 기본 자세가 만족되고..
                if LESSDOWN_CONDITION and LESSDOWN_ANGLE:   # 많이 구부렸을 때
                    voiceFeedback('lessdown')
                    reps -= 1
                    status = 'Up'
                    feedback = 'Bend your legs less'
                    color = [(0, 0, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
                elif COUNT_CONDITION and COUNT_ANGLE:       # 적절히 구부렸을 때
                    voiceFeedback('buzzer')
                    reps += 1
                    status = 'Down'
                    feedback = 'Success'
                    prev = time.time()
                    color = [(255, 0, 0), (255, 0, 0), (255, 0, 0), (0, 0, 0)]
                elif MOREDOWN_CONDITION and MOREDOWN_ANGLE: # 덜 구부렸을 때
                    voiceFeedback('moredown')
                    status = 'Up'
                    feedback = 'Bend your legs more'
                    color = [(0, 0, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
                elif DEFAULT_CONDITION and DEFAULT_ANGLE:   # 구부리지 않았을 때
                    status = 'Up'
                    feedback = 'Start'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
            else:
                if feedback == 'Success' and (not KNEEDOWN_ANGLE or not PARALLEL_ANGLE):    # 카운트가 된 직후 잘못 자세를 잡았을 때
                    reps -= 1
                    status = 'Up'
                    feedback = 'Keep your position to the end'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 255), (0, 0, 0)]
                elif KNEEDOWN_CONDITION and not KNEEDOWN_ANGLE:   # 무릎이 발끝 앞으로 나갔을 때
                    voiceFeedback('kneedown')
                    status = 'Up'
                    feedback = 'Place your knees behind toes'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 0), (0, 0, 0)] 
                elif PARALLEL_CONDITION and not PARALLEL_RATIO: # 발이 11자가 아닐 때
                    print("condition 6")
                    voiceFeedback('parallel')
                    status = 'Up'
                    feedback = 'Parallel your feet'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 255), (0, 0, 0)]
                    
            # after each set
            if AFTER_SET_CONDITION:
                prev = time.time()
                if feedback == 'Start':
                    voiceFeedback('rest_time')
                status = 'Rest'
                feedback = 'Take a breathe..'
            if status == 'Rest':
                reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # run timer function
            
            # when exercise is finished
            if AFTER_ALL_SET_CONDITION:
                voiceFeedback('end')
                reps = 0
                status = 'All done'
                sets = 0
                feedback = "Well done!"
                
            # make table for avg_angles
            table_calculations(color, avg_leg = avg_leg_angle, avg_knee = avg_knee_angle, foot_ratio = heel_foot_ratio, avg_parallel = avg_foot_parallel,)
            
        return [reps, status, sets, feedback, timer, camID]

    # pushup function
    def pushup(self, reps, status, sets, feedback, timer, camID):
        global left_arm_angle, right_arm_angle, avg_arm_angle,\
                left_spine_angle, right_spine_angle, avg_spine_angle,\
                left_wrist_angle, right_wrist_angle, avg_wrist_angle,\
                shoulder_length, wrist_length, elbow_length,\
                elbow_shoulder_ratio, wrist_shoulder_ratio,\
                prev, color   
        
        # reference angles
        REF_ARM_ANGLE = 80.0
        REF_SPINE_ANGLE = 130.0
        MORE_ARM_ANGLE = 100.0
        MORE_WRIST_ANGLE = 27.0
        # LESS_WRIST_ANGLE = 20.0
        REF_WRIST_SHOULDER_RATIO = 1.6
        # REF_ELBOW_SHOULDER_RATIO = 2.2
        
        # conditions
        AFTER_SET_CONDITION = (reps == REF_REPS and status == 'Up')     # 한 세트 이후 조건
        AFTER_ALL_SET_CONDITION = (sets == REF_SETS)                    # 전체 세트 이후 조건
        SPINE_CONDITION = (status != 'Rest' and (feedback != 'Straight your spine' or feedback != 'Put your hands together'))    # 허리 구부렸을 때
        WRIST_CONDITION = (status != 'Rest' and (feedback != 'Put your hands together' or feedback != 'Straight your spine'))    # 팔 넓이
        DEFAULT_CONDITION = (status != 'Rest')  # 운동 중인데 아무것도 아닌 경우
        MOREDOWN_CONDITION = (status != 'Rest' and feedback == 'Start') # 더 구부려야 하는 경우
        COUNT_CONDITION = (status != 'Rest' and feedback == 'Bend your arms more')  # 적절한 경우
        
        # angles in conditions -> '만족하는' 각도
        SPINE_ANGLE = (avg_spine_angle > REF_SPINE_ANGLE)
        # WRIST_ANGLE = (LESS_WRIST_ANGLE < avg_wrist_angle < MORE_WRIST_ANGLE)
        WRIST_ANGLE = (avg_wrist_angle < MORE_WRIST_ANGLE)
        WRIST_RATIO = (wrist_shoulder_ratio < REF_WRIST_SHOULDER_RATIO)
        DEFAULT_ANGLE = (avg_arm_angle > MORE_ARM_ANGLE)
        MOREDOWN_ANGLE = (REF_ARM_ANGLE < avg_arm_angle < MORE_ARM_ANGLE)
        COUNT_ANGLE = (avg_arm_angle < REF_ARM_ANGLE)
        
        # get angles from eact camID
        if camID == LEFT_CAM:
            left_spine_angle = self.angle_of_the_left_spine()
            left_arm_angle = self.angle_of_the_left_arm()
            left_wrist_angle = self.angle_of_the_left_wrist()
            # elbow_length = self.length_of_elbow_to_elbow()
        elif camID == RIGHT_CAM:
            right_spine_angle = self.angle_of_the_right_spine()
            right_arm_angle = self.angle_of_the_right_arm()
            right_wrist_angle = self.angle_of_the_right_wrist()
            wrist_length = self.length_of_wrist_to_wrist()
            shoulder_length = self.length_of_shoulder_to_shoulder()
        
            # get average
            avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 
            avg_spine_angle = (left_spine_angle + right_spine_angle) // 2 
            avg_wrist_angle = (left_wrist_angle + right_wrist_angle) // 2
            
            # get ratio
            shoulder_length = round(shoulder_length, 4)
            wrist_shoulder_ratio = wrist_length / shoulder_length
            # elbow_shoulder_ratio = elbow_length / shoulder_length
            
            # count logic
            if SPINE_ANGLE and WRIST_RATIO:         # 기본 자세가 만족되고
                if COUNT_CONDITION and COUNT_ANGLE: # 적절하게 구부렸을 때
                    voiceFeedback('buzzer')
                    reps += 1
                    status = 'Down'
                    feedback = 'Success'
                    color = [(255, 0, 0), (255, 0, 0), (255, 0, 0)]
                elif MOREDOWN_CONDITION and MOREDOWN_ANGLE:     # 너무 적게 구부렸을 때
                    voiceFeedback('moredown')
                    status = 'Up'
                    feedback = 'Bend your arms more'
                    color = [(0, 0, 255), (0, 0, 0), (0, 0, 0)]
                elif DEFAULT_CONDITION and DEFAULT_ANGLE:       #구부리지 않았을 때
                    status = 'Up'
                    feedback = 'Start'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
            else:
                if feedback == 'Success' and (not SPINE_ANGLE or not WRIST_RATIO):  # 카운트가 된 직후 잘못 자세를 잡았을 때
                    reps -= 1
                    status = 'Up'
                    feedback = 'Keep your position to the end'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 255)]
                elif SPINE_CONDITION and not SPINE_ANGLE:   # 허리를 구부렸을 때
                    voiceFeedback('spine')
                    status = 'Up'
                    feedback = 'Straight your spine'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 0)]
                elif WRIST_CONDITION and not WRIST_RATIO:
                    voiceFeedback('hand')
                    status = 'Up'
                    feedback = 'Put your hands together'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 255)]
                    
            # after each set
            if AFTER_SET_CONDITION:
                prev = time.time()
                if feedback == 'Start':
                    voiceFeedback('rest_time')
                status = 'Rest'
                feedback = 'Take a breathe..'
            if status == 'Rest':
                reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # run timer function
                
            # when exercise is finished
            if AFTER_ALL_SET_CONDITION:
                voiceFeedback('end')
                reps = 0
                status = 'All done'
                sets = 0
                feedback = "Well done!"
                 
            # make table for calculations
            table_calculations(color, avg_arm = avg_arm_angle, avg_spine = avg_spine_angle, wrist_ratio = wrist_shoulder_ratio)
        
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
    