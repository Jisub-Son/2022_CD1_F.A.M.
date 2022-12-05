import time
from datetime import datetime
from keypoint import *
from utils import voiceFeedback
from utils import LEFT_CAM, RIGHT_CAM, REF_TIMER, REF_SETS, REF_REPS

cur = 0.0 # 타이머 초기화
prev = 0.0
timeElapsed = 0.0

left_leg_angle = 180.0 # 스쿼트 초기화
right_leg_angle = 180.0
avg_leg_angle = 180.0
left_knee_angle = 120.0
right_knee_angle = 120.0
avg_knee_angle = 120.0
heel_length = 10.0
foot_length = 10.0
shoulder_length = 10.0
heel_foot_ratio = 1.0
heel_shoulder_ratio = 1.0

left_arm_angle = 180.0 # 푸쉬업 초기화
right_arm_angle = 180.0
avg_arm_angle = 180.0
left_spine_angle = 180.0
right_spine_angle = 180.0
avg_spine_angle = 180.0
wrist_length = 10.0
wrist_shoulder_ratio = 1.0

left_shoulder_angle = 110.0 # 사레레 초기화
right_shoulder_angle = 110.0
avg_shoulder_angle = 110
left_elbow_angle = 180.0
right_elbow_angle = 180.0
avg_elbow_angle = 180

now = datetime.now() # 프로그램 시작 시간

