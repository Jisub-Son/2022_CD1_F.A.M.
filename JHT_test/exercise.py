import numpy as np              # 스켈레톤 탐지 후 각도/거리 계산
import time                     # 타이머 사용
from keypoint import KEYPOINT   # keypoint 불러오기
from utils import *             # utils 불러오기

import pygame    #pip install pygame  cmd에 쳐야됨

# 전역 변수로 사용(타이머 구현)
cur = 0.0
prev = 0.0
timeElapsed = 0.0  

pushup_end = 1


class EXERCISE(KEYPOINT):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    # 휴식 타이머
    def Rest_timer(self, reps, status, sets, feedback, timer):
        global cur, prev, timeElapsed   # 함수 내에서 전역 변수를 사용하기 위해서는 global 선언 필요
        cur = time.time()               # 현재 시간을 받아옴
        
        timeElapsed = cur - prev        # 시간 차를 계산 -> 1초를 계산하기 위해 사용
        
        if timeElapsed >= 1:        # 1초가 지났으면
            timer -= 1              # 1초를 table에 표시하기 위해 timer -= 1
            timeElapsed = 0         # 시간차 초기화
            prev += 1               # 이전 시간에 1초를 더함 -> 42line의 조건을 반복적으로 쓰기 위해
            if timer <= 0:          # 타이머가 끝나면
                # print("timer over")
                timer = 5           # 타이머 초기화(임시로 5초 설정)
                reps = 0            # reps 초기화
                sets += 1           # sets 입력
        
        return [reps, status, sets, feedback, timer]
                            
    # 스쿼트
    def squat(self, reps, status, sets, feedback, timer): ## 스쿼트
        left_leg_angle = self.angle_of_the_right_leg() ## 무릎각도
        right_leg_angle = self.angle_of_the_left_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2 ## 무릎 평균 각도(//2는 평균 + 정수값)



        
        global prev     # 전역 변수 사용 위해
        
        if sets < 3:    # 테스트용으로 set = 3 // 추후 5로 변경                            
            if reps < 5: # 5 rerps = 1 sets
                if status == 'Up':

                   
                        if avg_leg_angle < 90:      # 무릎 충분히 굽혔을 때
                            reps += 1               # 운동 동작 timer
                            prev = time.time()      # 현재 시간 저장 -> reps == 5가 되는 순간 더 이상 갱신이 안되기 때문에 세트가 끝난 시간이라고 볼 수 있음          
                            status = 'Down'         # 운동 상태  
                            feedback = 'Success'    # 피드백






                else:
                    if avg_leg_angle > 160:     # 무릎 충분히 폈을 때
                        status = 'Up'           # 운동 상태
                        feedback = 'Ready'      # 피드백
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
    def pushup(self, reps, status, sets, feedback, timer):
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_left_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 ## 팔꿈치 평균 각도(//2는 평균 + 정수값)

        avg_spine_angle = self.angle_of_the_abdomen()

        elbow_angle= self.angle_of_the_elbow()




        global prev     # 전역 변수 사용 위해
        
        if sets < 3:                                
            if reps < 5:
                if status == 'Up':

                    if avg_spine_angle > 160:


                        if (avg_arm_angle < 90) and (elbow_angle < 120) :      # 무릎 충분히 굽혔을 때
                            reps += 1               # 운동 동작 카운트                      
                            prev = time.time()      # 현재 시간 저장 -> reps == 5가 되는 순간 더 이상 갱신이 안되기 때문에 세트가 끝난 시간이라고 볼 수 있음          
                            status = 'Down'         # 운동 상태
                            feedback = 'Success'    # 피드백



                    if (elbow_angle > 120) and (avg_spine_angle < 160) :
                        feedback = 'straighten your back and Bring your elbows together a little more'

                        
                        pygame.mixer.init() #소리를 재생할때마다 꼭 초기화 해야됨
                        
                        if pygame.mixer.music.get_busy() == False : #소리가 겹쳐서 재생되지 않도록 재생상태가 아닐때만 재생
                            pygame.mixer.music.load('spineelbow.mp3')
                            pygame.mixer.music.play()
                       
    


                    elif (avg_spine_angle < 160):
                        feedback = 'straighten your back'

                        pygame.mixer.init() #소리를 재생할때마다 꼭 초기화 해야됨
                        
                        if pygame.mixer.music.get_busy() == False :
                            pygame.mixer.music.load('spine.mp3')
                            pygame.mixer.music.play()
                       
                       
                   

                    elif elbow_angle > 120:
                        feedback = 'Bring your elbows together a little more'

                        pygame.mixer.init() #소리를 재생할때마다 꼭 초기화 해야됨
                        
                        if pygame.mixer.music.get_busy() == False :
                            pygame.mixer.music.load('elbow.mp3')
                            pygame.mixer.music.play()
                            




                else:
                    
                    if avg_spine_angle > 160:


                        if( avg_arm_angle > 160)and (elbow_angle < 120) :     # 무릎 충분히 폈을 때
                            status = 'Up'           # 운동 상태 
                            feedback = 'Ready'      # 피드백 


                            
                    if (elbow_angle > 120) and (avg_spine_angle < 160) :
                        feedback = 'straighten your back and Bring your elbows together a little more'

                        pygame.mixer.init() #소리를 재생할때마다 꼭 초기화 해야됨
                        
                        if pygame.mixer.music.get_busy() == False :
                            pygame.mixer.music.load('spineelbow.mp3')
                            pygame.mixer.music.play()


                    elif (avg_spine_angle < 160):
                        feedback = 'straighten your back'
                       
                        pygame.mixer.init() #소리를 재생할때마다 꼭 초기화 해야됨
                        
                        if pygame.mixer.music.get_busy() == False :
                            pygame.mixer.music.load('spine.mp3')
                            pygame.mixer.music.play()
                    
                           

                    elif elbow_angle > 120:
                        feedback = 'Bring your elbows together a little more'
                
                        
                        pygame.mixer.init() #소리를 재생할때마다 꼭 초기화 해야됨
                        
                        if pygame.mixer.music.get_busy() == False :
                            pygame.mixer.music.load('elbow.mp3')
                            pygame.mixer.music.play()
                            
                            

                        
            else:
                if reps == 5:                   # reps가 끝나게 되면
                    # print('run timer')
                    reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # 타이머 함수 호출

                    pygame.mixer.init() #소리를 재생할때마다 꼭 초기화 해야됨
                        
                    if pygame.mixer.music.get_busy() == False :
                        pygame.mixer.music.load('buzer.mp3')
                        pygame.mixer.music.play()
           
                            
        else:
            if sets == 3:                       # sets가 끝나게 되면
                # print('운동 끝')                # 아직 별다른 조치 안함
                feedback = 'well done!'         # 피드백

                pygame.mixer.init() #소리를 재생할때마다 꼭 초기화 해야됨
                global pushup_end #1번만 재생 하기위한 플래그
                        
                if (pygame.mixer.music.get_busy() == False) and pushup_end == 1 :
                    pygame.mixer.music.load('pushupend.mp3')
                    pygame.mixer.music.play()
                    pushup_end = 0

       

                pass
        return [reps, status, sets, feedback,timer]
    
    # 운동횟수 계산
    def calculate_exercise(self, exercise, reps, status, sets, feedback, timer): 
        if exercise == "pushup":
            reps, status, sets, feedback, timer = EXERCISE(self.landmarks).pushup(
                reps, status, sets, feedback, timer)
        elif exercise == "squat":
            reps, status, sets, feedback, timer = EXERCISE(self.landmarks).squat(
                reps, status, sets, feedback, timer)
        
        return [reps, status, sets, feedback, timer]
    
