import time
from keypoint import *
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
shoulder_length2 = 0.0
wrist_length = 0.0
elbow_length = 0.0
heel_length = 0.0
foot_length = 0.01
ankle_length = 0.0

elbow_shoulder_ratio = 0.0
wrist_shoulder_ratio = 0.0
heel_foot_ratio = 0.0
ankle_shoulder_ratio = 0.0

left_elbow_angle = 0.0 ## 이스터 초기화
left_shoulder_angle = 0.0
left_knee_angle = 0.0
right_elbow_angle = 0.0
right_shoulder_angle = 0.0
right_knee_angle = 0.0
right_wrist_angle = 0.0


left_shoulder_angle = 0.0 ## side-lateral-raise 초기화
right_shoulder_angle = 0.0
left_elbow_angle = 0.0
right_elbow_angle = 0.0

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
                left_leg_angle, right_leg_angle,\
                heel_length, foot_length, heel_foot_ratio,\
                left_elbow_angle, left_shoulder_angle, left_knee_angle,\
                right_elbow_angle, right_shoulder_angle, right_knee_angle, right_wrist_angle,\
                prev, color
        
        # reference angles
        REF_KNEE_ANGLE = 85.0 ## 무릎 나온거
        REF_LEG_ANGLE = 140.0 ## 140 이하일 때 정답
        MORE_LEG_ANGLE = 160.0 ## 160부터 더 내려가
        LESS_LEG_ANGLE = 70.0 ## 너무 내려갔고
        LESS_HEEL_FOOT_RATIO = 0.6 ## 발 11자 조건
        MORE_HEEL_FOOT_RATIO = 1.4 ## 발 11자 조건       
        
        # conditions
        AFTER_SET_CONDITION = (reps == REF_REPS and status == 'Up')     # 한 세트 이후 조건
        AFTER_ALL_SET_CONDITION = (sets == REF_SETS)                    # 전체 세트 이후 조건
        # KNEEDOWN_CONDITION = (status != 'Rest' and feedback != 'Place your knees behind toes' and feedback != 'Parallel your feet') # 무릎이 발끝 앞으로 나갔을 경우
        KNEEDOWN_CONDITION = (status != 'Rest') # 무릎이 발끝 앞으로 나갔을 경우
        # PARALLEL_CONDITION = (status != 'Rest' and feedback != 'Parallel your feet' and feedback != 'Place your knees behind toes') # 발 11자를 못했을 경우
        PARALLEL_CONDITION = (status != 'Rest') # 발 11자를 못했을 경우
        DEFAULT_CONDITION = (status != 'Rest')  # 운동 중인데 아무것도 아닌 경우
        MOREDOWN_CONDITION = (status != 'Rest' and feedback == 'Start') # 더 구부려야 하는 경우
        COUNT_CONDITION = (status != 'Rest' and feedback == 'Bend your legs more')  # 적절한 경우
        LESSDOWN_CONDITION = (status != 'Rest' and feedback == 'Success')   # 덜 구부려야 하는 경우
        AFTER_REST_CONDITION = (timer == 1 and feedback == 'Take a breathe..') ## 쉬는시간이 끝난 경우(timer가 0이 되는 순간 feedback 출력값이 변경되므로 1로 설정)
        
        # angles in conditions -> '만족하는' 각도
        KNEEDOWN_ANGLE = (avg_knee_angle > REF_KNEE_ANGLE)
        PARALLEL_RATIO = (LESS_HEEL_FOOT_RATIO < heel_foot_ratio < MORE_HEEL_FOOT_RATIO)
        DEFAULT_ANGLE = (left_leg_angle > MORE_LEG_ANGLE and right_leg_angle > MORE_LEG_ANGLE)
        MOREDOWN_ANGLE = (REF_LEG_ANGLE < left_leg_angle < MORE_LEG_ANGLE and REF_LEG_ANGLE < right_leg_angle < MORE_LEG_ANGLE)
        COUNT_ANGLE = (LESS_LEG_ANGLE < left_leg_angle < REF_LEG_ANGLE and LESS_LEG_ANGLE < right_leg_angle < REF_LEG_ANGLE)
        LESSDOWN_ANGLE = (left_leg_angle < LESS_LEG_ANGLE and right_leg_angle < LESS_LEG_ANGLE)
        
        ## easter egg
        RIGHT_ELBOW_ANGLE = (30.0 < right_elbow_angle < 60.0) ## 이스터 기준 각도
        RIGHT_SHOULDER_ANGLE = (140.0 < right_shoulder_angle)
        RIHGHT_WRIST_ANGLE = (130.0 < right_wrist_angle < 160.0)    
        
        RIGHT_KNEE_ANGLE = (160.0 < right_knee_angle)
        LEFT_ELBOW_ANGLE = (160.0 < left_elbow_angle)
        LEFT_SHOULDER_ANGLE = (left_shoulder_angle < 110.0)
        LEFT_KNEE_ANGLE = (160.0 < left_knee_angle)   
        EASTER_CONDITION = (status == 'Up' and feedback == 'Start') ## 이스터
        EASTER_ANGLE = (RIHGHT_WRIST_ANGLE and RIGHT_ELBOW_ANGLE and RIGHT_SHOULDER_ANGLE and RIGHT_KNEE_ANGLE and LEFT_ELBOW_ANGLE and LEFT_SHOULDER_ANGLE and LEFT_KNEE_ANGLE)
        
        # get angles from eact camID
        if camID == LEFT_CAM: ## cam1
            left_leg_angle = self.angle_of_the_right_leg()
            left_knee_angle = self.angle_of_the_left_knee() 
            left_foot_parallel = self.angle_of_left_foot_parallel()  
            left_elbow_angle = self.angle_of_the_left_elbow() ## 이스터
            left_knee_angle = self.angle_of_the_left_knee()
        elif camID == RIGHT_CAM: ## cam0
            right_leg_angle = self.angle_of_the_left_leg()
            right_knee_angle = self.angle_of_the_right_knee()
            right_foot_parallel = self.angle_of_right_foot_parallel()
            heel_length = self.length_of_heel_to_heel()
            foot_length = self.length_of_foot_to_foot()
            right_elbow_angle = self.angle_of_the_right_elbow() ## 이스터
            right_shoulder_angle = self.angle_of_the_right_shoulder()
            right_knee_angle = self.angle_of_the_right_shoulder()
            right_wrist_angle = self.angle_of_the_right_wrist()
        
            # get average    
            ##avg_leg_angle = (left_leg_angle + right_leg_angle) // 2
            avg_knee_angle = (left_knee_angle + right_knee_angle) // 2 
            # avg_foot_parallel = fabs(left_foot_parallel - right_foot_parallel) 
            
            #get ratio
            foot_length = round(foot_length, 4)
            heel_foot_ratio = heel_length / foot_length             
            
            if EASTER_ANGLE and EASTER_CONDITION: ## 이스터
                voiceFeedback('easter')
                status = 'Congratulations'
                feedback = 'Congratulations'
                ##color = [(0, 255, 0), (0, 255, 0), (0, 255, 0)]
                
            # count logic    
            if KNEEDOWN_ANGLE and PARALLEL_RATIO:       # 기본 자세가 만족되고..
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
                elif DEFAULT_CONDITION and DEFAULT_ANGLE and not EASTER_ANGLE and not EASTER_CONDITION :   # 구부리지 않았을 때
                    status = 'Up'
                    feedback = 'Start'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
            else:
                if feedback == 'Success' and (not KNEEDOWN_ANGLE or not PARALLEL_RATIO):    # 카운트가 된 직후 잘못 자세를 잡았을 때
                    reps -= 1
                    status = 'Up'
                    feedback = 'Keep your position to the end'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 255), (0, 0, 0)]
                elif KNEEDOWN_CONDITION and not KNEEDOWN_ANGLE:   # 무릎이 발끝 앞으로 나갔을 때
                    if feedback != 'Place your knees behind toes':
                        voiceFeedback('kneedown')
                    status = 'Up'
                    feedback = 'Place your knees behind toes'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 0), (0, 0, 0)] 
                elif PARALLEL_CONDITION and not PARALLEL_RATIO: # 발이 11자가 아닐 때
                    if feedback != 'Parallel your feet':
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
            if AFTER_REST_CONDITION: ## 쉬는 시간이 종료될 경우
                voiceFeedback('start_exercise') ## 다시 운동할 시간
                feedback = 'Start exercise again'
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
            table_calculations(color, right_leg = right_leg_angle, avg_knee = avg_knee_angle, foot_ratio = heel_foot_ratio, avg_parallel = avg_foot_parallel)
            ##table_calculations(color, easter_elbow = right_elbow_angle, easter_shoulder = right_shoulder_angle, easter_wrist = right_wrist_angle) ## 이스터 확인용
            
        return [reps, status, sets, feedback, timer, camID]

    # pushup function
    def pushup(self, reps, status, sets, feedback, timer, camID):
        global left_arm_angle, right_arm_angle,\
                left_spine_angle, right_spine_angle,\
                shoulder_length, wrist_length,\
                elbow_shoulder_ratio, wrist_shoulder_ratio,\
                prev, color   
        
        # reference angles
        REF_ARM_ANGLE = 80.0
        REF_SPINE_ANGLE = 130.0
        MORE_ARM_ANGLE = 100.0
        REF_WRIST_SHOULDER_RATIO = 1.8
        
        # conditions
        AFTER_SET_CONDITION = (reps == REF_REPS and status == 'Up')     # 한 세트 이후 조건
        AFTER_ALL_SET_CONDITION = (sets == REF_SETS)                    # 전체 세트 이후 조건
        # SPINE_CONDITION = (status != 'Rest' and feedback != 'Straight your spine' and feedback != 'Put your hands together')    # 허리 구부렸을 때
        SPINE_CONDITION = status != 'Rest'    # 허리 구부렸을 때
        # WRIST_CONDITION = (status != 'Rest' and feedback != 'Put your hands together' and feedback != 'Straight your spine')    # 팔 넓이
        WRIST_CONDITION = status != 'Rest'      # 팔 넓이
        DEFAULT_CONDITION = (status != 'Rest')  # 운동 중인데 아무것도 아닌 경우
        MOREDOWN_CONDITION = (status != 'Rest' and feedback == 'Start') # 더 구부려야 하는 경우
        COUNT_CONDITION = (status != 'Rest' and feedback == 'Bend your arms more')  # 적절한 경우
        AFTER_REST_CONDITION = (timer == 1 and feedback == 'Take a breathe..') ## 쉬는시간이 끝난 경우(timer가 0이 되는 순간 feedback 출력값이 변경되므로 1로 설정)
        
        # angles in conditions -> '만족하는' 각도
        SPINE_ANGLE = (left_spine_angle > REF_SPINE_ANGLE and right_spine_angle > REF_SPINE_ANGLE)
        # WRIST_ANGLE = (LESS_WRIST_ANGLE < avg_wrist_angle < MORE_WRIST_ANGLE)
        WRIST_RATIO = (wrist_shoulder_ratio < REF_WRIST_SHOULDER_RATIO)
        DEFAULT_ANGLE = (left_arm_angle > MORE_ARM_ANGLE and right_arm_angle > MORE_ARM_ANGLE)
        MOREDOWN_ANGLE = (REF_ARM_ANGLE < left_arm_angle < MORE_ARM_ANGLE and REF_ARM_ANGLE < right_arm_angle < MORE_ARM_ANGLE)
        COUNT_ANGLE = (left_arm_angle < REF_ARM_ANGLE and right_arm_angle < REF_ARM_ANGLE)
        
        # get angles from eact camID
        if camID == LEFT_CAM:
            left_spine_angle = self.angle_of_the_left_spine()
            left_arm_angle = self.angle_of_the_left_elbow()
            # elbow_length = self.length_of_elbow_to_elbow()
        elif camID == RIGHT_CAM:
            right_spine_angle = self.angle_of_the_right_spine()
            right_arm_angle = self.angle_of_the_right_elbow()
            wrist_length = self.length_of_wrist_to_wrist()
            shoulder_length = self.length_of_shoulder_to_shoulder()
            
            # get average
            """avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 
            avg_spine_angle = (left_spine_angle + right_spine_angle) // 2"""
            
            # get ratio
            shoulder_length = round(shoulder_length, 4)
            if right_arm_angle > 160:
                wrist_shoulder_ratio = wrist_length / shoulder_length
            
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
                    if feedback != 'Straight your spine':
                        voiceFeedback('spine')
                    status = 'Up'
                    feedback = 'Straight your spine'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 0)]
                elif WRIST_CONDITION and not WRIST_RATIO:
                    if feedback != 'Put your hands together':
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
            if AFTER_REST_CONDITION: ## 쉬는시간이 종료될 경우
                voiceFeedback('start_exercise') ## 다시 운동 시작    
                feedback = 'Start exercise again' 
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
            table_calculations(color, right_arm = right_arm_angle, right_spine = right_spine_angle, wrist_ratio = wrist_shoulder_ratio)
        
        return [reps, status, sets, feedback, timer, camID]
    
    # side lateral raise function
    def sidelateralraise(self, reps, status, sets, feedback, timer, camID):
        global left_elbow_angle, right_elbow_angle,\
                left_shoulder_angle, right_shoulder_angle,\
                ankle_length, shoulder_length, ankle_shoulder_ratio, ankle_shoulder_ratio2,\
                prev, color   
                
        # reference angles
        REF_SHOULDER_ANGLE = 145.0 
        LESS_SHOULDER_ANGLE = 120.0
        MORE_SHOULDER_ANGLE = 175.0
        DEFAULT_SHOULDER_ANGLE = 100.0
        REF_ELBOW_ANGLE = 110.0
        LESS_ANKLE_SHOLDER_RATIO = 0.6 ## 발이 어께 너비일 조건
        MORE_ANKLE_SHOLDER_RATIO = 1.3 ## 발이 어께 너비일 조건   
        
        # conditions
        AFTER_SET_CONDITION = (reps == REF_REPS and status == 'Down')     # 한 세트 이후 조건
        AFTER_ALL_SET_CONDITION = (sets == REF_SETS)                        # 전체 세트 이후 조건
        MORE_RAISE_CONDITION = (status != 'Rest' and feedback == 'Success')   # 팔을 더 들어야하는 경우
        LESS_RAISE_CONDITION = (status != 'Rest' and feedback == 'Start')   # 팔을 조금 내려야하는 경우
        ANKLE_SHOULDER_RATIO_CONDITION = (status == 'Rest') # 발 어께너비로 벌리지 못했을 경우
        COUNT_CONDITION = (status != 'Rest' and feedback == 'raise your arm more')  # 적절한 경우
        AFTER_REST_CONDITION = (timer == 1 and feedback == 'Take a breathe..') ## 쉬는시간이 끝난 경우(timer가 0이 되는 순간 feedback 출력값이 변경되므로 1로 설정)
        DEFAULT_CONDITION = (status != 'Rest')  # 운동 중인데 아무것도 아닌 경우      
        
        # angles in conditions -> '만족하는' 각도
        ELBOW_ANGLE = ((REF_ELBOW_ANGLE < left_elbow_angle) and (REF_ELBOW_ANGLE < right_elbow_angle)) ## 정확한 팔꿈치 각도
        LESS_BEND_ANGLE = ((left_elbow_angle < REF_ELBOW_ANGLE) and (right_elbow_angle < REF_ELBOW_ANGLE))  ## 너무 적게 폈을 때
        SHOULDER_ANGLE = ((REF_SHOULDER_ANGLE < left_shoulder_angle < MORE_SHOULDER_ANGLE) and (REF_SHOULDER_ANGLE < right_shoulder_angle < MORE_SHOULDER_ANGLE))   ## 정확한 어깨 각도
        MORE_RAISE_ANGLE = ((left_shoulder_angle > MORE_SHOULDER_ANGLE) or (right_shoulder_angle > MORE_SHOULDER_ANGLE))   ## 너무 많이 벌렸을 때
        LESS_RAISE_ANGLE = ((LESS_SHOULDER_ANGLE < left_shoulder_angle < REF_SHOULDER_ANGLE) or (LESS_SHOULDER_ANGLE < right_shoulder_angle < REF_SHOULDER_ANGLE))   ## 너무 많이 벌렸음 
        DEFAULT_ANGLE = ((left_shoulder_angle < DEFAULT_SHOULDER_ANGLE) and (right_shoulder_angle < DEFAULT_SHOULDER_ANGLE)) ## 기본자세
        ANKLE_SHOULDER_RATIO_REF = (LESS_ANKLE_SHOLDER_RATIO < ankle_shoulder_ratio < MORE_ANKLE_SHOLDER_RATIO)
        
        # get angles from eact camID
        if camID == LEFT_CAM: ## 노트북
            left_shoulder_angle = self.angle_of_the_left_shoulder()
            left_elbow_angle = self.angle_of_the_left_elbow()
            ankle_length = self.length_of_ankle_to_ankle()
            shoulder_length = self.length_of_shoulder_to_shoulder()
        elif camID == RIGHT_CAM:
            right_shoulder_angle = self.angle_of_the_right_shoulder()
            right_elbow_angle = self.angle_of_the_right_elbow()
            
            # get average 없애는게 좋을듯?    
            """average_shoulder_angle = (left_shoulder_angle + right_shoulder_angle) // 2
            average_elbow_angle = (left_elbow_angle + right_elbow_angle) // 2""" 
            

            # get ratio
            shoulder_length2 = round(shoulder_length, 4)
            ankle_shoulder_ratio = ankle_length / shoulder_length2
            
            # count logic
            if ELBOW_ANGLE and ANKLE_SHOULDER_RATIO_REF:         # 기본 자세가 만족되고(팔꿈치가 적절히 구부려짐)   
                if MORE_RAISE_CONDITION and MORE_RAISE_ANGLE:  ## 너무 많이 올렸을 때
                    voiceFeedback('lessraise')
                    reps -= 1
                    status = 'Down'
                    feedback = 'raise your arm less'
                    color = [(0, 0, 255), (0, 0, 255), (0, 0, 0)] 
                elif COUNT_CONDITION and SHOULDER_ANGLE: # 적절하게 올렸을 때
                    voiceFeedback('buzzer')
                    reps += 1
                    status = 'Up'
                    feedback = 'Success'
                    color = [(255, 0, 0), (255, 0, 0), (255, 0, 0)]
                elif LESS_RAISE_CONDITION and LESS_RAISE_ANGLE:  ## 너무 적게 올렸을 때
                    voiceFeedback('moreraise')
                    status = 'Down'
                    feedback = 'raise your arm more'
                    color = [(0, 0, 255), (0, 0, 255), (0, 0, 0)]        
                elif DEFAULT_CONDITION and DEFAULT_ANGLE:  ## 디폴트 상태
                    status = 'Down'
                    feedback = 'Start'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 0)]      
            else:
                if feedback == 'Success' and (not ELBOW_ANGLE or not ANKLE_SHOULDER_RATIO_REF):  # 카운트가 된 직후 잘못 자세를 잡았을 때
                    reps -= 1
                    status = 'Down'
                    feedback = 'Keep your position to the end'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 255)]
                elif DEFAULT_CONDITION and LESS_BEND_ANGLE:   ## 팔꿈치를 더 구부려야함
                    if feedback != 'bend your elbow less':
                        voiceFeedback('lessbend')
                    status = 'Down'
                    feedback = 'bend your elbow less'
                    color = [(0, 0, 0), (0, 0, 255), (0, 0, 255)]     
                elif   not ANKLE_SHOULDER_RATIO_REF: # 발을 어께 너비로 벌리지 않았을때  ANKLE_SHOULDER_RATIO_CONDITION and
                    if feedback != 'Stand with your feet shoulder-width apart':
                        voiceFeedback('parallel')#발을 어께 너비로 벌리는 wav 추가해야함
                    status = 'Down'
                    feedback = 'Stand with your feet shoulder-width apart'
                    color = [(0, 0, 0), (0, 0, 0), (0, 0, 255)]       
                
            # after each set
            if AFTER_SET_CONDITION:
                prev = time.time()
                if feedback == 'Start':
                    voiceFeedback('rest_time')
                status = 'Rest'
                feedback = 'Take a breathe..'
            if AFTER_REST_CONDITION: ## 쉬는시간이 종료될 경우
                voiceFeedback('start_exercise') ## 다시 운동 시작    
                feedback = 'Start exercise again' 
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
            #table_calculations(color,  ankle_length =  ankle_length, shoulder_length2 = shoulder_length2, ankle_shoulder = ankle_shoulder_ratio)   발목 어께 비율 계산용
            table_calculations(color, right_shoulder = right_shoulder_angle, right_elbow = right_elbow_angle,  ankle_shoulder = ankle_shoulder_ratio)
        
        return [reps, status, sets, feedback, timer, camID]

    # select mode
    def calculate_exercise(self, exercise, reps, status, sets, feedback, timer, camID): 
        if exercise == "pushup":
            reps, status, sets, feedback, timer, camID = EXERCISE(self.landmarks).pushup(
                reps, status, sets, feedback, timer, camID)
        elif exercise == "squat":
            reps, status, sets, feedback, timer, camID = EXERCISE(self.landmarks).squat(
                reps, status, sets, feedback, timer, camID)
        elif exercise == "sidelateralraise":
            reps, status, sets, feedback, timer, camID = EXERCISE(self.landmarks).sidelateralraise(
                reps, status, sets, feedback, timer, camID)    
        
        return [reps, status, sets, feedback, timer, camID]
    
