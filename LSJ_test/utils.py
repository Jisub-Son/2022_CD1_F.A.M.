import mediapipe as mp ## 스켈레톤 구현
import pandas as pd ## keypoint간 빠른계산
import numpy as np ## 스켈레톤 다차원 배열
import cv2 ## opencv

mp_pose = mp.solutions.pose ## 스켈레톤

def calculate_angle(a, b, c): ## 각도계산 로직(라디안 -> 각도)
    a = np.array(a) ## 좌표값
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0]) ## 라디안 계산
    angle = np.abs(radians * 180.0 / np.pi) ## 라디안 -> 각도 (180/π를 곱하기)

    if angle > 180.0: ## 180도 넘지 않게 조정
        angle = 360 - angle

    return angle

def detection(landmarks, keypoint_name): ## keypoint 좌표값 변환
    return [
        landmarks[mp_pose.PoseLandmark[keypoint_name].value].x,
        landmarks[mp_pose.PoseLandmark[keypoint_name].value].y,
        landmarks[mp_pose.PoseLandmark[keypoint_name].value].visibility
    ]

"""def detections(landmarks): ## 좌표값 데이터값 변환
    keypoints = pd.DataFrame(columns=["keypoint", "x", "y"]) ## keypoint 좌표값

    
    for i, lndmrk in enumerate(mp_pose.PoseLandmark): ## 파이썬 내장함수(for문 in 뒤쪽), 2차원배열에서 인덱스 오타 적음
        lndmrk = str(lndmrk).split(".")[1]
        cord = detection(landmarks, lndmrk)
        keypoints.loc[i] = lndmrk, cord[0], cord[1]

    return keypoints
"""
def table(exercise, timerer, status, set, feedback, timer,camID): ## table 표기내용
    table = cv2.imread("./table.PNG") ## table 위치
    cv2.putText(table, "CapstoneDisign1 Team-1", ## opencv문자열: 제목
                (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, ## 문자열: 위치, 크기, 색상(검정) 설정
                cv2.LINE_AA)
    cv2.putText(table, "Exercise : " + exercise.replace("-", " "), ## opencv문자열: table 운동타입(입력한 운동타입)
                (1, 75), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, ## 문자열: 위치, 크기, 색상(검정) 설정
                cv2.LINE_AA)
    cv2.putText(table, "Reps : " + str(timerer), (1, 110), ## opencv문자열: table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Status : " + str(status), (5, 145), ## opencv문자열: table 운동 상태
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Set : " + str(set), (5, 180), ## opencv문자열: table 세트수
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Feedback : " + str(feedback), (5, 215), ## opencv문자열: table 피드백
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "Timer : " + str(timer), (5, 250), ## opencv문자열: table 타이머
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.putText(table, "CamID : " + str(camID), (150, 285), ## opencv문자열: table 타이머
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA) ## 문자열: 위치, 크기, 색상(검정) 설정
    cv2.imshow("Table" + str(camID), table) ## table 출력