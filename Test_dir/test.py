import numpy as np



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