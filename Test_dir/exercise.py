import numpy as np              # 스켈레톤 탐지 후 각도/거리 계산
import time
from turtle import right                     # 타이머 사용
from keypoint import KEYPOINT   # keypoint 불러오기
from utils import *             # utils 불러오기
from ast import Break
import pygame
import os
# 전역 변수로 사용(타이머 구현)
cur = 0.0
prev = 0.0
timeElapsed = 0.0

left_leg_angle = []      ## 스쿼트 무릎 각도
right_leg_angle = []
avg_leg_angle = []

left_knee_angle = []     ## 스쿼트 무릎/발끝 각도
right_knee_angle = []
avg_knee_angle = []

left_arm_angle = 180.0      ## 푸쉬업 팔꿈치 각도
right_arm_angle = 180.0
avg_arm_angle = 0.0

left_spine_angle = 180.0    ## 푸쉬업 척추 각도
right_spine_angle = 180.0
avg_spine_angle = 0.0

# pygame.init() ## mixer 초기화
# os.getcwd()
# rest = pygame.mixer.Sound('rest_time.mp3')
# buzzer = pygame.mixer.Sound('buzzer.mp3')
# end = pygame.mixer.Sound('end.mp3')

class EXERCISE(KEYPOINT):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    # 휴식 타이머
    def Rest_timer(self, reps, status, sets, feedback, timer):
        print("timer start..!\r\n")
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
        
        return [reps, status, sets, feedback, timer]
                            
    # 스쿼트
    def squat(self, reps, status, sets, feedback, timer): ## 스쿼트
        left_leg_angle = self.angle_of_the_right_leg() ## 무릎각도
        right_leg_angle = self.angle_of_the_left_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2 ## 무릎 평균 각도(//2는 평균 + 정수값)
        
        left_knee_angle = self.angle_of_the_left_knee()
        right_knee_angle = self.angle_of_the_right_knee()
        avg_knee_angle = (left_knee_angle + right_knee_angle)//2  
        
        global prev     # 전역 변수 사용 위해
        
        if sets < 3:    # 테스트용으로 set = 3 // 추후 5로 변경                            
            if reps < 5: # 5 rerps = 1 sets // 추후 15로 변경
                if status == 'Up': ## count 조건
                    if avg_knee_angle > 150: ## 무릎이 발끝보다 뒤쪽일 때
                        status = 'Up' ## 운동 상태
                        feedback = 'knees are in the right' ## 올바른 자세라는 feedback
                        print("knee : ", avg_knee_angle)
                        ##Break
                        if avg_leg_angle < 90:      # 무릎 충분히 굽혔을 때
                            print("leg : ", avg_leg_angle)
                            reps += 1               # 운동 동작 timer
                            status = 'Down'         # 운동 상태
                            prev = time.time()      # 현재 시간 저장 -> reps == 5가 되는 순간 더 이상 갱신이 안되기 때문에 세트가 끝난 시간이라고 볼 수 있음                                      
                            feedback = 'Success'    # 피드백
                            ##Break
                else:                    
                    if avg_leg_angle > 100:     # 무릎 충분히 폈을 때
                        print("leg : ", avg_leg_angle)
                        status = 'Up'           # 운동 상태
                        feedback = 'Ready'      # 피드백
                        Break ## if문 빠져나감
                    if avg_knee_angle < 150: ## 무릎이 발끝보다 앞쪽일 때
                        print("knee : ", avg_knee_angle)
                        status = 'Up'
                        feedback = 'Place your knees behind toes' ## feedback 내용
                        Break ## if문 빠져나감
            else:
                if reps == 5:                   # reps가 끝나게 되면
                    # print('run timer')
                    reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # 타이머 함수 호출
        else:
            if sets == 3:                       # sets가 끝나게 되면
                # print('운동 끝')              # 아직 별다른 조치 안함
                feedback = 'Well done!'         # 운동 끝
                pass
        return [reps, status, sets, feedback, timer]

    # 푸쉬업
    def pushup(self, reps, status, sets, feedback, timer, camID):
        
        global prev, left_arm_angle, right_arm_angle, avg_arm_angle, left_spine_angle, right_spine_angle, avg_spine_angle
        
        # REF_ARM_ANGLE = 90.0
        # REF_SPINE_ANGLE = 170.0
        
        # camID 구분 -> 좌측, 우측 각각 따로 계산
        if camID == 1:
            left_spine_angle = self.angle_of_the_left_spine()
            left_arm_angle = self.angle_of_the_left_arm()
        elif camID == 0:
            right_spine_angle = self.angle_of_the_right_spine()
            right_arm_angle = self.angle_of_the_right_arm()

        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 ## 팔꿈치 평균 각도(//2는 평균 + 정수값)
        avg_spine_angle = (left_spine_angle + right_spine_angle) // 2 ## 척추 평균 각도
        print("l_arm : ", left_arm_angle, "r_arm : ", right_arm_angle, "avg arm : ", avg_arm_angle)
        print("l_spine : ", left_spine_angle, "r_spine : ", right_spine_angle, "avg spine : ", avg_spine_angle)
        
        '''# count logic
        if avg_arm_angle < REF_ARM_ANGLE and avg_spine_angle > REF_SPINE_ANGLE:     # 팔꿈치를 충분히 굽히고 허리가 일자일 때
            print("make")
            reps += 1
            status = 'Down'
            feedback = 'Success'
            prev = time.time()
        else:
            if avg_arm_angle > REF_ARM_ANGLE:     # 팔을 충분히 굽히지 않은 경우
                status = 'Up'
                feedback = 'Bend your elbows'
                print("line 141", feedback)
            elif avg_spine_angle < REF_SPINE_ANGLE: # 척추가 일자가 아닐 경우
                status = 'Up'
                feedback = 'Straight your spine'
                print("line 146", feedback)
                
        # after 1 set
        if reps == REF_REPS and camID == 0:
            # if pygame.mixer.get_busy() == False:
            #     if timer == 5:
            #         rest.play()
            reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # 타이머 함수 호출
        
        # when exercise is finished
        if sets == REF_SETS:
            reps = 0
            status = 'Up'
            sets = 0
            feedback = "Well done!"'''
        
        if sets < 3: ## 임시로 sets 3설정, 추후 5로 변경                             
            if reps < 5: ## 임시로 reps 5설정, 추후 15로 변경
                if status == 'Up': ## count하기 위한 조건
                    if avg_spine_angle > 170: ## 척추 1자일 때
                        print("spine: ", avg_spine_angle)
                        status = 'Up' ## 운동 상태
                        feedback = 'Spine is Straight' ## 올바른 자세라는 피드백
                        ##Break
                        if avg_arm_angle < 90:      # 팔꿈치 충분히 굽혔을 때
                            print("\r\nline 126 arms down {}\r\n".format(avg_arm_angle))
                            reps += 1               # 운동 동작 카운트
                            status = 'Down'         # 운동 상태                      
                            prev = time.time()      # 현재 시간 저장 -> reps == 5가 되는 순간 더 이상 갱신이 안되기 때문에 세트가 끝난 시간이라고 볼 수 있음          
                            feedback = 'Success'    # 피드백
                            ##Break
                else: ## count 하지 않을 조건
                    if avg_arm_angle > 160:     # 팔꿈치 충분히 폈을 때
                        print("\r\nline 134 arms up {}\r\n".format(avg_arm_angle))
                        print("arm : ", avg_arm_angle)
                        status = 'Up'           ## 운동 상태 변경 
                        feedback = 'Ready'      # 피드백
                         ## if문 종료                                       
                    if avg_spine_angle < 160: ## 척추 구부러졌을 때 
                        print("spine: ", avg_spine_angle)
                        status = 'Up' ## 운동상태 변경 
                        feedback = 'Straight your spine' ## 피드백
                        Break ## if문 종료
            else:
                if reps == 5:                   # reps가 끝나게 되면
                    print('run timer')
                    reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # 타이머 함수 호출
        else:
            if sets == 3:                       # sets가 끝나게 되면
                # print('운동 끝')                # 아직 별다른 조치 안함
                feedback = 'well done!'         # 피드백
                pass
        
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
    