import mediapipe as mp 
import pandas as pd 
import numpy as np
import cv2 
import pygame

# set constants for reference
REF_TIMER = 5           
REF_VISIBILITY = 0.7    
REF_ROUGH_VISIBILITY = 0.0
REF_REPS = 5        
REF_SETS = 3         
RIGHT_CAM = 0
LEFT_CAM = 1 

pygame.init()               # init mixer
pygame.mixer.Sound("sound\./rest_time.wav")     # 쉬는 시간입니다
pygame.mixer.Sound("sound\./buzzer.wav")        # 버저음
pygame.mixer.Sound("sound\./end.wav")           # 운동이 종료되었습니다 
pygame.mixer.Sound("sound\./kneedown.wav")      # 무릎을 넎으세요
pygame.mixer.Sound("sound\./lessdown.wav")      # 너무 내려갔습니다
pygame.mixer.Sound("sound\./moredown.wav")      # 더 내리세요
pygame.mixer.Sound("sound\./parallel.wav")      # 발을 11자로 해주세요
pygame.mixer.Sound("sound\./spine.wav")         # 허리를 더 펴주세요
pygame.mixer.Sound("sound\./hand.wav")          # 손을 더 모아주세요
pygame.mixer.Sound("sound\./lessraise.wav")     # 팔을 조금만 벌리세요
pygame.mixer.Sound("sound\./moreraise.wav")     # 팔을 더 벌리세요
pygame.mixer.Sound("sound\./lessbend.wav")      # 팔꿈치를 조금만 구부리세요
pygame.mixer.Sound("sound\./start_exercise.wav") ## 쉬는 시간 종료
pygame.mixer.Sound("sound\./easter.wav") ## 이스터
prev_sound = ""

mp_pose = mp.solutions.pose # landmark

# calculate length function
def calculate_length(a, b):
    # get np array(coordinates)
    a = np.array(a)
    b = np.array(b)
    
    length = np.hypot(a[0] - b[0], a[1] - b[1]) # 두 점 사이 거리
    
    return length

# calculate angle function(ladian -> angle)
def calculate_angle(a, b, c):
    # get np array(coordinates)
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0]) # 라디안 계산
    angle = np.abs(radians * 180.0 / np.pi) # 라디안 -> 각도(3.14로 나누기)

    if angle > 180.0: 
        angle = 360 - angle

    return angle

# get keypoints x, y, visibility
def detection(landmarks, keypoint_name):
    return [
        landmarks[mp_pose.PoseLandmark[keypoint_name].value].x,
        landmarks[mp_pose.PoseLandmark[keypoint_name].value].y,
        landmarks[mp_pose.PoseLandmark[keypoint_name].value].visibility
    ]

# get keypoints data(사용 안함)
def detections(landmarks):
    keypoints = pd.DataFrame(columns=["keypoint", "x", "y","visibility"])

    for i, lndmrk in enumerate(mp_pose.PoseLandmark):
        lndmrk = str(lndmrk).split(".")[1]
        cord = detection(landmarks, lndmrk)
        keypoints.loc[i] = lndmrk, cord[0], cord[1], cord[2]

    return keypoints

# voice feedback function
# how to use : voiceFeedback('end') 라고 치면 end.wav 재생됨
def voiceFeedback(sound): 
    global prev_sound
    if pygame.mixer.get_busy() == False:
        prev_sound = sound
        pygame.mixer.Sound('sound\./' +  sound + '.wav').play()
    else:
        if prev_sound != sound:                             # 약간 인터럽트처럼 작동됨 end 재생       
            # print("prev", prev_sound, "cur", sound)   
            pygame.mixer.stop()                             # -> buzzer가 울리는 중에 end가 울려야 한다면 buzzer를 즉시 끄고 end 재생 
            pygame.mixer.Sound('sound\./' + sound + '.wav').play()       # -> buzzer가 울리는 중에 buzzer가 약간 겹쳐서 호출되면 새로 재생하지는 않음    
        else:
            pass

# make table
def table(exercise, reps, status, sets, feedback, timer): 
    table = cv2.imread("table\./table.PNG") # table 이미지 위치
    cv2.putText(table, "Exercise            " + exercise.replace("-", " "), ## opencv문자열: table 운동타입(입력한 운동타입)
                (1, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Reps                " + str(reps), (1, 155), ## opencv문자열: table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Status              " + str(status), (5, 210), ## opencv문자열: table 운동 상태
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Set                 " + str(sets), (5, 270), ## opencv문자열: table 세트수
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Feedback           " + str(feedback), (5, 330), ## opencv문자열: table 피드백
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Timer               " + str(timer), (5, 390), ## opencv문자열: table 타이머
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.imshow("Table", table) ## table 출력
    cv2.moveWindow("Table", 0, 510)

# make calculations table    
def table_calculations(*args, **kwargs):
    table_calculations = cv2.imread("table\./table_angle.PNG")
    for i, key in enumerate(kwargs):
        cv2.putText(table_calculations, "{} : {:.4f}".format(key, kwargs[key]), (1, 150 + i*90), ## opencv문자열: table 운동 카운트
                    cv2.FONT_HERSHEY_SIMPLEX, 1, args[0][i], 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.imshow("Table_calculations", table_calculations)
    cv2.moveWindow("Table_calculations", 1013, 510) 