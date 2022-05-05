import mediapipe as mp ## 스켈레톤 구현
import pandas as pd ## keypoint간 빠른계산
import numpy as np ## 스켈레톤 다차원 배열
import cv2 ## opencv

mp_pose = mp.solutions.pose ## 스켈레톤

def calculate_angle(a, b, c): ## 각도계산 로직(라디안 -> 각도)
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) -\
              np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0: ## 180도 넘지 않게 조정
        angle = 360 - angle

    return angle

def calculate_distance(a, b): ## 거리계산 좌표사이의 거리 공식
    a = np.array(a)  # First
    b = np.array(b)  # second
    
    distance = np.sqrt(np.sum(np.square(a-b)))
    
    return distance

def detection_body_part(landmarks, body_part_name): ## keypoint 좌표값 변환
    return [
        landmarks[mp_pose.PoseLandmark[body_part_name].value].x,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].y,
        landmarks[mp_pose.PoseLandmark[body_part_name].value].visibility
    ]

def detection_body_parts(landmarks): ## 좌표값 데이터값 변환
    body_parts = pd.DataFrame(columns=["body_part", "x", "y"])

    for i, lndmrk in enumerate(mp_pose.PoseLandmark):
        lndmrk = str(lndmrk).split(".")[1]
        cord = detection_body_part(landmarks, lndmrk)
        body_parts.loc[i] = lndmrk, cord[0], cord[1]

    return body_parts

def score_table(exercise, counter, status, set, feedback, pose_feedback, count): ## table 표기내용
    score_table = cv2.imread("C:/CD_Code/table.png") ## table 위치
    cv2.putText(score_table, "CapstoneDisign1 Team-1", ## 제목
                (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2,
                cv2.LINE_AA)
    cv2.putText(score_table, "Exercise : " + exercise.replace("-", " "), ## table 운동타입(입력한 운동타입)
                (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2,
                cv2.LINE_AA)
    cv2.putText(score_table, "Count : " + str(counter), (10, 100), ## table 운동 카운트
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(score_table, "Status : " + str(status), (10, 135), ## table 운동 상태
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(score_table, "Set : " + str(set), (10, 170), ## table 세트수
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(score_table, "Feedback : " + str(feedback), (10, 205), ## table 피드백
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(score_table, "PoseFeedback : " + str(pose_feedback), (10, 240), ## table 피드백
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(score_table, "Timer : " + str(count), (10, 275), #3 table 타이머
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow("Table", score_table) ## table 출력