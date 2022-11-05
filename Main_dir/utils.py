import mediapipe as mp 
import pandas as pd 
import numpy as np
import cv2 
import pygame

# set constants for reference
REF_TIMER = 10
REF_VISIBILITY = 0.7
REF_ROUGH_VISIBILITY = 0.0
REF_REPS = 2
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
            pygame.mixer.stop()                             # -> buzzer가 울리는 중에 end가 울려야 한다면 buzzer를 즉시 끄고 end 재생 
            pygame.mixer.Sound('sound\./' + sound + '.wav').play()       # -> buzzer가 울리는 중에 buzzer가 약간 겹쳐서 호출되면 새로 재생하지는 않음    
        else:
            pass
        
# display guide
def shadow(file, frame, camID, r, c): 
    file_inv = cv2.flip(file, 1) ## 좌우반전
    if file is None:
        print('image load failed!')
    # logo with frame0   
    rows, cols, channels = file.shape ## 로고 픽셀값
    roi = frame[r:rows + r, c:cols + c] ## 로고를 필셀값 ROI(관심영역)
    gray = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY) ## 로고를 gray로 변환
    ret, mask = cv2.threshold(gray, 97, 255, cv2.THRESH_BINARY) ## 이진영상으로 변환 (흰색배경, 검정로고)
    mask_inv = cv2.bitwise_not(mask) ## mask 반전
    background = cv2.bitwise_and(roi, roi, mask = mask) ## 캠화면에 넣을 위치 black
    shadowpartner = cv2.bitwise_and(file, file, mask = mask_inv) ## 로고에서 캠화면에 출력할 부분
    final0 = cv2.bitwise_or(background, shadowpartner) ## 캠화면의 검정부분과 로고 출력부분 합성
    # logo with frame1
    rows, cols, channels = file_inv.shape ## 로고 픽셀값
    roi = frame[r:rows + r, c:cols + c] ## 로고를 필셀값 ROI(관심영역)
    gray = cv2.cvtColor(file_inv, cv2.COLOR_BGR2GRAY) ## 로고를 gray로 변환
    ret, mask = cv2.threshold(gray, 97, 255, cv2.THRESH_BINARY) ## 이진영상으로 변환 (흰색배경, 검정로고)
    mask_inv = cv2.bitwise_not(mask) ## mask 반전
    background = cv2.bitwise_and(roi, roi, mask = mask) ## 캠화면에 넣을 위치 black
    shadowpartner = cv2.bitwise_and(file_inv, file_inv, mask = mask_inv) ## 로고에서 캠화면에 출력할 부분
    final1 = cv2.bitwise_or(background, shadowpartner) ## 캠화면의 검정부분과 로고 출력부분 합성
    # display shadowpartner
    if camID == RIGHT_CAM: 
        frame[r:rows + r, c:cols + c] = final0 ## 캠화면에 실시간으로 출력하기 위해 합성 
    elif camID == LEFT_CAM: ## cam1 에는 flip된 영상 출력         
        frame[r:rows + r, c:cols + c] = final1       

# make table
def table(mode, reps, status, sets, feedback, timer): 
    table = cv2.imread("table\./table.PNG") # table 이미지 위치
    cv2.putText(table, "Exercise            " + str(mode), (1, 95), ## opencv문자열: table 운동타입(입력한 운동타입)
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
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
    
    table = cv2.resize(table, dsize=(1280, 510))    # table.width == frame.width*2 와 같도록 설정
                                                    # table.width = 1280 = 640*2, table.height = (1280/1012)*403 = 510 
    return table

# make calculations table    
def table_calculations(*args, **kwargs):
    table_calculations = cv2.imread("table\./table_angle.PNG")
    for i, key in enumerate(kwargs):
        cv2.putText(table_calculations, "{} : {:.4f}".format(key, kwargs[key]), (1, 150 + i*90), ## opencv문자열: table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 1, args[0][i], 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.imshow("Table_calculations", table_calculations)
    # cv2.moveWindow("Table_calculations", 1013, 510) 