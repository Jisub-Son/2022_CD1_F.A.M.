import cv2
import mediapipe as mp
from multiprocessing import Process, shared_memory
from multiprocessing import current_process
from utils import REF_TIMER
from utils import voiceFeedback
from utils import table
from exercise2 import EXERCISE
from guide import guide
from datetime import datetime
import time
from sys import getsizeof
import numpy as np

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

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw(frame, results):
    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,                     # landmark 좌표
        mp_pose.POSE_CONNECTIONS,                   # landmark 구현
        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2), # keypoint 연결선 -> 빨간색
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5), # keypoint 원 -> 초록색 
    )

class GetVideo(Process):
    def __init__(self, src, getPipe_child, shm):
        Process.__init__(self, daemon=True)
        self.src = src
        self.getPipe_child = getPipe_child
        self.shm = shared_memory.SharedMemory(shm)
        self.stream = None
        self.grabbed = False
        self.frame = None
        self.stopped = False
        self.camID = src
        
    def run(self):
        self.get()
        
    def get(self):
        print('pid :', current_process().pid, 'get start')
        
        self.stream = cv2.VideoCapture(self.src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
        (self.grabbed, self.frame) = self.stream.read()
        
        now = datetime.now()
        print('pid :', current_process().pid, 'get loop start', now.strftime('%H:%M:%S'))
        
        self.getPipe_child.send('show start')
        
        with mp_pose.Pose(model_complexity=0,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as pose:
            
            while not self.stopped:
                if not self.grabbed:
                    self.stop()
                    print('GetVideo stopped')
                else:
                    (self.grabbed, self.frame) = self.stream.read()
                    
                    cur = time.time()
                    prev = cur
                    
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
                    self.frame.flags.writeable = False
                    results = pose.process(self.frame)                   
                    self.frame.flags.writeable = True
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)  
                    
                    cur = time.time()
                    sec = cur - prev
                    print('pid :', current_process().pid, 'mp.process : {:.03f}'.format(sec*10**3))
                    
                    print('pid :', current_process().pid, 'id :', id(results), 'size', getsizeof(results))
                    
                    results2 = np.ndarray(results, buffer=self.shm.buf)
                    print(results2)
                    
                    draw(self.frame, results)
                    
                    self.getPipe_child.send(self.frame)

        
        self.getPipe_child.close()
        print('GetVideo end')
        
    def stop(self):
        self.stopped = True

class ShowVideo(Process):
    def __init__(self, showPipe_child):
        Process.__init__(self, daemon=True)
        self.showPipe_child = showPipe_child
        self.stopped = False
        
    def run(self):
        self.show()
        
    def show(self):
        print('pid :', current_process().pid, 'show start')
        
        prevTime = 0
        
        while not self.stopped:
            frame0, frame1 = self.showPipe_child.recv()
            
            curTime = time.time()
            sec = curTime - prevTime
            prevTime = curTime
            frame_per_sec = 1 / (sec)
            str = "FPS : %0.1f" % frame_per_sec
            cv2.putText(frame0, str, (1, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
            cv2.putText(frame1, str, (1, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
            
            cv2.imshow('proc_show0', frame0)
            cv2.imshow('proc_show1', frame1)
            
            if cv2.waitKey(1) == ord('q'):
                break
        
        self.showPipe_child.send(1)
        self.showPipe_child.close()
        print('ShowVideo end')
        
    def stop(self):
        self.stopped = True