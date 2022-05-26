# 
# 2022-1 CD1 Team-1
# Project Name  : F.A.M.(Fitness Assistant Module)
# Member        : 손지섭(팀장), 강태영, 이석진, 정홍택
# 

# import cv2                      # opencv import        
import argparse                 # 실행 인자 추가 
# import mediapipe as mp          # 스켈레톤 구현 
from utils import *             # utils
# from keypoint import KEYPOINT   # keypoint 불러오기
# from exercise import EXERCISE   # exercise 불러오기
from threadingCam import camThread

'''#변수 초기화
reps = 0                        # rep 수 초기화
status = 'Up'                   # 운동 상태 초기화    
sets = 0                        # set 수 초기화
feedback = 'start exercise'     # feedback 초기화 : 운동 시작 전'''

#상수 설정
REF_TIMER = 5                   # timer 초기화(임시로 5초 설정)
REF_VISIBILITY = 0.8            # visibility 기준 초기화
REF_REPS = 5                    # 기준 reps
REF_SETS = 3                    # 기준 sets

# argparse setting
ap = argparse.ArgumentParser()  # argparse 설정 python main.py -mode squat 로 실행가능
ap.add_argument("-mode",
                "--exercise",
                type=str,
                help='activity',
                required=True)
args = vars(ap.parse_args())

# Create two threads as follows
thread1 = camThread("Camera 0", 0, args)
thread2 = camThread("Camera 1", 1, args)
thread1.start()
thread2.start()