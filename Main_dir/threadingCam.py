import cv2
import mediapipe as mp
import time
from threading import Thread
from threading import active_count
from datetime import datetime
from utils import *
from exercise import EXERCISE

# # initialize variables
# def initState():
#     mode = 'Choose'    
#     reps = 0                        
#     status = 'Up'                   
#     sets = 0                        
#     feedback = 'start exercise'     
#     timer = REF_TIMER               
#     return [mode, reps, status, sets, feedback, timer]

class stateInfo:
    def __init__(self):
        print("init")
        self.mode = 'Choose'    
        self.reps = 0                        
        self.status = 'Up'                   
        self.sets = 0                        
        self.feedback = 'start exercise'     
        self.timer = REF_TIMER
        
state_info = stateInfo()

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

def putIterationsPerSec(frame, iterations_per_sec):
    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

class VideoGet:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.frameBuf = self.frame
        self.stopped = False
        self.fps = 0.0
        self.camID = src
        
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        global state_info
        # state_info = stateInfo()
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        
        with mp_pose.Pose(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as pose:  

            while not self.stopped:
                if not self.grabbed:
                    self.stop()
                else:
                    (self.grabbed, self.frame) = self.stream.read()
                    self.fps = self.stream.get(cv2.CAP_PROP_FPS)
                    
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                    self.frame.flags.writeable = False
                    results = pose.process(self.frame) 
                    self.frame.flags.writeable = True
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
                    
                    # measure exervise with landmarks
                    try:    
                        landmarks = results.pose_landmarks.landmark
                        state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer, self.camID = EXERCISE(landmarks).calculate_exercise(
                            state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer, self.camID)
                        # print("Get : ", state_info.mode)
                    except:
                        pass
                    
                    # landmark detection and output 
                    mp_drawing.draw_landmarks(
                        self.frame,
                        results.pose_landmarks,                     # landmark 좌표
                        mp_pose.POSE_CONNECTIONS,                   # landmark 구현
                        mp_drawing.DrawingSpec(color=(0, 0, 255),   # keypoint 연결선 -> 빨간색
                                            thickness=2, 
                                            circle_radius=2),
                        mp_drawing.DrawingSpec(color=(0, 255, 0),   # keypoint 원 -> 초록색
                                            thickness=5,
                                            circle_radius=5),
                    )

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
        global state_info
        
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
            
            # make table
            table(state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer)
            
            cv2.imshow("Video0", self.frame1)
            cv2.imshow("Video1", self.frame2)
            
            # key input for exit, mode, reset
            key = cv2.waitKey(1) & 0xFF     # 키보드 입력
            if key == ord('q'):             # exit
                print("exit")
                self.stopped = True  
            elif key == ord('s'):           # squat mode
                state_info.__init__()
                state_info.mode = "squat"
                print("Show : ", state_info.mode)
            elif key == ord('p'):           # pushup mode
                state_info.__init__()
                state_info.mode = "pushup"
                print("Show : ", state_info.mode)
            elif key == ord('r'):           # reset
                state_info.__init__()
                # state_info.mode = "reset"
                print("Show : ", state_info.mode)

    def stop(self):
        self.stopped = True