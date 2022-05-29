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
                prev, color
        
        # reference angles
        REF_KNEE_ANGLE = 140.0
        REF_LEG_ANGLE = 100.0
        ALLOW_RATE = 0.1        # 허용 오차 비율
        MEASURE_RATE = 0.5      # 에러 오차 비율  ex) too much < 100-10 < good < 100+10 < more < 100+50 < default
        
        # get angles from eact camID
        if camID == LEFT_CAM:
            left_leg_angle = self.angle_of_the_right_leg()
            left_knee_angle = self.angle_of_the_left_knee()   
        elif camID == RIGHT_CAM:
            right_leg_angle = self.angle_of_the_left_leg()
            right_knee_angle = self.angle_of_the_right_knee()
            
            # get average    
            avg_leg_angle = (left_leg_angle + right_leg_angle) // 2
            avg_knee_angle = (left_knee_angle + right_knee_angle) // 2  
            
            # get ready state
            if status != 'Rest' and status != 'All done':
                ready = True
            else:
                ready = False
            
            # count logic
            if ready == True and avg_knee_angle > REF_KNEE_ANGLE:   # 기본 자세가 충족된 상태에서 무릎을 구부릴 때
                if feedback == 'Success' and avg_leg_angle < REF_LEG_ANGLE*(1-ALLOW_RATE): # 너무 많이 구부렸을 때
                    voiceFeedback('lessdown')
                    reps -= 1
                    status = 'Up'
                    feedback = 'Bend your legs less'
                    color = [(0, 0, 255), (0, 0, 0)]        
                elif feedback == 'Bend your legs more' and REF_LEG_ANGLE*(1-ALLOW_RATE) < avg_leg_angle < REF_LEG_ANGLE*(1+ALLOW_RATE):    # 적절하게 구부렸을 때
                    voiceFeedback('buzzer')
                    reps += 1
                    status = 'Down'
                    feedback = 'Success'
                    color = [(255, 0, 0), (255, 0, 0)]
                elif feedback == 'Start' and REF_LEG_ANGLE*(1+ALLOW_RATE) < avg_leg_angle < REF_LEG_ANGLE*(1+MEASURE_RATE):  # 너무 적게 구부렸을 때
                    voiceFeedback('moredown')
                    status = 'Up'
                    feedback = 'Bend your legs more'
                    color = [(0, 0, 255), (0, 0, 0)]
                elif REF_LEG_ANGLE*(1+MEASURE_RATE) < avg_leg_angle:   # 구부리지 않았을 때
                    status = 'Up'
                    feedback = 'Start'
                    color = [(0, 0, 0), (0, 0, 0)]
            elif ready == True and feedback != 'Place your knees behind toes' and avg_knee_angle < REF_KNEE_ANGLE: # 기본 자세 충족 안됨 -> 무릎이 발끝보다 앞에 있을 때
                voiceFeedback('kneedown')
                status = 'Up'
                feedback = 'Place your knees behind toes'
                color = [(0, 0, 0), (0, 0, 255)]
                    
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
                
            # make table for avg_angles
            table_calculations(color, avg_leg = avg_leg_angle, avg_knee = avg_knee_angle)
                            #    heel = length_heel, ankle = length_ankle, foot = length_foot)
            
        return [reps, status, sets, feedback, timer, camID]

    # pushup function
    def pushup(self, reps, status, sets, feedback, timer, camID):
        global left_arm_angle, right_arm_angle, avg_arm_angle,\
                left_spine_angle, right_spine_angle, avg_spine_angle,\
                left_elbow_angle, right_elbow_angle, avg_elbow_angle ,\
                left_wrist_angle, right_wrist_angle, avg_wrist_angle,\
                prev, color   
        
        # reference angles
        REF_ARM_ANGLE = 40.0
        REF_SPINE_ANGLE = 170.0
        REF_ELBOW_ANGLE = 70.0
        REF_WRIST_ANGLE = 15.0
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
                    color = [(255, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0)]
                elif feedback == 'Start' and REF_ARM_ANGLE*(1+ALLOW_RATE) < avg_arm_angle < REF_ARM_ANGLE*(1+MEASURE_RATE): # 너무 적게 구부렸을 때
                    voiceFeedback('moredown')
                    status = 'Up'
                    feedback = 'Bend your arms more'
                    color = [(0, 0, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
                elif REF_ARM_ANGLE*(1+MEASURE_RATE) < avg_arm_angle:    #구부리지 않았을 때
                    status = 'Up'
                    feedback = 'Start'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
            elif ready == True and feedback != 'Straight your spine' and avg_spine_angle < REF_SPINE_ANGLE:   # 기본 자세 충족 안됨 -> 허리가 일직선이 아닐 때
                voiceFeedback('spine')
                status = 'Up'
                feedback = 'Straight your spine'
                color = [(0, 0, 0), (0, 0, 255), (0, 0, 0), (0, 0, 0)]
            elif ready == True and feedback != 'Put your hands together' and avg_wrist_angle > REF_WRIST_ANGLE: # 기본 자세 충족 안됨 -> 손을 너무 크게 벌렸을 때
                voiceFeedback('hand')
                status = 'Up'
                feedback = 'Put your hands together'
                color = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 255)]
                    
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
            table_calculations(color, avg_arm = avg_arm_angle, avg_spine = avg_spine_angle, avg_elbow = avg_elbow_angle, avg_wrist = avg_wrist_angle)
        
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
    