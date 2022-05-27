import time
from keypoint import KEYPOINT   # keypoint 불러오기
from utils import *             # utils 불러오기
from ast import Break

# 전역 변수로 사용(타이머 구현)
cur = 0.0
prev = 0.0
timeElapsed = 0.0

left_leg_angle = 180.0 ## 푸쉬업 팔꿈치 각도
right_leg_angle = 180.0
avg_leg_angle = 0.0

left_knee_angle = 180.0 ## 푸쉬업 척추 각도 
right_knee_angle = 180.0
avg_knee_angle = 0.0

left_arm_angle = 180.0      ## 푸쉬업 팔꿈치 각도
right_arm_angle = 180.0
avg_arm_angle = 0.0

left_spine_angle = 180.0
right_spine_angle = 180.0
avg_spine_angle = 0.0

class EXERCISE(KEYPOINT):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    # 휴식 타이머
    def Rest_timer(self, reps, status, sets, feedback, timer):
        print("run timer")
        global cur, prev, timeElapsed   # 함수 내에서 전역 변수를 사용하기 위해서는 global 선언 필요
        cur = time.time()               # 현재 시간을 받아옴
        
        timeElapsed = cur - prev        # 시간 차를 계산 -> 1초를 계산하기 위해 사용
        
        if timeElapsed >= 1:            # 1초가 지났으면
            timer -= 1                  # 1초를 table에 표시하기 위해 timer -= 1
            timeElapsed = 0             # 시간차 초기화
            prev += 1                   # 이전 시간에 1초를 더함 -> 42line의 조건을 반복적으로 쓰기 위해
            if timer <= 0:              # 타이머가 끝나면
                timer = REF_TIMER     # 타이머 초기화(임시로 5초 설정)
                reps = 0                # reps 초기화
                sets += 1               # sets 입력
                status = 'Up'
        
        return [reps, status, sets, feedback, timer]
                            
    # 스쿼트
    def squat(self, reps, status, sets, feedback, timer, camID): ## 스쿼트
        
        global prev, left_knee_angle, right_knee_angle, avg_knee_angle, left_leg_angle, right_leg_angle, avg_leg_angle
        
        REF_KNEE_ANGLE = 140.0
        REF_LEG_ANGLE = 90.0
        
        # camID 구분 -> 좌측, 우측 각각 따로 계산
        if camID == 1:
            left_leg_angle = self.angle_of_the_right_leg() ## 무릎각도
            left_knee_angle = self.angle_of_the_left_knee()
        elif camID == 0:
            right_leg_angle = self.angle_of_the_left_leg()
            right_knee_angle = self.angle_of_the_right_knee()
            
            
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2 ## 무릎 평균 각도(//2는 평균 + 정수값)
        avg_knee_angle = (left_knee_angle + right_knee_angle) // 2  
        
        table_angle("leg", avg_leg_angle, "knee", avg_knee_angle)
                
        # count logic
        if status == 'Up' and avg_leg_angle < REF_LEG_ANGLE and avg_knee_angle > REF_KNEE_ANGLE:     # 무릎이 발끝보다 뒤에 있고 무를을 충분히 굽혔을 때
            voiceFeedback('buzzer')
            reps += 1
            status = 'Down'
            feedback = 'Success'
            prev = time.time()
        else:
            if (status != 'Rest' and status != 'All done') and avg_leg_angle > REF_LEG_ANGLE:     # 무릎을 굽히지 않았을 때
                status = 'Up'
                feedback = 'Bend your legs'
            elif (status != 'Rest' and status != 'All done') and avg_knee_angle < REF_KNEE_ANGLE: # 척추가 일자가 아닐 경우
                status = 'Up'
                feedback = 'Place your knees behind toes'
                
        # after 1 set
        if reps == REF_REPS:
            if timer == 5 and camID == 0:
                voiceFeedback('rest_time')
            status = 'Rest'
            feedback = 'Take a breathe..'
            reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # 타이머 함수 호출
        
        # when exercise is finished
        if sets == REF_SETS:
            voiceFeedback('end')
            reps = 0
            status = 'All done'
            sets = 0
            feedback = "Well done!"
            
        return [reps, status, sets, feedback, timer, camID]

    # 푸쉬업
    def pushup(self, reps, status, sets, feedback, timer, camID):
        
        global prev, left_arm_angle, right_arm_angle, avg_arm_angle, left_spine_angle, right_spine_angle, avg_spine_angle
        
        REF_ARM_ANGLE = 90.0
        REF_SPINE_ANGLE = 170.0
        
        # camID 구분 -> 좌측, 우측 각각 따로 계산
        if camID == 1:
            left_spine_angle = self.angle_of_the_left_spine()
            left_arm_angle = self.angle_of_the_left_arm()
        elif camID == 0:
            right_spine_angle = self.angle_of_the_right_spine()
            right_arm_angle = self.angle_of_the_right_arm()

        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 ## 팔꿈치 평균 각도(//2는 평균 + 정수값)
        avg_spine_angle = (left_spine_angle + right_spine_angle) // 2 ## 척추 평균 각도
        # print("avg_arm : ", avg_arm_angle)
        # print("avg_spine : ", avg_spine_angle)
        
        table_angle("arm", avg_arm_angle, "spine", avg_spine_angle)
                
        # count logic
        if status == 'Up' and avg_arm_angle < REF_ARM_ANGLE and avg_spine_angle > REF_SPINE_ANGLE:     # 팔꿈치를 충분히 굽히고 허리가 일자일 때
            voiceFeedback('buzzer')
            reps += 1
            status = 'Down'
            feedback = 'Success'
            prev = time.time()
        else:
            if (status != 'Rest' and status != 'All done') and avg_arm_angle > REF_ARM_ANGLE:     # 팔을 충분히 굽히지 않은 경우
                status = 'Up'
                feedback = 'Bend your elbows'
            elif (status != 'Rest' and status != 'All done') and avg_spine_angle < REF_SPINE_ANGLE: # 척추가 일자가 아닐 경우
                status = 'Up'
                feedback = 'Straight your spine'
                
        # after 1 set
        if reps == REF_REPS:
            if timer == 5 and camID == 0:
                voiceFeedback('rest_time')
            status = 'Rest'
            feedback = 'Take a breathe..'
            reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # 타이머 함수 호출
        
        # when exercise is finished
        if sets == REF_SETS:
            voiceFeedback('end')
            reps = 0
            status = 'All done'
            sets = 0
            feedback = "Well done!"
        
        return [reps, status, sets, feedback, timer, camID]
  
    
    # 운동횟수 계산
    def calculate_exercise(self, exercise, reps, status, sets, feedback, timer, camID): 
        if exercise == "pushup":
            reps, status, sets, feedback, timer, camID = EXERCISE(self.landmarks).pushup(
                reps, status, sets, feedback, timer, camID)
        elif exercise == "squat":
            reps, status, sets, feedback, timer, camID = EXERCISE(self.landmarks).squat(
                reps, status, sets, feedback, timer, camID)
        
        return [reps, status, sets, feedback, timer, camID]
    