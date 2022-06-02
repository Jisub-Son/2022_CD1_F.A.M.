import time
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

length_shoudler = 0.0   # 어깨, 발 사이 거리
length_foot = 0.0
length_heel = 0.0
length_ankle = 0.0

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
                prev, color
        
        # reference angles
        REF_KNEE_ANGLE = 135.0
        REF_LEG_ANGLE = 140.0
        MORE_LEG_ANGLE = 160.0
        LESS_LEG_ANGLE = 60.0
        LESS_PARALLEL_ANGLE = 0.0
        MORE_PARALLEL_ANGLE = 60.0 
        
        AFTER_SET_CONDITION = (reps == REF_REPS and status == 'Up')
        AFTER_ALL_SET_CONDITION = (sets == REF_SETS)
        
        KNEEDOWN_CONDITION = (status != 'Rest' and feedback != 'Place your knees behind toes' and feedback != 'Parallel your feet')
        PARALLEL_CONDITION = (status != 'Rest' and feedback != 'Parallel your feet' and feedback != 'Place your knees behind toes')
        DEFAULT_CONDITION = (status != 'Rest')
        MOREDOWN_CONDITION = (status != 'Rest' and feedback == 'Start')
        COUNT_CONDITION = (status != 'Rest' and feedback == 'Bend your legs more')
        LESSDOWN_CONDITION = (status != 'Rest' and feedback == 'Success')
        
        # 만족하는 각도
        KNEEDOWN_ANGLE = (avg_knee_angle > REF_KNEE_ANGLE)
        PARALLEL_ANGLE = (LESS_PARALLEL_ANGLE < avg_foot_parallel < MORE_PARALLEL_ANGLE)
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
            
            # get average    
            avg_leg_angle = (left_leg_angle + right_leg_angle) // 2
            avg_knee_angle = (left_knee_angle + right_knee_angle) // 2 
            avg_foot_parallel = fabs(left_foot_parallel - right_foot_parallel) 
                
            # count logic
            if KNEEDOWN_ANGLE and PARALLEL_ANGLE:
                if LESSDOWN_CONDITION and LESSDOWN_ANGLE:
                    print("condition 1")
                    voiceFeedback('lessdown')
                    reps -= 1
                    status = 'Up'
                    feedback = 'Bend your legs less'
                    color = [(0, 0, 255), (0, 0, 0), (0, 0, 0)]
                elif COUNT_CONDITION and COUNT_ANGLE:
                    print("condition 2")
                    voiceFeedback('buzzer')
                    reps += 1
                    status = 'Down'
                    feedback = 'Success'
                    prev = time.time()
                    color = [(255, 0, 0), (255, 0, 0), (255, 0, 0)]
                elif MOREDOWN_CONDITION and MOREDOWN_ANGLE:
                    print("condition 3")
                    voiceFeedback('moredown')
                    status = 'Up'
                    feedback = 'Bend your legs more'
                    color = [(0, 0, 255), (0, 0, 0), (0, 0, 0)]
                elif DEFAULT_CONDITION and DEFAULT_ANGLE:
                    print("condition 4")
                    status = 'Up'
                    feedback = 'Start'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]
            else:
                if KNEEDOWN_CONDITION and not KNEEDOWN_ANGLE:
                    print("condition 5")
                    voiceFeedback('kneedown')
                    status = 'Up'
                    feedback = 'Place your knees behind toes'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 0)] 
                elif PARALLEL_CONDITION and not PARALLEL_ANGLE:
                    print("condition 6")
                    voiceFeedback('parallel')
                    status = 'Up'
                    feedback = 'Parallel your feet'
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
                
            # make table for avg_angles
            table_calculations(color, avg_leg = avg_leg_angle, avg_knee = avg_knee_angle, avg_parallel = avg_foot_parallel)
            
        return [reps, status, sets, feedback, timer, camID]

    # pushup function
    def pushup(self, reps, status, sets, feedback, timer, camID):
        global left_arm_angle, right_arm_angle, avg_arm_angle,\
                left_spine_angle, right_spine_angle, avg_spine_angle,\
                left_elbow_angle, right_elbow_angle, avg_elbow_angle ,\
                left_wrist_angle, right_wrist_angle, avg_wrist_angle,\
                prev, color   
        
        # reference angles
        REF_ARM_ANGLE = 75.0
        REF_SPINE_ANGLE = 130.0
        REF_ELBOW_ANGLE = 70.0
        REF_WRIST_ANGLE = 27.0
        ALLOW_RATE = 0.1        # 허용 오차 비율
        MEASURE_RATE = 0.5      # 에러 오차 비율  ex) good < 40+4 < more < 40+20 < default
        
        # get angles from eact camID
        if camID == LEFT_CAM:
            left_spine_angle = self.angle_of_the_left_spine()
            left_arm_angle = self.angle_of_the_left_arm()
            left_elbow_angle = self.angle_of_the_left_elbow()
            left_wrist_angle = self.angle_of_the_left_wrist()
        elif camID == RIGHT_CAM:
            right_spine_angle = self.angle_of_the_right_spine()
            right_arm_angle = self.angle_of_the_right_arm()
            right_elbow_angle = self.angle_of_the_right_elbow()
            right_wrist_angle = self.angle_of_the_right_wrist()
        
            # get average
            avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 
            avg_spine_angle = (left_spine_angle + right_spine_angle) // 2 
            avg_elbow_angle = (left_elbow_angle + right_elbow_angle) // 2
            avg_wrist_angle = (left_wrist_angle + right_wrist_angle) // 2

            # get ready state
            if status != 'Rest' and status != 'All done':
                ready = True
            else:
                ready = False

            # count logic
            if ready == True and avg_spine_angle > REF_SPINE_ANGLE and avg_wrist_angle < REF_WRIST_ANGLE:     # 기본 자세가 충족된 상태에서 무릎을 구부릴 때
                if feedback == 'Bend your arms more' and avg_arm_angle < REF_ARM_ANGLE*(1+ALLOW_RATE):  # 적절하게 구부렸을 때
                    voiceFeedback('buzzer')
                    reps += 1
                    status = 'Down'
                    feedback = 'Success'
                    color = [(255, 0, 0), (255, 0, 0), (255, 0, 0), (0, 0, 0)]
                elif feedback == 'Start' and REF_ARM_ANGLE*(1+ALLOW_RATE) < avg_arm_angle < REF_ARM_ANGLE*(1+MEASURE_RATE): # 너무 적게 구부렸을 때
                    voiceFeedback('moredown')
                    status = 'Up'
                    feedback = 'Bend your arms more'
                    color = [(0, 0, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
                elif REF_ARM_ANGLE*(1+MEASURE_RATE) < avg_arm_angle:    #구부리지 않았을 때
                    status = 'Up'
                    feedback = 'Start'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
            
            elif ready == True and feedback != 'Put your hands together' and feedback != 'Straight your spine' and avg_wrist_angle > REF_WRIST_ANGLE: # 기본 자세 충족 안됨 -> 손을 너무 크게 벌렸을 때
                voiceFeedback('hand')
                status = 'Up'
                feedback = 'Put your hands together'
                color = [(0, 0, 0), (0, 0, 0), (0, 0, 255), (0, 0, 0)]
            elif ready == True and feedback != 'Straight your spine' and feedback != 'Put your hands together' and avg_spine_angle < REF_SPINE_ANGLE:   # 기본 자세 충족 안됨 -> 허리가 일직선이 아닐 때
                voiceFeedback('spine')
                status = 'Up'
                feedback = 'Straight your spine'
                color = [(0, 0, 0), (0, 0, 255), (0, 0, 0), (0, 0, 0)]
                    
            # after each set
            if reps == REF_REPS and status == 'Up':
                prev = time.time()
                if feedback == 'Start':
                    voiceFeedback('rest_time')
                status = 'Rest'
                feedback = 'Take a breathe..'
            if status == 'Rest':
                reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # run timer function
                
            # when exercise is finished
            if sets == REF_SETS:
                voiceFeedback('end')
                reps = 0
                status = 'All done'
                sets = 0
                feedback = "Well done!"
                 
            # make table for calculations
            table_calculations(color, avg_arm = avg_arm_angle, avg_spine = avg_spine_angle, avg_wrist = avg_wrist_angle)
        
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
    