class MEASURE:
    def __init__(self, angle_list0, angle_list1, state_info):
        self.angle_list0 = angle_list0
        self.angle_list1 = angle_list1
        self.state_info = state_info
    
    # timer function
    def Rest_timer(self, reps, status, sets, feedback, timer):
        global cur, prev, timeElapsed, flag
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
    
    def squat(self, reps, status, sets, feedback, timer):
        global left_knee_angle, right_knee_angle, avg_knee_angle,\
                left_leg_angle, right_leg_angle, avg_leg_angle,\
                heel_length, foot_length, shoulder_length,\
                heel_foot_ratio, heel_shoulder_ratio,\
                left_elbow_angle, right_elbow_angle,\
                left_shoulder_angle, right_shoulder_angle,\
                prev, squat_log
                
        squat_log = open('log/squat_log/SquatLog_' + str(now.strftime('%Y%m%d %H%M%S')) + '.txt', 'a') # a: 이어쓰기
        
        # reference angles
        REF_KNEE_ANGLE = 140.0 ## 무릎 나온거
        MORE_LEG_ANGLE = 160.0 ## 더 내려가
        REF_LEG_ANGLE = 140.0 ## 정답
        LESS_LEG_ANGLE = 90.0 ## 너무 내려갔고
        LESS_HEEL_FOOT_RATIO = 0.5 ## 발 11자 조건
        MORE_HEEL_FOOT_RATIO = 1.3
        LESS_SHOULDER_RATIO = 0.4 # 두 발 어깨 넓이     
        MORE_SHOULDER_RATIO = 1.1
        
        # conditions
        AFTER_SET_CONDITION = (reps == REF_REPS and status == 'Up')     # 한 세트 이후 조건
        AFTER_ALL_SET_CONDITION = (sets == REF_SETS)                    # 전체 세트 이후 조건
        DEFAULT_CONDITION = (status != 'Rest')  # default
        MOREDOWN_CONDITION = (status != 'Rest' and feedback == 'Start') # 더 구부려야 하는 경우
        COUNT_CONDITION = (status != 'Rest' and feedback == 'Bend your legs more')  # 적절한 경우
        LESSDOWN_CONDITION = (status != 'Rest' and feedback == 'Success')   # 덜 구부려야 하는 경우
        AFTER_REST_CONDITION = (timer == 1 and feedback == 'Take a breathe..') ## 쉬는시간이 끝난 경우(timer가 0이 되는 순간 feedback 출력값이 변경되므로 1로 설정)
        
        # angles in conditions -> '만족하는' 각도
        KNEEDOWN_ANGLE = (avg_knee_angle > REF_KNEE_ANGLE)
        PARALLEL_RATIO = (LESS_HEEL_FOOT_RATIO < heel_foot_ratio < MORE_HEEL_FOOT_RATIO)
        HEEL_RATIO = (LESS_SHOULDER_RATIO < heel_shoulder_ratio < MORE_SHOULDER_RATIO)
        DEFAULT_ANGLE = (avg_leg_angle > MORE_LEG_ANGLE)
        MOREDOWN_ANGLE = (REF_LEG_ANGLE < avg_leg_angle < MORE_LEG_ANGLE)
        COUNT_ANGLE = (LESS_LEG_ANGLE < avg_leg_angle < REF_LEG_ANGLE)
        LESSDOWN_ANGLE = (avg_leg_angle < LESS_LEG_ANGLE)
        
        # easter egg: 1차 테스트 완료
        EASTER_ELBOW_ANGLE = (170.0 < left_elbow_angle and 30.0 < right_elbow_angle < 50.0)
        EASTER_SHOULDER_ANGLE = (70.0 < left_shoulder_angle < 120.0 and 60.0 < right_shoulder_angle < 100)
        EASTER_CONDITION = (status == 'Up' and feedback == 'Start')
        EASTER_ANGLE = (DEFAULT_ANGLE and EASTER_ELBOW_ANGLE and EASTER_SHOULDER_ANGLE)
        
        # get angles
        try:
            left_leg_angle = self.angle_list0[0]
            left_knee_angle = self.angle_list0[1]
            left_elbow_angle = self.angle_list0[2]
            left_shoulder_angle = self.angle_list0[3]
            right_leg_angle = self.angle_list1[0]
            right_knee_angle = self.angle_list1[1]
            heel_length = self.angle_list1[2]
            foot_length = self.angle_list1[3]
            shoulder_length = self.angle_list1[4]
            right_elbow_angle = self.angle_list1[5]
            right_shoulder_angle = self.angle_list1[6]
            # right_hand_angle = self.angle_list1[7]
        except:
            pass
        # get average    
        avg_knee_angle = (left_knee_angle + right_knee_angle) // 2  
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2
        
        #get ratio
        foot_length = round(foot_length, 4)
        if foot_length != 0:
            heel_foot_ratio = heel_length / foot_length
            
        shoulder_length = round(shoulder_length, 4)
        if right_leg_angle > 160:
            heel_shoulder_ratio = heel_length / shoulder_length
            
        if EASTER_ANGLE and EASTER_CONDITION: ## 이스터
            voiceFeedback('easter')
            status = 'Congratulations'
            feedback = 'Congratulations'
            squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
        
        # count logic    
        if KNEEDOWN_ANGLE and PARALLEL_RATIO and HEEL_RATIO:       # 기본 자세가 만족되고..
            if LESSDOWN_CONDITION and LESSDOWN_ANGLE:   # 많이 구부렸을 때
                voiceFeedback('lessdown')
                reps -= 1
                status = 'Up'
                feedback = 'Bend your legs less'
                squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif COUNT_CONDITION and COUNT_ANGLE:       # 적절히 구부렸을 때
                voiceFeedback('buzzer')
                reps += 1
                status = 'Down'
                feedback = 'Success'
                squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
                prev = time.time()
            elif MOREDOWN_CONDITION and MOREDOWN_ANGLE: # 덜 구부렸을 때 (log 확인 배제)
                voiceFeedback('moredown')
                status = 'Up'
                feedback = 'Bend your legs more'
            elif DEFAULT_CONDITION and DEFAULT_ANGLE and not EASTER_ANGLE and not EASTER_CONDITION :   # 구부리지 않았을 때 (log 배제)
                status = 'Up'
                feedback = 'Start'
        else:
            if feedback == 'Success' and (not KNEEDOWN_ANGLE or not PARALLEL_RATIO or not HEEL_RATIO):    # 카운트가 된 직후 잘못 자세를 잡았을 때
                reps -= 1
                status = 'Up'
                feedback = 'Keep your position to the end'
                squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif DEFAULT_CONDITION and not KNEEDOWN_ANGLE:   # 무릎이 발끝 앞으로 나갔을 때
                if feedback != 'Place your knees behind toes':
                    voiceFeedback('kneedown')
                status = 'Up'
                feedback = 'Place your knees behind toes'
                squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif DEFAULT_CONDITION and not PARALLEL_RATIO: # 발이 11자가 아닐 때
                if feedback != 'Parallel your feet':
                    voiceFeedback('parallel')
                status = 'Up'
                feedback = 'Parallel your feet'
                squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif DEFAULT_CONDITION and not HEEL_RATIO: # 발이 어깨넓이가 아닐 때
                if feedback != 'Spread your feet shoulder width':
                    voiceFeedback('shoulder_length')
                status = 'Up'
                feedback = 'Spread your feet shoulder width'
                squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")        
        # after each set
        if AFTER_SET_CONDITION:
            prev = time.time()
            if feedback == 'Start':
                voiceFeedback('rest_time')
            status = 'Rest'
            feedback = 'Take a breathe..'
            squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
        if AFTER_REST_CONDITION: ## 쉬는 시간이 종료될 경우
            voiceFeedback('start_exercise') ## 다시 운동할 시간
            feedback = 'Start exercise again'
            squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
        if status == 'Rest':
            reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # run timer function
        
        # when exercise is finished
        if AFTER_ALL_SET_CONDITION:
            voiceFeedback('end')
            reps = 0
            status = 'All done'
            sets = 0
            feedback = "Well done!"
            squat_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            squat_log.write("Total Reps: " + str(REF_REPS) + '\n' + "Total Sets: " + str(REF_SETS) + "\n" + "Total Runtime: " +  str(datetime.now() - now) + "\n" + "\n")
            squat_log.close()
            
        return [reps, status, sets, feedback, timer]
    
    def pushup(self, reps, status, sets, feedback, timer):
        global left_arm_angle, right_arm_angle, avg_arm_angle,\
                left_spine_angle, right_spine_angle, avg_spine_angle,\
                shoulder_length, wrist_length, wrist_shoulder_ratio,\
                prev, pushup_log
        
        pushup_log = open('log/pushup_log/PushUpLog_' + str(now.strftime('%Y%m%d %H%M%S')) + '.txt', 'a') # a: 이어쓰기
        
        # reference angles
        REF_ARM_ANGLE = 80.0
        MORE_ARM_ANGLE = 110.0
        REF_SPINE_ANGLE = 140.0
        REF_WRIST_SHOULDER_RATIO = 1.8
        
        # conditions
        AFTER_SET_CONDITION = (reps == REF_REPS and status == 'Up')     # 한 세트 이후 조건
        AFTER_ALL_SET_CONDITION = (sets == REF_SETS)                    # 전체 세트 이후 조건
        DEFAULT_CONDITION = (status != 'Rest') # default
        MOREDOWN_CONDITION = (status != 'Rest' and feedback == 'Start') # 더 구부려야 하는 경우
        COUNT_CONDITION = (status != 'Rest' and feedback == 'Bend your arms more')  # 적절한 경우
        AFTER_REST_CONDITION = (timer == 1 and feedback == 'Take a breathe..') ## 쉬는시간이 끝난 경우(timer가 0이 되는 순간 feedback 출력값이 변경되므로 1로 설정)
        
        # angles in conditions -> '만족하는' 각도
        SPINE_ANGLE = (avg_spine_angle > REF_SPINE_ANGLE)
        WRIST_RATIO = (wrist_shoulder_ratio < REF_WRIST_SHOULDER_RATIO)
        DEFAULT_ANGLE = (avg_arm_angle > MORE_ARM_ANGLE)
        MOREDOWN_ANGLE = (REF_ARM_ANGLE < avg_arm_angle < MORE_ARM_ANGLE)
        COUNT_ANGLE = (avg_arm_angle < REF_ARM_ANGLE)
        
        # get angles
        try:
            left_arm_angle = self.angle_list0[0]
            left_spine_angle = self.angle_list0[1]
            right_arm_angle = self.angle_list1[0]
            right_spine_angle = self.angle_list1[1]
            wrist_length = self.angle_list1[2]
            shoulder_length = self.angle_list1[3]
        except:
            pass
        
        # get average    
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2
        avg_spine_angle = (left_spine_angle + right_spine_angle) // 2
        
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
                pushup_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif MOREDOWN_CONDITION and MOREDOWN_ANGLE:     # 너무 적게 구부렸을 때 (log 배제)
                voiceFeedback('moredown')
                status = 'Up'
                feedback = 'Bend your arms more'
            elif DEFAULT_CONDITION and DEFAULT_ANGLE:       #구부리지 않았을 때 (log 배제)
                status = 'Up'
                feedback = 'Start'
        else:
            if feedback == 'Success' and (not SPINE_ANGLE or not WRIST_RATIO):  # 카운트가 된 직후 잘못 자세를 잡았을 때
                reps -= 1
                status = 'Up'
                feedback = 'Keep your position to the end'
                pushup_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif DEFAULT_CONDITION and not SPINE_ANGLE:   # 허리를 구부렸을 때
                if feedback != 'Straight your spine':
                    voiceFeedback('spine')
                status = 'Up'
                feedback = 'Straight your spine'
                pushup_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif DEFAULT_CONDITION and not WRIST_RATIO:
                if feedback != 'Put your hands together':
                    voiceFeedback('hand')
                status = 'Up'
                feedback = 'Put your hands together'
                pushup_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
                
        # after each set
        if AFTER_SET_CONDITION:
            prev = time.time()
            if feedback == 'Start':
                voiceFeedback('rest_time')
            status = 'Rest'
            feedback = 'Take a breathe..'
            pushup_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
        if AFTER_REST_CONDITION: ## 쉬는시간이 종료될 경우
            voiceFeedback('start_exercise') ## 다시 운동 시작    
            feedback = 'Start exercise again' 
            pushup_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
        if status == 'Rest':
            reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # run timer function
            
        # when exercise is finished
        if AFTER_ALL_SET_CONDITION:
            voiceFeedback('end')
            reps = 0
            status = 'All done'
            sets = 0
            feedback = "Well done!"
            pushup_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            pushup_log.write("Total Reps: " + str(REF_REPS) + '\n' + "Total Sets: " + str(REF_SETS) + "\n" + "Total Runtime: " +  str(datetime.now() - now) + "\n" + "\n")
            pushup_log.close()
        
        return [reps, status, sets, feedback, timer]
            
    def sidelateralraise(self, reps, status, sets, feedback, timer):
        global left_elbow_angle, right_elbow_angle, avg_elbow_angle,\
                left_shoulder_angle, right_shoulder_angle, avg_shoulder_angle,\
                heel_length, foot_length, shoulder_length,\
                heel_foot_ratio, heel_shoulder_ratio,\
                prev, sidelateralraise_log
        
        sidelateralraise_log = open('log/sidelateralraise_log/SideLateralRaiseLog_' + str(now.strftime('%Y%m%d %H%M%S')) + '.txt', 'a') # a: 이어쓰기
        
        # reference angles: 1차 수정 완료
        LESS_SHOULDER_ANGLE = 35.0 # 더 올리고
        REF_SHOULDER_ANGLE = 60.0  # 적당하고
        MORE_SHOULDER_ANGLE = 75.0 # 너무많이 올렸고
        REF_ELBOW_ANGLE = 140.0 ## 팔꿈치
        LESS_HEEL_FOOT_RATIO = 0.6 ## 발 11자 조건
        MORE_HEEL_FOOT_RATIO = 1.2
        LESS_SHOULDER_RATIO = 0.4 # 두 발 어깨 넓이     
        MORE_SHOULDER_RATIO = 1.1
        
        # conditions
        AFTER_SET_CONDITION = (reps == REF_REPS and status == 'Down')     # 한 세트 이후 조건
        AFTER_ALL_SET_CONDITION = (sets == REF_SETS)                        # 전체 세트 이후 조건
        MORE_RAISE_CONDITION = (status != 'Rest' and feedback == 'Success')   # 팔을 더 들어야하는 경우
        LESS_RAISE_CONDITION = (status != 'Rest' and feedback == 'Start')   # 팔을 조금 내려야하는 경우
        PARALLEL_CONDITION = (status != 'Rest') # 발 11자를 못했을 경우
        COUNT_CONDITION = (status != 'Rest' and feedback == 'raise your arm more')  # 적절한 경우
        AFTER_REST_CONDITION = (timer == 1 and feedback == 'Take a breathe..') ## 쉬는시간이 끝난 경우(timer가 0이 되는 순간 feedback 출력값이 변경되므로 1로 설정)
        DEFAULT_CONDITION = (status != 'Rest')  # 운동 중인데 아무것도 아닌 경우      
        
        # angles in conditions -> '만족하는' 각도
        ELBOW_ANGLE = (REF_ELBOW_ANGLE < avg_elbow_angle) ## 정확한 팔꿈치 각도
        LESS_BEND_ANGLE = (avg_elbow_angle < REF_ELBOW_ANGLE)  ## 너무 적게 폈을 때
        SHOULDER_ANGLE = (REF_SHOULDER_ANGLE < avg_shoulder_angle < MORE_SHOULDER_ANGLE)   ## 정확한 어깨 각도
        MORE_RAISE_ANGLE = (avg_shoulder_angle > MORE_SHOULDER_ANGLE)   ## 너무 많이 벌렸을 때
        LESS_RAISE_ANGLE = (LESS_SHOULDER_ANGLE < avg_shoulder_angle < REF_SHOULDER_ANGLE) ## 너무 많이 벌렸음 
        DEFAULT_ANGLE = (avg_shoulder_angle < LESS_SHOULDER_ANGLE) ## 기본자세
        PARALLEL_RATIO = (LESS_HEEL_FOOT_RATIO < heel_foot_ratio < MORE_HEEL_FOOT_RATIO)
        HEEL_RATIO = (LESS_SHOULDER_RATIO < heel_shoulder_ratio < MORE_SHOULDER_RATIO)
        
        # get angles
        try:
            left_shoulder_angle = self.angle_list0[0]
            left_elbow_angle = self.angle_list0[1]
            right_shoulder_angle = self.angle_list1[0]
            right_elbow_angle = self.angle_list1[1]
            heel_length = self.angle_list1[2]
            foot_length = self.angle_list1[3]
            shoulder_length = self.angle_list1[4]
        except:
            pass
        
        # get average    
        avg_shoulder_angle = (left_shoulder_angle + right_shoulder_angle) // 2  
        avg_elbow_angle = (left_elbow_angle + right_elbow_angle) // 2
        
        # get ratio
        foot_length = round(foot_length, 4)
        if foot_length != 0:
            heel_foot_ratio = heel_length / foot_length    
        shoulder_length = round(shoulder_length, 4)
        if right_leg_angle > 160:
            heel_shoulder_ratio = heel_length / shoulder_length
        
        # count logic
        if ELBOW_ANGLE and PARALLEL_RATIO and HEEL_RATIO:         # 기본 자세가 만족되고(팔꿈치가 적절히 구부려짐)
            if MORE_RAISE_CONDITION and MORE_RAISE_ANGLE:  ## 너무 많이 올렸을 때
                voiceFeedback('lessraise')
                reps -= 1
                status = 'Down'
                feedback = 'raise your arm less'
                sidelateralraise_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif COUNT_CONDITION and SHOULDER_ANGLE: # 적절하게 올렸을 때
                voiceFeedback('buzzer')
                reps += 1
                status = 'Up'
                feedback = 'Success'
                sidelateralraise_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif LESS_RAISE_CONDITION and LESS_RAISE_ANGLE:  ## 너무 적게 올렸을 때 (log 배제)
                voiceFeedback('moreraise')
                status = 'Down'
                feedback = 'raise your arm more'    
            elif DEFAULT_CONDITION and DEFAULT_ANGLE:  ## 디폴트 상태 (log 배제)
                status = 'Down'
                feedback = 'Start'  
        else:
            if feedback == 'Success' and (not ELBOW_ANGLE or not PARALLEL_RATIO or not HEEL_RATIO):  # 카운트가 된 직후 잘못 자세를 잡았을 때
                reps -= 1
                status = 'Down'
                feedback = 'Keep your position to the end'
                sidelateralraise_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif DEFAULT_CONDITION and LESS_BEND_ANGLE:   ## 팔꿈치를 더 구부려야함
                if feedback != 'bend your elbow less':
                    voiceFeedback('lessbend')
                status = 'Down'
                feedback = 'bend your elbow less' 
                sidelateralraise_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif PARALLEL_CONDITION and not PARALLEL_RATIO: # 발이 11자가 아닐 때
                if feedback != 'Parallel your feet':
                    voiceFeedback('parallel')
                status = 'Down'
                feedback = 'Parallel your feet'    
                sidelateralraise_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            elif DEFAULT_CONDITION and not HEEL_RATIO: # 발이 어깨넓이가 아닐 때
                if feedback != 'Spread your feet shoulder width':
                    voiceFeedback('shoulder_length')
                status = 'Up'
                feedback = 'Spread your feet shoulder width'
                sidelateralraise_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
                
        # after each set
        if AFTER_SET_CONDITION:
            prev = time.time()
            if feedback == 'Start':
                voiceFeedback('rest_time')
            status = 'Rest'
            feedback = 'Take a breathe..'
            sidelateralraise_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
        if AFTER_REST_CONDITION: ## 쉬는시간이 종료될 경우
            voiceFeedback('start_exercise') ## 다시 운동 시작    
            feedback = 'Start exercise again' 
            sidelateralraise_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
        if status == 'Rest':
            reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # run timer function
            
        # when exercise is finished
        if AFTER_ALL_SET_CONDITION:
            voiceFeedback('end')
            reps = 0
            status = 'All done'
            sets = 0
            feedback = "Well done!"
            sidelateralraise_log.write(str(datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + str(feedback) + "\n")
            sidelateralraise_log.write("Total Reps: " + str(REF_REPS) + '\n' + "Total Sets: " + str(REF_SETS) + "\n" + "Total Runtime: " +  str(datetime.now() - now) + "\n" + "\n")
            sidelateralraise_log.close()
                
        return [reps, status, sets, feedback, timer]
    
    def calculate_exercise(self):
        if self.state_info.mode == "squat":
            self.state_info.reps, self.state_info.status, self.state_info.sets, self.state_info.feedback, self.state_info.timer = self.squat(self.state_info.reps, self.state_info.status, self.state_info.sets, self.state_info.feedback, self.state_info.timer)
        elif self.state_info.mode == "pushup":
            self.state_info.reps, self.state_info.status, self.state_info.sets, self.state_info.feedback, self.state_info.timer = self.pushup(self.state_info.reps, self.state_info.status, self.state_info.sets, self.state_info.feedback, self.state_info.timer)
        elif self.state_info.mode == "sidelateralraise":
            self.state_info.reps, self.state_info.status, self.state_info.sets, self.state_info.feedback, self.state_info.timer = self.sidelateralraise(self.state_info.reps, self.state_info.status, self.state_info.sets, self.state_info.feedback, self.state_info.timer)
        else:
            pass
        
        return self.state_info

class EXERCISE(KEYPOINT):
    def __init__(self, landmarks):
        super().__init__(landmarks)
    
    def squat(self, camID):
        #get angles from each camID
        if camID == LEFT_CAM:
            left_leg_angle = self.angle_of_the_left_leg()
            left_knee_angle = self.angle_of_the_left_knee()
            left_elbow_angle = self.angle_of_the_left_elbow() ## 이스터
            left_shoulder_angle = self.angle_of_the_left_shoulder()
            
            angle_list = [left_leg_angle, left_knee_angle, left_elbow_angle, left_shoulder_angle]
        elif camID == RIGHT_CAM:
            right_leg_angle = self.angle_of_the_right_leg()
            right_knee_angle = self.angle_of_the_right_knee()
            heel_length = self.length_of_heel_to_heel()
            foot_length = self.length_of_foot_to_foot()
            shoulder_length = self.length_of_shoulder_to_shoulder()
            right_elbow_angle = self.angle_of_the_right_elbow() ## 이스터
            right_shoulder_angle = self.angle_of_the_right_shoulder()
            # right_hand_angle = self.angle_of_the_right_hand()
            
            angle_list = [right_leg_angle, right_knee_angle, heel_length, foot_length, shoulder_length, right_elbow_angle, right_shoulder_angle]#, right_hand_angle]
            
        return angle_list
        
    def pushup(self, camID):
        #get angles from each camID
        if camID == LEFT_CAM:
            left_arm_angle = self.angle_of_the_left_arm()
            left_spine_angle = self.angle_of_the_left_spine()
            
            angle_list = [left_arm_angle, left_spine_angle]
        elif camID == RIGHT_CAM:
            right_arm_angle = self.angle_of_the_right_arm()
            right_spine_angle = self.angle_of_the_right_spine()
            wrist_length = self.length_of_wrist_to_wrist()
            shoulder_length = self.length_of_shoulder_to_shoulder()
            
            angle_list = [right_arm_angle, right_spine_angle, wrist_length, shoulder_length]
            
        return angle_list

    def sidelateralraise(self, camID):
        #get angles from each camID
        if camID == LEFT_CAM:
            left_shoulder_angle = self.angle_of_the_left_shoulder()
            left_elbow_angle = self.angle_of_the_left_elbow()
            
            angle_list = [left_shoulder_angle, left_elbow_angle]
        elif camID == RIGHT_CAM:
            right_shoulder_angle = self.angle_of_the_right_shoulder()
            right_elbow_angle = self.angle_of_the_right_elbow() 
            heel_length = self.length_of_heel_to_heel()
            foot_length = self.length_of_foot_to_foot()
            shoulder_length = self.length_of_shoulder_to_shoulder()
            
            angle_list = [right_shoulder_angle, right_elbow_angle, heel_length, foot_length, shoulder_length]
            
        return angle_list
    
    # select mode
    def select_mode(self, mode, camID): 
        if mode == "squat":
            angle_list = EXERCISE(self.landmarks).squat(camID)
        elif mode == "pushup":
            angle_list = EXERCISE(self.landmarks).pushup(camID)
        elif mode == "sidelateralraise":
            angle_list = EXERCISE(self.landmarks).sidelateralraise(camID)
        else:
            angle_list = []
            pass
        
        return angle_list