import mediapipe as mp 
import pandas as pd 
import numpy as np
import cv2 
import pygame

# set constants for reference
REF_TIMER = 5           
REF_VISIBILITY = 0.7    
REF_REPS = 5            
REF_SETS = 3            

pygame.init()               # init mixer
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

# get keypoints data
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
    pygame.mixer.Sound('rest_time.wav')
    pygame.mixer.Sound('buzzer.wav')
    pygame.mixer.Sound('end.wav')
     
    if pygame.mixer.get_busy() == False:
        return pygame.mixer.Sound(sound + '.wav').play()

# make table
def table(exercise, reps, status, sets, feedback, timer): 
    table = cv2.imread("./table.PNG") # table 이미지 위치
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
    
# make angle table
#def table_angle(value1, angle1, value2, angle2, value3, length3, value4, length4):
def table_angle(value1, angle1, value2, angle2):
    table_angle = cv2.imread("./table_angle.PNG")
    cv2.putText(table_angle, "avg " + str(value1) + " : " + str(angle1), (1, 45), ## opencv문자열: table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table_angle, "avg " + str(value2) + " : " + str(angle2), (1, 105), ## opencv문자열: table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    '''cv2.putText(table_angle, "avg " + str(value3) + " : " + str(length3), (1, 165), ## opencv문자열: table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table_angle, "avg " + str(value4) + " : " + str(length4), (1, 225), ## opencv문자열: table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정'''
    cv2.imshow("Table_angle", table_angle) ## table 출력
    cv2.moveWindow("Table_angle", 1013, 510) 