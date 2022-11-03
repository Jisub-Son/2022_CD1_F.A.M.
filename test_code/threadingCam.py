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
from threading import activeCount

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
    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame
    
class CountsPerSec:
    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0

    def start(self):
        self._start_time = datetime.now()
        return self

    def increment(self):
        self._num_occurrences += 1

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        if elapsed_time == 0:
            return 0
        else:
            return self._num_occurrences / elapsed_time

class VideoGet:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.frameBuf = self.frame
        self.stopped = False
        self.fps = 0.0
        
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        
        global exercise_type ## 가이드 전용 global 변수
        global status_type
        global feedback_type
        
        with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                    min_tracking_confidence=0.5) as pose:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5     
                   
            while not self.stopped:
                if not self.grabbed:
                    self.stop()
                else:
                    (self.grabbed, self.frame) = self.stream.read()
                    
                    self.fps = self.stream.get(cv2.CAP_PROP_FPS)
                    
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # OpenCV에서는 BGR 순서로 저장/RGB로 바꿔야 제대로 표시
                    self.frame.flags.writeable = False
                    results = pose.process(self.frame)                   # landmark 구현
                    self.frame.flags.writeable = True
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)  # 원본 frame의 배열 RGB를 BGR로 변경
                    
                    """# measure exervise with landmarks 
                    try:    
                        landmarks = results1.pose_landmarks.landmark
                        reps, status, sets, feedback, timer = EXERCISE(landmarks).calculate_exercise(
                            args["exercise"], reps, status, sets, feedback, timer)
                    except:
                        pass
                        
                    # make table
                    if src == 0:
                        table(args["exercise"], reps, status, sets, feedback, timer)
                        exercise_type = args["exercise"] ## shadow에서 사용할 변수
                        status_type = status
                        feedback_type = feedback"""
                            
                    # draw 함수화
                    draw(self.frame, results)

                    # 카메라 좌우반전(운동 자세보기 편하게)
                    self.frameBuf = cv2.flip(self.frame, 1)

    def stop(self):
        self.stopped = True

class VideoShow:
    def __init__(self, frame1=None, frame2=None, fps=0.0):
        self.frame1 = frame1
        self.frame2 = frame2
        self.stopped = False
        self.fps = fps
        
    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            
            # calculate fps
            if self.fps == 0.0:
                self.fps = 30.0
            time_per_frame_video = 1/self.fps
            last_time = time.perf_counter()
            time_per_frame = time.perf_counter() - last_time
            time_sleep_frame = max(0,time_per_frame_video - time_per_frame)
            time.sleep(time_sleep_frame)
            real_fps = 1/(time.perf_counter()-last_time)
            last_time = time.perf_counter()
            str = "FPS : %0.2f" % real_fps
            cv2.putText(self.frame1, str, (1,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
            cv2.putText(self.frame2, str, (1,400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
            
            cv2.imshow("Video0", self.frame1)
            cv2.moveWindow("Video0", 0, 0) # 좌표 설정
            cv2.imshow("Video1", self.frame2)
            cv2.moveWindow("Video1", 640, 0) # 좌표 설정
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True
   
def threadBoth(src1=0, src2=1):
    video_getter0 = VideoGet(src=src1).start()
    video_getter1 = VideoGet(src=src2).start()
    video_shower = VideoShow(frame1=video_getter0.frame, frame2=video_getter1.frame).start()
    cps = CountsPerSec().start()

    print("total thread : ", activeCount())
    
    while True:
        if video_getter0.stopped or video_getter1.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter1.stop()
            video_getter0.stop()
            break

        frame1 = video_getter0.frameBuf
        frame2 = video_getter1.frameBuf                              # getThread에서 frame 받아오기
        frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
        frame2 = putIterationsPerSec(frame2, cps.countsPerSec())    # 스켈레톤 붙은 frame에 iterate 텍스트 넣기
        video_shower.frame1 = frame1
        video_shower.frame2 = frame2                                # 최종 frame를 showThread에 보내기
        cps.increment()