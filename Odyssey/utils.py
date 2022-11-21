import mediapipe as mp 
import pandas as pd 
import numpy as np
import cv2 
import pygame

# set constants for reference
REF_TIMER = 3
REF_VISIBILITY = 0.7
REF_ROUGH_VISIBILITY = 0.0
REF_REPS = 3
REF_SETS = 2
RIGHT_CAM = 2 # usb 2-input port 위: 2번 카메라
LEFT_CAM = 0 # usb 2-input port 아래: 0번 카메라

# init mixer
pygame.init() # 윈도우는 역슬래쉬(\), 리눅스는 슬래쉬(/)
pygame.mixer.Sound("sound/rest_time.wav")        # 쉬는 시간입니다
pygame.mixer.Sound("sound/buzzer.wav")           # 버저음
pygame.mixer.Sound("sound/end.wav")              # 운동이 종료되었습니다 
pygame.mixer.Sound("sound/kneedown.wav")         # 무릎을 넎으세요
pygame.mixer.Sound("sound/lessdown.wav")         # 너무 내려갔습니다
pygame.mixer.Sound("sound/moredown.wav")         # 더 내리세요
pygame.mixer.Sound("sound/parallel.wav")         # 발을 11자로 해주세요
pygame.mixer.Sound("sound/shoulder_length.wav")  # 발을 어깨넓이로 벌리세요
pygame.mixer.Sound("sound/spine.wav")            # 허리를 더 펴주세요
pygame.mixer.Sound("sound/hand.wav")             # 손을 더 모아주세요
pygame.mixer.Sound("sound/lessraise.wav")        # 팔을 조금만 벌리세요
pygame.mixer.Sound("sound/moreraise.wav")        # 팔을 더 벌리세요
pygame.mixer.Sound("sound/lessbend.wav")         # 팔꿈치를 조금만 구부리세요
pygame.mixer.Sound("sound/start_exercise.wav")   # 쉬는 시간 종료
pygame.mixer.Sound("sound/easter.wav")           # 이스터(졸업을 축하합니다)
pygame.mixer.Sound("sound/squat.wav")            # 스쿼트 모드입니다 
pygame.mixer.Sound("sound/pushup.wav")           # 푸쉬업 모드입니다
pygame.mixer.Sound("sound/sidelateralraise.wav") # 사이드레터럴레이즈 모드입니다
pygame.mixer.Sound("sound/reset.wav")            # 초기화되었습니다 운동을 선택하세요
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
        pygame.mixer.Sound('sound/' +  sound + '.wav').play()
    else:
        if prev_sound != sound:                             # 약간 인터럽트처럼 작동됨 end 재생       
            pygame.mixer.stop()                             # -> buzzer가 울리는 중에 end가 울려야 한다면 buzzer를 즉시 끄고 end 재생 
            pygame.mixer.Sound('sound/' + sound + '.wav').play()       # -> buzzer가 울리는 중에 buzzer가 약간 겹쳐서 호출되면 새로 재생하지는 않음    
        else:
            pass

# make table
def table(mode, reps, status, sets, feedback, timer): 
    table = cv2.imread("table/finaltable.PNG") # table 이미지 위치
    cv2.putText(table, "              " + str(mode), (1, 70), ## opencv문자열: table 운동타입(입력한 운동타입)
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "              " + str(reps), (1, 120), ## opencv문자열: table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "              " + str(status), (1, 160), ## opencv문자열: table 운동 상태
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "              " + str(sets), (1, 200), ## opencv문자열: table 세트수
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "              " + str(feedback), (1, 240), ## opencv문자열: table 피드백
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "              " + str(timer), (1, 285), ## opencv문자열: table 타이머
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    
    table = cv2.resize(table, dsize=(1920, 360))    # table.width == frame.width*2 와 같도록 설정
                                                    # table.width = 1920 = 960*2, table.height = 360
    return table