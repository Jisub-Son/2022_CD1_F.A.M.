import cv2
import mediapipe as mp
import time
from threading import Thread
from threading import active_count
from datetime import datetime
from utils import *
from exercise import * # exercise.py의 전부 불러옴

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
        
# initialize variables
class stateInfo:
    def __init__(self):        
        self.mode = 'Choose'
        self.reps = 0                        
        self.status = 'Up'                   
        self.sets = 0                        
        self.feedback = 'start exercise'     
        self.timer = REF_TIMER

state_info = stateInfo()

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
        self.camID = src
        
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self): 
        global state_info
        
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
                    # measure exercise with landmarks 
                    try:    
                        landmarks = results.pose_landmarks.landmark
                        state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer, self.camID = EXERCISE(landmarks).calculate_exercise(
                            state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer, self.camID)
                    except:
                        pass
                            
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
        global state_info
                
        """global exercise_type ## 가이드 전용 global 변수
        global status_type
        global feedback_type"""
        
        """squat_down = 1 ## 초기화
            squat_up = 51
            pushup_down = 1
            pushup_up = 60
            sidelateralraise_up = 1
            sidelateralraise_down = 35"""
            
        while not self.stopped:
            
            # key input for exit, mode, reset
            key = cv2.waitKey(1) & 0xFF     # 키보드 입력
            if key == ord('q'):             # exit
                self.stopped = True  
            elif key == ord('s'):           # squat mode
                state_info.__init__()
                state_info.mode = "squat"
            elif key == ord('p'):           # push up mode
                state_info.__init__()
                state_info.mode = "pushup"
            elif key == ord('l'):           # side lateral raise mode
                state_info.__init__()
                state_info.mode = "sidelateralraise"
            elif key == ord('r'):           # reset
                state_info.__init__()
                state_info.feedback = "choose exercise"
            
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
            
            # make table
            table(state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer)
            #exercise_type = args ## shadow에서 사용할 변수
            #status_type = status
            #feedback_type = feedback
            
            # make culculate table
            if state_info.mode == "squat":
                table_calculations(color, right_leg = right_leg_angle, avg_knee = avg_knee_angle, foot_ratio = heel_foot_ratio)
                ##table_calculations(color, easter_elbow = right_elbow_angle, easter_shoulder = right_shoulder_angle, easter_wrist = right_wrist_angle) ## 이스터 확인용
            elif state_info.mode == "pushup":
                table_calculations(color, right_arm = right_arm_angle, right_spine = right_spine_angle, wrist_ratio = wrist_shoulder_ratio)
            elif state_info.mode == "sidelateralraise":    
                table_calculations(color, right_shoulder = right_shoulder_angle, right_elbow = right_elbow_angle, parellel_ratio = heel_foot_ratio)
                
            cv2.imshow("Video0", self.frame1)
            cv2.moveWindow("Video0", 0, 0) # 좌표 설정
            cv2.imshow("Video1", self.frame2)
            cv2.moveWindow("Video1", 640, 0) # 좌표 설정
                
            

    def stop(self):
        self.stopped = True