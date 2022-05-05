import cv2 ## opencv
import argparse ## cmd창에서 실행가능 -> 추후 라즈베리파이 리눅스에서 실행
from utils import * ## utils 불러오기
import mediapipe as mp ## 미디어파이프 스켈레톤 구현
from body_part_angle import BodyPartAngle ## boby_part_angle 불러오기
from types_of_exercise import TypeOfExercise ## types_od _exercise 불러오기
import time ## 타이머 사용

ap = argparse.ArgumentParser() ## argparse 설정 python main.py -mode squat 로 실행가능
ap.add_argument("-mode",
                "--exercise_type",
                type=str,
                help='Type of activity to do',
                required=True)
ap.add_argument("-vs",
                "--video_source",
                type=str,
                help='Type of activity to do',
                required=False)
args = vars(ap.parse_args())

mp_drawing = mp.solutions.drawing_utils ## 스켈레톤 구현
mp_pose = mp.solutions.pose

if args["video_source"] is not None: ## 카메라 켜기
    cap = cv2.VideoCapture(args["video_source"])
else:
    cap = cv2.VideoCapture(0)

cap.set(3, 800) ## 카메라 넓이 설정
cap.set(4, 480) ## 카메라 높이 설정

with mp_pose.Pose(min_detection_confidence=0.5, ## 미디어파이프 설정
                  min_tracking_confidence=0.5) as pose:

    counter = 0  ## 운동횟수
    status = True  # 상태
    set = 0 ## 세트 수
    feedback = "start exercise" ## 운동시작 전
    count = 0 ## 타이머
    
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
        ## recolor frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) ## 카메라 RGB
        frame.flags.writeable = False
        results = pose.process(frame) ## 스켈레톤 구현
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) ## BGR

        try: ## 스켈레톤을 통해 운동횟수 계산
            landmarks = results.pose_landmarks.landmark
            counter, status, set, feedback, count = TypeOfExercise(landmarks).calculate_exercise(
                args["exercise_type"], counter, status, set, feedback, count)
        except:
            pass

        score_table(args["exercise_type"], counter, status, set, feedback, count) ## 테이블 표시 내용

        mp_drawing.draw_landmarks( ## 랜드마크 감지/출력
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 255), ## keypoint 연결 빨간색
                                   thickness=2,
                                   circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 255, 0), ## keypoint 원 초록색
                                   thickness=5,
                                   circle_radius=5),
        )

        frame = cv2.flip(frame, 1) ## 카메라 좌우반전
        
        cv2.imshow('Video', frame) ## q누르면 종료
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
