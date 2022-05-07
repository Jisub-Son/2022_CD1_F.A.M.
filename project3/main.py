# 
# 2022-1 CD1 Team-1
# Project Name  : F.A.M.(Fitness Assistant Module)
# Member        : 손지섭(팀장), 강태영, 이석진, 정홍택
# 

#import packages
import cv2                      # opencv import        
import argparse                 # 실행 인자 추가, 이거 필요없을 것 같은데 뺄 수 있음 빼자 
import mediapipe as mp          # 스켈레톤 구현 
import time                     # 타이머 사용
from utils import *             # utils
from keypoint import KEYPOINT   # keypoint 불러오기
from exercise import EXERCISE   # exercise 불러오기

'''argument 하나 삭제함 -> 비디오 소스 사용하는 용도였음(우린 안쓰니깐)
지금은 squat랑 pushup을 따로 실행하니깐 쓰는데
나중에는 삭제하는게 맞을 듯
얘 없으면 그냥 python main.py로 실행 가능함'''

# argparse setting
ap = argparse.ArgumentParser()  # argparse 설정 python main.py -mode squat 로 실행가능
ap.add_argument("-mode",
                "--exercise",
                type=str,
                help='activity',
                required=True)
args = vars(ap.parse_args())

'''cap->capture로 바꿨고, 카메라 세팅에 있던 if문도 삭제함
이것도 예제 영상 받아오는 거에 관련된 코드였음'''

# camera setting
# 카메라 영상을 받아올 객체 선언 및 가로, 세로 길이 설정
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# mediapipe setting
# 스켈레톤 구현
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.5, ## 최소감지신뢰값([0.0, 1.0]) 기본값=0.5 설정
                  min_tracking_confidence=0.5) as pose: ## 최소추적신뢰값([0.0, 1.0]) 기본값=0.5 설정
    
    '''변수 counter -> reps, set -> sets로 변경 count랑 헷갈려서'''
    
    reps = 0                        # rep 수 초기화
    status = 'Up'                   # 운동 상태 초기화    
    sets = 0                        # set 수 초기화
    feedback = 'start exercise'     # feedback 초기화 : 운동 시작 전
    count = 5                       # timer 초기화    
    
    while capture.isOpened():
        ret, frame = capture.read() # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret == True
        
        '''여기서부터 try 전까지 있는거 필요없는거 있음 빼자'''
        
        frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA) # recolor frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 카메라 RGB
        frame.flags.writeable = False
        results = pose.process(frame)   # 스켈레톤 구현
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # BGR
        
        try:    # 스켈레톤을 통해 운동횟수 계산
            landmarks = results.pose_landmarks.landmark
            reps, status, sets, feedback, count = EXERCISE(landmarks).calculate_exercise(
                args["exercise"], reps, status, sets, feedback, count)
        except:
            pass
        
        table(args["exercise"], reps, status, sets, feedback, count)    # 테이블 내용 표시

        # 랜드마크 감지/출력
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,     # 랜드마크 좌표
            mp_pose.POSE_CONNECTIONS,   # 스켈레톤 구현
            mp_drawing.DrawingSpec(color=(0, 0, 255),   # keypoint 연결 빨간색
                                   thickness=2, 
                                   circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 255, 0),   # keypoint 원 초록색
                                   thickness=5,
                                   circle_radius=5),
        )
        
        frame = cv2.flip(frame, 1)  # 카메라 좌우반전
        
        cv2.imshow('Video', frame)  # q누르면 종료
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    capture.release()       # 캡쳐 객체를 없애줌
    cv2.destroyAllWindows() # 모든 영상 창을 닫아줌