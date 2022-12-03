import mediapipe as mp
import cv2
import time

from multiprocessing import Process
from multiprocessing import current_process
from datetime import datetime

from exercise3 import EXERCISE
from guide import guide
from utils import voiceFeedback, table
from utils import REF_TIMER

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

def draw(frame, results):
    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,                     # landmark 좌표
        mp_pose.POSE_CONNECTIONS,                   # landmark 구현
        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2), # keypoint 연결선 -> 빨간색
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5), # keypoint 원 -> 초록색 
    )

class GetVideo(Process):
    def __init__(self, src, getPipe_child, statePipe_get):
        Process.__init__(self, daemon=True)
        self.src = src
        self.getPipe_child = getPipe_child
        self.statePipe_get = statePipe_get
        self.stream = None
        self.grabbed = False
        self.frame = None
        self.stopped = False
        self.camID = src
        
    def run(self):
        self.get()
        
    def get(self):
        print('pid :', current_process().pid, 'get start')
        
        # connect to camera and get first frame
        self.stream = cv2.VideoCapture(self.src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
        (self.grabbed, self.frame) = self.stream.read()
        
        now = datetime.now()
        print('pid :', current_process().pid, 'get loop start', now.strftime('%H:%M:%S'))
        
        # send msg to start showVideo
        self.getPipe_child.send('show start')
        self.getPipe_child.send(self.frame)
        
        # open mediapipe and loop streaming
        with mp_pose.Pose(model_complexity=0,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as pose:
            
            while not self.stopped:
                if not self.grabbed:
                    self.stop()
                    print('pid :', current_process().pid, 'GetVideo stopped')
                else:
                    (self.grabbed, self.frame) = self.stream.read()
                    
                    # receive mode
                    if self.getPipe_child.recv() == 'state':
                        mode = self.getPipe_child.recv()
                    
                    cur = time.time()
                    prev = cur
                    
                    # do process function
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
                    self.frame.flags.writeable = False
                    results = pose.process(self.frame)                   
                    self.frame.flags.writeable = True
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)  
                    
                    cur = time.time()
                    sec = cur - prev
                    # print('pid :', current_process().pid, 'mp.process : {:.03f}'.format(sec*10**3))
                    
                    # measure exercise with landmarks 
                    try:    
                        landmarks = results.pose_landmarks.landmark
                        angle_list = EXERCISE(landmarks).select_mode(mode, self.camID)
                    except:
                        pass
                    
                    # draw landmarks on frame
                    draw(self.frame, results)
                    self.frame = cv2.flip(self.frame, 1)
                    
                    # display guide
                    # guide(state_info.mode, state_info.status, state_info.feedback, self.frame, self.camID)
                    
                    # send frame to main loop
                    try:
                        self.getPipe_child.send([self.frame, angle_list])
                    except:
                        self.getPipe_child.send([self.frame, []])
                    
    def stop(self):
        self.stopped = True
        

class ShowVideo:
    def __init__(self, frame0, frame1, state_info):
        self.frame0 = frame0
        self.frame1 = frame1
        self.stopped = False
        self.state_info = state_info
    
    def show(self):
        if not self.stopped:
            
            # key input for exit, mode, reset
            key = cv2.waitKey(1) & 0xFF     # 키보드 입력
            if key == ord('q'):             # exit
                self.stopped = True
            elif key == ord('s'):           # squat mode
                self.state_info.__init__()
                self.state_info.mode = "squat"
                voiceFeedback('squat')
            elif key == ord('p'):           # push up mode
                self.state_info.__init__()
                self.state_info.mode = "pushup"
                voiceFeedback('pushup')
            elif key == ord('l'):           # side lateral raise mode
                self.state_info.__init__()
                self.state_info.mode = "sidelateralraise"
                voiceFeedback('sidelateralraise')
            elif key == ord('r'):           # reset
                self.state_info.__init__()
                self.state_info.feedback = "choose exercise"
                voiceFeedback('reset')
            
            # make table
            tableMat = table(self.state_info.mode, self.state_info.reps,
                            self.state_info.status, self.state_info.sets, 
                            self.state_info.feedback, self.state_info.timer)
            
            totalFrame = cv2.hconcat([self.frame0, self.frame1])    # [right, left]
            totalFrame = cv2.resize(totalFrame, dsize=(1920, 700))
            totalShow = cv2.vconcat([totalFrame, tableMat])         # vconcat : 세로 방향 합치기(폭이 같아야 함)
            
            # cv2.namedWindow("totalShow_full", cv2.WND_PROP_FULLSCREEN)
            # cv2.moveWindow("totalShow_full", 1920-1, 1080-1)
            # cv2.setWindowProperty("totalShow_full", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("totalShow_full", totalShow)
    
    def stop(self):
        self.stopped = True