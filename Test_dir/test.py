import numpy as np
import time
import pygame

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

'''if 무릎이 발끝보다 뒤에 있고 and 발이 11자일 때:
    if 각도 < 기준1:  --> 너무 내려감
    elif 기준1 < 각도 < 기준2: --> 횟수 인정
    elif 기준2 < 각도 < 기준3: --> 더 구부려야 함
    else: --> 아직 안구부림
elif 무릎이 발끝보다 앞에 있을 때:
elif 발이 11자가 아닐 때:'''


# less < 50 < good < 120 < more < 155   170 < default

pygame.init()

prev_sound =""

def voiceFeedback(sound): 
    global prev_sound
    pygame.mixer.Sound('rest_time.wav')
    pygame.mixer.Sound('buzzer.wav')
    pygame.mixer.Sound('end.wav')
    pygame.mixer.Sound('correct.wav')
    pygame.mixer.Sound('kneedown.wav')
    pygame.mixer.Sound('lessdown.wav')
    pygame.mixer.Sound('end.wav')
    pygame.mixer.Sound('parallel.wav')
    print("cur", sound)
    if pygame.mixer.get_busy() == False:
        prev_sound = sound
        print("prev", prev_sound)
        pygame.mixer.Sound(sound + '.wav').play()
    else:
        if prev_sound != sound:
            print("like interrupt")
            pygame.mixer.stop()
            pygame.mixer.Sound(sound + '.wav').play()
        else:
            print("same sound")
            

voiceFeedback('rest_time')
time.sleep(3)
print(1)
voiceFeedback('rest_time')
print(2)
time.sleep(1)
voiceFeedback('rest_time')
print(3)
time.sleep(3)
voiceFeedback('rest_time')
print(1)
time.sleep(0.5)
voiceFeedback('end')
time.sleep(3)


######################

'''#landmark data 저장(마지막 프레임 데이터만)
                if camID == 0:                  
                    data = detections(landmarks=landmarks)
                    data.to_csv("./data.csv")'''

##########################

'''if sets < 3:    # 테스트용으로 set = 3 // 추후 5로 변경                            
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
        pass'''

##################################    
    
'''if sets < 3: ## 임시로 sets 3설정, 추후 5로 변경                             
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
                pass'''    

########################
        
'''import time

avg_spine_angle = 0
avg_arm_angle = 0
reps = 0
sets = 0
status = 'Up'
feedback = 'Ready'
REF_REPS = 5
REF_SETS = 3
REF_TIMER = 5
REF_ARM_ANGLE = 90
REF_SPINE_ANGLE = 170

if avg_arm_angle < REF_ARM_ANGLE and avg_spine_angle > REF_SPINE_ANGLE:     # 팔꿈치를 충분히 굽히고 허리가 일자일 때
    reps += 1
    status = 'Down'
    feedback = 'Success'
    prev = time.time()
else:
    if avg_arm_angle > REF_ARM_ANGLE:     # 팔을 충분히 굽히지 않은 경우
        status = 'Up'
        feedback = 'Bend your elbows'
    elif avg_spine_angle < REF_SPINE_ANGLE: # 척추가 일자가 아닐 경우
        status = 'Up'
        feedback = 'Straight your spine'
        
if reps == REF_REPS:
    reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # 타이머 함수 호출
    
if sets == REF_SETS:
    reps = 0
    status = 'Up'
    sets = 0
    feedback = 'Well done!'
    '''