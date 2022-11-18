from multiprocessing import Process, Queue, Pipe
from multiprocessing import current_process, parent_process
import cv2
from datetime import datetime
import mediapipe as mp
import time

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
    def __init__(self, src, childPipe):
        Process.__init__(self, daemon=True)
        self.src = src
        self.childPipe = childPipe
        self.frame = None
        self.stopped = False
    
    def run(self):
        self.get()
    
    def get(self):
        print('pid : ', current_process().pid, 'get Video frame')
        
        self.stream = cv2.VideoCapture(self.src)
        (self.grabbed, self.frame) = self.stream.read()
        print('pid : ', current_process().pid, 'captured', self.src)
        
        now = datetime.now()
        print('pid : ', current_process().pid, 'run get func', now.strftime('%Y-%m-%d %H:%M:%S'))
        
        with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                    min_tracking_confidence=0.5) as pose:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5    
            
            while not self.stopped:
                if not self.grabbed:
                    self.stop()
                else:
                    (self.grabbed, self.frame) = self.stream.read()
                    
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # OpenCV에서는 BGR 순서로 저장/RGB로 바꿔야 제대로 표시
                    self.frame.flags.writeable = False
                    results = pose.process(self.frame)                   # landmark 구현
                    self.frame.flags.writeable = True
                    self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)  # 원본 frame의 배열 RGB를 BGR로 변경
                            
                    # draw 함수화
                    draw(self.frame, results)
                    
                    self.childPipe.send(self.frame)
                                    
        self.childPipe.close()
        print("getVideo end")
    
    def stop(self):
        self.stopped = True

class ShowVideo(Process):
    def __init__(self, frame0, frame1):
        Process.__init__(self, daemon=True)
        self.frame0 = frame0
        self.frame1 = frame1
    
    def run(self):
        self.show()
        
    def show(self):
        print('pid : ', current_process().pid, 'show Video frame')

if __name__ == '__main__':
    print("main start")
    parnetPipe0, childPipe0 = Pipe()
    parnetPipe1, childPipe1 = Pipe()
    
    proc_get1 = GetVideo(2, childPipe1)
    proc_get0 = GetVideo(0, childPipe0)
    proc_show = ShowVideo(proc_get0.frame, proc_get1.frame)
    
    proc_get1.start()
    proc_get0.start()
    proc_show.start()
    
    prevTime = 0
    
    while True:
        frame0 = parnetPipe0.recv()
        frame1 = parnetPipe1.recv()
        
        proc_show.frame0 = frame0
        proc_show.frame1 = frame1
        
        # put txt: fps
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        frame_per_sec = 1 / (sec)
        str = "FPS : %0.1f" % frame_per_sec
        cv2.putText(frame0, str, (1, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.putText(frame1, str, (1, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
            
        cv2.imshow('proc0', frame0)
        cv2.imshow('proc1', frame1)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    print("main end")