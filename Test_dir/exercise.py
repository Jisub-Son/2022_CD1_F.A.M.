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

left_foot_parallel = 90.0   # 발 11자 각도
right_foot_parallel = 90.0
avg_foot_parallel = 90.0

length_shoudler = 0.0   # 어깨, 발 사이 거리
length_foot = 0.0
length_heel = 0.0
length_ankle = 0.0

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
        global left_knee_angle, right_knee_angle, avg_knee_angle,\
                left_leg_angle, right_leg_angle, avg_leg_angle,\
                prev
        global length_foot, length_heel, length_ankle
        
        # reference angles
        REF_KNEE_ANGLE = 140.0
        REF_LEG_ANGLE = 100.0
        ALLOW_RATE = 0.1       # 허용 오차 비율
        MEASURE_RATE = 0.5       # 에러 오차 비율  ex) less < 90 < good < 110 < more < 150 < default
        
        # get angles from eact camID
        if camID == LEFT_CAM:
            left_leg_angle = self.angle_of_the_right_leg()
            left_knee_angle = self.angle_of_the_left_knee()
            '''length_foot = self.length_of_foot_to_foot()      ### 11자로 두면 3개 값이 나름 비슷하게 나오는데 문제는
            length_ankle = self.length_of_ankle_to_ankle()      ### 한 카메라 안에 양 발 landmark가 다 나와야 해    
            length_heel = self.length_of_heel_to_heel()'''      
        elif camID == RIGHT_CAM:
            right_leg_angle = self.angle_of_the_left_leg()
            right_knee_angle = self.angle_of_the_right_knee()
            
            # get average    
            avg_leg_angle = (left_leg_angle + right_leg_angle) // 2
            avg_knee_angle = (left_knee_angle + right_knee_angle) // 2  
            
            # make table for avg_angles
            table_calculations(avg_leg = avg_leg_angle, avg_knee = avg_knee_angle,
                               heel = length_heel, ankle = length_ankle, foot = length_foot)
                    
            # how to make count
            # 무릎이 발끝보다 뒤에 있고 and 무를을 충분히 굽혔을 때 count
            if status == 'Up' and avg_knee_angle > REF_KNEE_ANGLE\
                and REF_LEG_ANGLE*(1-ALLOW_RATE) < avg_leg_angle < REF_LEG_ANGLE*(1+ALLOW_RATE):    
                voiceFeedback('buzzer')
                reps += 1
                status = 'Down'
                feedback = 'Success'
                prev = time.time()
            else:
                # 우선순위1 : 무릎을 충분히 굽히지 않았을 때 + 무릎이 발끝보다 뒤에
                if (status != 'Rest' and status != 'All done') and avg_knee_angle > REF_KNEE_ANGLE\
                    and REF_LEG_ANGLE*(1+ALLOW_RATE) < avg_leg_angle < REF_LEG_ANGLE*(1+MEASURE_RATE):  
                    status = 'Up'
                    feedback = 'Bend your legs'
                # 우선순위2 : 무릎이 발끝보다 앞쪽에 있을 때
                elif (status != 'Rest' and status != 'All done') and avg_knee_angle < REF_KNEE_ANGLE:
                    status = 'Up'
                    feedback = 'Place your knees behind toes'
                # elif (status != 'Rest' and status != 'All done') and avg_knee_angle > REF_KNEE_ANGLE\
                #     and REF_LEG_ANGLE*(1+MEASURE_RATE) < avg_leg_angle:
                    
            # after each set
            if reps == REF_REPS:
                if timer == 5:
                    voiceFeedback('rest_time')
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
        global left_arm_angle, right_arm_angle, avg_arm_angle,\
                left_spine_angle, right_spine_angle, avg_spine_angle,\
                prev   
        
        # reference angles
        REF_ARM_ANGLE = 90.0
        REF_SPINE_ANGLE = 170.0
        
        # get angles from eact camID
        if camID == LEFT_CAM:
            left_spine_angle = self.angle_of_the_left_spine()
            left_arm_angle = self.angle_of_the_left_arm()
        elif camID == RIGHT_CAM:
            right_spine_angle = self.angle_of_the_right_spine()
            right_arm_angle = self.angle_of_the_right_arm()
        
            # get average
            avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 
            avg_spine_angle = (left_spine_angle + right_spine_angle) // 2 
            
            # make table for calculations
            table_calculations(avg_arm = avg_arm_angle, avg_spine = avg_spine_angle)
                
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
                if timer == 5:
                    voiceFeedback('rest_time')
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
    