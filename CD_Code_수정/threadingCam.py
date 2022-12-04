import cv2
import mediapipe as mp
from threading import Thread
from utils import *
from exercise import *
from guide import *
import time

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
    )

class VideoGet:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
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
                    
                    # display guide
                    guide(state_info.mode, state_info.status, state_info.feedback, self.frameBuf, self.camID)
                    
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
        
        prevTime = 0
        
        while not self.stopped:
            
            # key input for exit, mode, reset
            key = cv2.waitKey(1) & 0xFF     # 키보드 입력
            if key == ord('q'):             # exit
                self.stopped = True  
            elif key == ord('s'):           # squat mode
                state_info.__init__()
                state_info.mode = "squat"
                voiceFeedback('squat')
            elif key == ord('p'):           # push up mode
                state_info.__init__()
                state_info.mode = "pushup"
                voiceFeedback('pushup')
            elif key == ord('l'):           # side lateral raise mode
                state_info.__init__()
                state_info.mode = "sidelateralraise"
                voiceFeedback('sidelateralraise')
            elif key == ord('r'):           # reset
                state_info.__init__()
                state_info.feedback = "choose exercise"
                voiceFeedback('reset')
            
            # put txt: fps
            curTime = time.time()
            sec = curTime - prevTime
            prevTime = curTime
            frame_per_sec = 1 / (sec)
            str = "FPS : %0.1f" % frame_per_sec
            cv2.putText(self.frame1, str, (1, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            cv2.putText(self.frame2, str, (1, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            
            # make table
            tableMat = table(state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer)
            table(state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer)
            
            totalFrame = cv2.hconcat([self.frame2, self.frame1])    # hconcat : 가로 방향 합치기(높이가 같아야 함)
            totalFrame = cv2.resize(totalFrame, dsize=(1920, 700)) # 1.5배 늘림
            totalShow = cv2.vconcat([totalFrame, tableMat])         # vconcat : 세로 방향 합치기(폭이 같아야 함)
            cv2.imshow("Capstone", totalShow) # 합쳐진 frame (좌표 설정하면 안되더라)
    
    def stop(self):
        self.stopped = True