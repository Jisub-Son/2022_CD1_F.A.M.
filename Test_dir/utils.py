import mediapipe as mp ## 스켈레톤 구현
import pandas as pd ## keypoint간 빠른계산
import numpy as np ## 스켈레톤 다차원 배열
import cv2 ## opencv

#상수 설정
REF_TIMER = 5                   # timer 초기화(임시로 5초 설정)
REF_VISIBILITY = 0.7            # visibility 기준 초기화
REF_REPS = 5                    # 기준 reps
REF_SETS = 3                    # 기준 sets

mp_pose = mp.solutions.pose ## 스켈레톤

def calculate_angle(a, b, c): ## 각도계산 로직(라디안 -> 각도)
    a = np.array(a) ## 좌표값
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0]) ## 라디안 계산
    angle = np.abs(radians * 180.0 / np.pi) ## 라디안 -> 각도(3.14로 나누기)

    if angle > 180.0: ## 180도 넘지 않게 조정
        angle = 360 - angle

    return angle

def detection(landmarks, keypoint_name): ## keypoint 좌표값 변환 
    return [
        landmarks[mp_pose.PoseLandmark[keypoint_name].value].x,
        landmarks[mp_pose.PoseLandmark[keypoint_name].value].y,
        landmarks[mp_pose.PoseLandmark[keypoint_name].value].visibility
    ]

def detections(landmarks): ## 좌표값 데이터값 변환
    keypoints = pd.DataFrame(columns=["keypoint", "x", "y","visibility"]) ## keypoint 좌표값

    for i, lndmrk in enumerate(mp_pose.PoseLandmark): ## 파이썬 내장함수(for문 in 뒤쪽)
        lndmrk = str(lndmrk).split(".")[1]
        cord = detection(landmarks, lndmrk)
        keypoints.loc[i] = lndmrk, cord[0], cord[1], cord[2]

    return keypoints

def table(exercise, reps, status, set, feedback, timer): ## table 표기내용
    table = cv2.imread("./table.PNG") ## table 위치
    cv2.putText(table, "Exercise            " + exercise.replace("-", " "), ## opencv문자열: table 운동타입(입력한 운동타입)
                (1, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, ## 문자열: 위치, 크기, 색상(검정) 설정
                cv2.LINE_AA)
    cv2.putText(table, "Reps                " + str(reps), (1, 155), ## opencv문자열: table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Status              " + str(status), (5, 210), ## opencv문자열: table 운동 상태
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Set                 " + str(set), (5, 270), ## opencv문자열: table 세트수
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Feedback           " + str(feedback), (5, 330), ## opencv문자열: table 피드백
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Timer               " + str(timer), (5, 390), ## opencv문자열: table 타이머
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.imshow("Table", table) ## table 출력