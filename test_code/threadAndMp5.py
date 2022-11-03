from datetime import datetime
from threading import Thread
import cv2
import mediapipe as mp
import time

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
    def __init__(self, src1=0, src2=1):
        self.stream1 = cv2.VideoCapture(src1)
        self.stream2 = cv2.VideoCapture(src2)
        # print("Video Get : ", src1, ", ", src2)
        (self.grabbed1, self.frame1) = self.stream1.read()
        (self.grabbed2, self.frame2) = self.stream2.read()
        self.frameBuf1 = self.frame1
        self.frameBuf2 = self.frame2
        self.stopped = False
        
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                    min_tracking_confidence=0.5) as pose1:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5     
            with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                    min_tracking_confidence=0.5) as pose2:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5       
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
                    
                        # draw 함수화
                        draw(self.frame1, results1)
                        draw(self.frame2, results2)

                        # 카메라 좌우반전(운동 자세보기 편하게)
                        self.frameBuf1 = cv2.flip(self.frame1, 1)
                        self.frameBuf2 = cv2.flip(self.frame2, 1)
                    
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
            cv2.imshow("Video1", self.frame2)
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

threadBoth()

# fps 추가