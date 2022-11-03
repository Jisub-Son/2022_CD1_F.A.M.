from datetime import datetime
from threading import Thread
import cv2
import mediapipe as mp

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

def putIterationsPerSec(frame, iterations_per_sec):
    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def noThreading(src1=0, src2=1):
    cap1 = cv2.VideoCapture(src1)
    cap2 = cv2.VideoCapture(src2)
    cps = CountsPerSec().start()

    while True:
        (grabbed1, frame1) = cap1.read()
        (grabbed2, frame2) = cap2.read()
        if not (grabbed1 or grabbed2) or cv2.waitKey(1) == ord("q"):
            break
        
        
        frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
        frame2 = putIterationsPerSec(frame2, cps.countsPerSec())
        cv2.imshow("Video0", frame1)
        cv2.imshow("Video1", frame2)
        cps.increment()

class VideoGet:
    def __init__(self, src1=0):
        self.stream1 = cv2.VideoCapture(src1)
        (self.grabbed1, self.frame1) = self.stream1.read()
        self.frameBuf1 = self.frame1
        self.stopped = False
        
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        
        with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                    min_tracking_confidence=0.5) as pose:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5     
               
            while not self.stopped:
                if not (self.grabbed1 or self.grabbed2):
                    self.stop()
                else:
                    (self.grabbed1, self.frame1) = self.stream1.read()
                    
                    self.frame1 = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)  # OpenCV에서는 BGR 순서로 저장/RGB로 바꿔야 제대로 표시
                    self.frame1.flags.writeable = False
                    results1 = pose.process(self.frame1)                   # landmark 구현
                    self.frame1.flags.writeable = True
                    self.frame1 = cv2.cvtColor(self.frame1, cv2.COLOR_RGB2BGR)  # 원본 frame의 배열 RGB를 BGR로 변경
                    
                    # landmark detection and output -> 두번 쓰는거 말고 깔끔한 방향이 있을까?
                    mp_drawing.draw_landmarks(
                        self.frame1,
                        results1.pose_landmarks,                     # landmark 좌표
                        mp_pose.POSE_CONNECTIONS,                   # landmark 구현
                        mp_drawing.DrawingSpec(color=(0, 0, 255),   # keypoint 연결선 -> 빨간색
                                            thickness=2, 
                                            circle_radius=2),
                        mp_drawing.DrawingSpec(color=(0, 255, 0),   # keypoint 원 -> 초록색
                                            thickness=5,
                                            circle_radius=5),
                    )

                    # 카메라 좌우반전(운동 자세보기 편하게)
                    self.frameBuf1 = cv2.flip(self.frame1, 1)

    def stop(self):
        self.stopped = True

def threadVideoGet(src1=0, src2=1):
    video_getter = VideoGet(src1, src2).start()
    cps = CountsPerSec().start()

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

        frame1 = video_getter.frame1
        frame2 = video_getter.frame2
        frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
        frame2 = putIterationsPerSec(frame2, cps.countsPerSec())
        cv2.imshow("Video0", frame1)
        cv2.imshow("Video1", frame2)
        cps.increment()

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
            cv2.imshow("Video1", self.frame2)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True

def threadVideoShow(src1=0, src2=1):
    cap1 = cv2.VideoCapture(src1)
    cap2 = cv2.VideoCapture(src2)
    (grabbed1, frame1) = cap1.read()
    (grabbed2, frame2) = cap2.read()
    video_shower = VideoShow(frame1, frame2).start()
    cps = CountsPerSec().start()

    while True:
        (grabbed1, frame1) = cap1.read()
        (grabbed2, frame2) = cap2.read()
        if not (grabbed1 or grabbed2) or video_shower.stopped:
            video_shower.stop()
            break

        frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
        frame2 = putIterationsPerSec(frame2, cps.countsPerSec())
        video_shower.frame1 = frame1
        video_shower.frame2 = frame2
        cps.increment()
   
def threadBoth(src1=0, src2=1):
    video_getter0 = VideoGet(src1=0).start()
    video_getter1 = VideoGet(src1=1).start()
    video_shower = VideoShow(frame1=video_getter0.frame1, frame2=video_getter1.frame1).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter0.stopped or video_getter1.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter1.stop()
            video_getter0.stop()
            break

        frame1 = video_getter0.frameBuf1
        frame2 = video_getter1.frameBuf1                                # getThread에서 frame 받아오기
        frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
        frame2 = putIterationsPerSec(frame2, cps.countsPerSec())    # 스켈레톤 붙은 frame에 iterate 텍스트 넣기
        video_shower.frame1 = frame1
        video_shower.frame2 = frame2                                # 최종 frame를 showThread에 보내기
        cps.increment()

# 이 중에서 하나만 주석 해제해서 돌려볼 것
# noThreading()
# threadVideoGet()
# threadVideoShow()
threadBoth()

# getVideoThread 에 mp 내용을 삽입
# getVideoThread(mp까지 처리) -> showVideoThread 구조
# getVideoThread를 2개 실행시킴