import numpy as np              # 스켈레톤 탐지 후 각도/거리 계산
import time                     # 타이머 사용
from keypoint import KEYPOINT   # keypoint 불러오기
from utils import *             # utils 불러오기
from datetime import datetime

'''detect -> self로 다시 수정 : python class 선언에서 관례적으로 쓰는거라 변경 안하는게 맞을 듯'''

cur = 0.0
prev = 0.0
timeElapsed = 0.0   # 전역 변수로 사용

class EXERCISE(KEYPOINT):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    # 푸쉬업
    def pushup(self, reps, status, sets, feedback, count):
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_left_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 ## 팔꿈치 각도

        if status:
            if avg_arm_angle < 70: ## 구부릴때
                reps += 1 ## 카운트
                status = False
        else:
            if avg_arm_angle > 160: ## 안구부릴때
                status = True

        return [reps, status, sets, feedback, count]
    
    # 휴식 타이머
    def Rest_timer(self, reps, status, sets, feedback, count):
        global cur, prev, timeElapsed   # 함수 내에서 전역 변수를 사용하기 위해서는 global 선언 필요
        cur = time.time()               # 현재 시간을 받아옴
        
        timeElapsed = cur - prev        # 시간 차를 계산 -> 1초를 계산하기 위해 사용
        # print("prev : {:.3f}\tcur : {:.3f}\ttimeElapsed : {:.3f}".format(prev, cur, timeElapsed))
        # test 해보고 싶으면 위에 print 찍어볼 것
        
        if timeElapsed >= 1:        # 1초가 지났으면
            count -= 1              # 1초를 table에 표시하기 위해 count -= 1
            timeElapsed = 0         # 시간차 초기화
            prev += 1               # 이전 시간에 1초를 더함 -> 42line의 조건을 반복적으로 쓰기 위해
            if count <= 0:          # 타이머가 끝나면
                # print("timer over")
                count = 5           # 타이머 초기화
                reps = 0            # reps 초기화
                sets += 1           # sets 입력
        
        return [reps, status, sets, feedback, count]
                            
    # 스쿼트
    def squat(self, reps, status, sets, feedback, count): ## 스쿼트
        left_leg_angle = self.angle_of_the_right_leg() ## 무릎각도
        right_leg_angle = self.angle_of_the_left_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2

        '이 부분 로직 완전히 바꿈 내 생각의 한계는 여기까지였음. 기존 로직이 더 깔끔한데 타이머를 못넣게덨더라고'
        
        global prev     # 전역 변수 사용 위해
        
        if sets < 3:                                
            if reps < 5:
                if status == 'Up':
                    if avg_leg_angle < 90:      # 무릎 충분히 굽혔을 때
                        reps += 1
                        # print("sets : {}\treps : {}\tcount : {}\tstatus : {}".format(sets, reps, count, status))
                        prev = time.time()      # 현재 시간 저장 -> reps == 5가 되는 순간 더 이상 갱신이 안되기 때문에 세트가 끝난 시간이라고 볼 수 있음          
                        status = 'Down'
                        feedback = 'Success'
                else:
                    if avg_leg_angle > 160:     # 무릎 충분히 폈을 때
                        status = 'Up'
                        feedback = 'Ready'
            else:
                if reps == 5:                   # reps가 끝나게 되면
                    # print('run timer')
                    reps, status, sets, feedback, count = self.Rest_timer(reps, status, sets, feedback, count)  # 타이머 함수 호출
        else:
            if sets == 3:                       # sets가 끝나게 되면
                # print('운동 끝')                # 아직 별다른 조치 안함
                feedback = 'well done!'
                pass
        return [reps, status, sets, feedback,count]

    def calculate_exercise(self, exercise_type, reps, status, sets, feedback, count): ## 운동횟수 계산
        if exercise_type == "pushup":
            reps, status, sets, feedback, count = EXERCISE(self.landmarks).pushup(
                reps, status, sets, feedback, count)
        elif exercise_type == "squat":
            reps, status, sets, feedback, count = EXERCISE(self.landmarks).squat(
                reps, status, sets, feedback, count)
        
        return [reps, status, sets, feedback, count]
    