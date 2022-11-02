from datetime import datetime
from threading import Thread
import cv2
import mediapipe as mp
import threading
from keypoint import *
from utils import *
from exercise import *
import time
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# initialize variables
def initState():        
    reps = 0                        
    status = 'Up'                   
    sets = 0                        
    feedback = 'start exercise'     
    timer = REF_TIMER               
    return [reps, status, sets, feedback, timer]
        
# drawing skeleton        
def draw(frame, results):
    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,                     # landmark 좌표
        mp_pose.POSE_CONNECTIONS,                   # landmark 구현
        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2), # keypoint 연결선 -> 빨간색
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5), # keypoint 원 -> 초록색 
    )       

# iteration
def putIterationsPerSec(frame, iterations_per_sec):
    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec), (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame    
        
class CountsPerSec:
    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0

    def start(self):
        self._start_time = datetime.now()
        print("cps start")
        return self

    def increment(self):
        self._num_occurrences += 1

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        if elapsed_time == 0:
            return 0
        else:
            return self._num_occurrences / elapsed_time

class VideoGet():
    def __init__(self, src1=0, src2=1):
        self.stream1 = cv2.VideoCapture(src1)
        self.stream2 = cv2.VideoCapture(src2)
        print("Video Get : ", src1, ", ", src2)
        (self.grabbed1, self.frame1) = self.stream1.read()
        (self.grabbed2, self.frame2) = self.stream2.read()
        self.frameBuf1 = self.frame1
        self.frameBuf2 = self.frame2
        self.stopped = False
        
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self): #args 필요
        with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                    min_tracking_confidence=0.5) as pose1:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5     
            with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                    min_tracking_confidence=0.5) as pose2:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5       
                
                # init variables
                reps, status, sets, feedback, timer = initState() 
                
                while not self.stopped:
                    if not (self.grabbed1 or self.grabbed2):
                        self.stop()
                    else:
                        (self.grabbed1, self.frame1) = self.stream1.read()
                        (self.grabbed2, self.frame2) = self.stream2.read()
                 
                        self.frame1 = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)  # OpenCV에서는 BGR 순서로 저장/RGB로 바꿔야 제대로 표시
                        self.frame2 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
                        self.frame1.flags.writeable = False
                        self.frame2.flags.writeable = False
                        results1 = pose1.process(self.frame1)                   # landmark 구현
                        results2 = pose2.process(self.frame2)
                        self.frame1.flags.writeable = True
                        self.frame2.flags.writeable = True
                        self.frame1 = cv2.cvtColor(self.frame1, cv2.COLOR_RGB2BGR)  # 원본 frame의 배열 RGB를 BGR로 변경
                        self.frame2 = cv2.cvtColor(self.frame2, cv2.COLOR_RGB2BGR)
                    
                        # measure exervise with landmarks 
                        """try:    
                            landmarks = results1.pose_landmarks.landmark
                            reps, status, sets, feedback, timer = EXERCISE(landmarks).calculate_exercise(
                                args["exercise"], reps, status, sets, feedback, timer)
                        except:
                             pass
                        
                        # make table
                        #if src1 == 0:
                        table(args["exercise"], reps, status, sets, feedback, timer)
                            #exercise_type = args["exercise"] ## shadow에서 사용할 변수
                            #status_type = status
                            #feedback_type = feedback"""
                     
                        # draw 함수화
                        draw(self.frame1, results1)
                        draw(self.frame2, results2)

                        # 카메라 좌우반전(운동 자세보기 편하게)
                        self.frameBuf1 = cv2.flip(self.frame1, 1)
                        self.frameBuf2 = cv2.flip(self.frame2, 1)    
    
    def stop(self):
        self.stopped = True
        
class VideoShow:
    def __init__(self, frame1=None, frame2=None):
        self.frame1 = frame1
        self.frame2 = frame2
        self.stopped = False
        
    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video0", self.frame1)
            cv2.moveWindow("Video0", 0, 0) # 좌표 설정
            cv2.imshow("Video1", self.frame2)
            cv2.moveWindow("Video1", 640, 0) # 좌표 설정
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True
   
def threadBoth(src1=0, src2=1):
    video_getter = VideoGet(src1, src2).start()
    video_shower = VideoShow(frame1=video_getter.frame1, frame2=video_getter.frame2).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame1 = video_getter.frameBuf1
        frame2 = video_getter.frameBuf2                                # getThread에서 frame 받아오기
        frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
        frame2 = putIterationsPerSec(frame2, cps.countsPerSec())    # 스켈레톤 붙은 frame에 iterate 텍스트 넣기
        video_shower.frame1 = frame1
        video_shower.frame2 = frame2                                # 최종 frame를 showThread에 보내기
        cps.increment()
        
# 기존 코드에서 def shadow()함수 utils로 보내고 실행 가능한 것 확인 완료                
# 운동 카운트에 꼭 필요한 부분 먼저 수정 중(thradingCam.py만 수정, main.py는 boththread로 변경하여 빌드)
# arg["exercise"]를 불어오는 과정에서 아직 해결 못함
# arg["exercise"] 날린 후 실행하면(utils의 table 함수, exercise의 calculate_exercise 함수의 exercise 부분도 날려야함) 테이블 window만 나오고 출력되지는 않음
# 현재 frame, skeleton은 큰 이상 없는 것으로 보임 + iteration: 12,000
# 내일(목) 오디세이에서 threadAndMp5.py 테스트 예정
# 기존코드에서 threadingCam.py만 바꾸고 main.py에 boththread()만 넣으면 실행됨