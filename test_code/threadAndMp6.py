from datetime import datetime
from threading import Thread
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw(frame, results):
    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,                     # landmark 좌표
        mp_pose.POSE_CONNECTIONS,                   # landmark 구현
        mp_drawing.DrawingSpec(color=(0, 0, 255),   # keypoint 연결선 -> 빨간색
                                thickness=2, 
                                circle_radius=2),
        mp_drawing.DrawingSpec(color=(0, 255, 0),   # keypoint 원 -> 초록색
                                thickness=5,
                                circle_radius=5),
    )   
            
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

class VideoGet:
    def __init__(self, src1=0, src2=0):
        self.stream1 = cv2.VideoCapture(src1)
        self.stream2 = cv2.VideoCapture(src2)
        # print("Video Get : ", src1, ", ", src2)
        (self.grabbed1, self.frame1) = self.stream1.read()
        (self.grabbed2, self.frame2) = self.stream2.read()
        self.stopped = False
        
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not (self.grabbed1 or self.grabbed2):
                self.stop()
            else:
                (self.grabbed1, self.frame1) = self.stream1.read()
                (self.grabbed2, self.frame2) = self.stream2.read()

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
            cv2.imshow("Video1", self.frame2)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True

class AddMediapipe:                 # mp 스켈레톤을 그리는 것도 클래스로 만들어 thread으로 돌린다면?
    def __init__(self, frame1=None, frame2=None):
        self.frame1 = frame1
        self.frameBuf1 = frame1
        self.frame2 = frame2        # 입력으로 받을 self.변수
        self.frameBuf2 = frame2     # 출력으로 내보낼 self.변수
        self.stopped = False
        
    def start(self):
        Thread(target=self.AddMp, args=()).start()
        return self
    
    def AddMp(self):                
        with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                    min_tracking_confidence=0.5) as pose1:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5    
             
            with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                    min_tracking_confidence=0.5) as pose2:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5  
                
                while not self.stopped:
                    
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
                
                    # draw 함수화
                    draw(self.frame1, results1)
                    draw(self.frame2, results2)

                    # 카메라 좌우반전(운동 자세보기 편하게)
                    self.frameBuf1 = cv2.flip(self.frame1, 1)
                    self.frameBuf2 = cv2.flip(self.frame2, 1)
   
                    if cv2.waitKey(1) == ord("q"):
                        self.stopped = True
    
    def stop(self):
        self.stopped = True

def threadAll(src1=0, src2=1):              # 3개 쓰레드를 모두 실행시켰을 경우
    # 3개 쓰레드 모두 실행
    video_getter = VideoGet(src1, src2).start()
    video_adder = AddMediapipe(frame1 = video_getter.frame1, frame2=video_getter.frame2).start()
    video_shower = VideoShow(frame1=video_adder.frameBuf1, frame2=video_adder.frameBuf2).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped or video_adder.stopped:
            video_shower.stop()
            video_adder.stop()
            video_getter.stop()
            break
        
        frame1 = video_getter.frame1
        frame2 = video_getter.frame2            # getThread에서 frame 받아오기
        
        video_adder.frame1 = frame1
        video_adder.frame2 = frame2             # 읽은 frame을 mpThread에 보내기
        
        frame1 = putIterationsPerSec(video_adder.frameBuf1, cps.countsPerSec())
        frame2 = putIterationsPerSec(video_adder.frameBuf2, cps.countsPerSec())     # 스켈레톤 붙은 frame에 텍스트 넣기
        
        video_shower.frame1 = frame1
        video_shower.frame2 = frame2            # 최종 frame를 showThread에 보내기
        
        cps.increment()

threadAll()