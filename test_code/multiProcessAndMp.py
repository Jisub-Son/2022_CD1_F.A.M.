from multiprocessing import Process, Pipe
from multiprocessing import current_process
import cv2
from datetime import datetime
import mediapipe as mp
import time

LEFT_CAM = 1
RIGHT_CAM = 0

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
    def __init__(self, src, getPipe_child):
        Process.__init__(self, daemon=True)
        self.src = src
        self.getPipe_child = getPipe_child
        self.stream = None
        self.grabbed = False
        self.frame = None
        self.stopped = False
        
    def run(self):
        self.get()
        
    def get(self):
        print('pid :', current_process().pid, 'get start')
        
        self.stream = cv2.VideoCapture(self.src)
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
                    print(current_process().pid,'mp.process : {:.03f}'.format(sec*10**3))
                    
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

#######################################################

if __name__ == '__main__':
    print('main start')
    getPipe_child0, getPipe_parent0 = Pipe()
    getPipe_child1, getPipe_parent1 = Pipe()
    showPipe_child, showPipe_parent = Pipe()
    # ctrlPipe_child, ctrlPipe_parent = Pipe()
    
    proc_get0 = GetVideo(LEFT_CAM, getPipe_child0)
    proc_get1 = GetVideo(RIGHT_CAM, getPipe_child1)
    proc_get0.start()
    proc_get1.start()
    print('main : proc_get start')
    
    '''while not (getPipe_parent.poll() == True):
        print('waiting')
        time.sleep(3)'''
    
    if getPipe_parent0.recv() == 'show start' and getPipe_parent1.recv() == 'show start':
        print('ok')
    
    proc_show = ShowVideo(showPipe_child)
    proc_show.start()
    print('main : proc_show start')
    
    while True:
        frame0 = getPipe_parent0.recv()
        frame1 = getPipe_parent1.recv()
        print("bbbb")
        if (proc_show.is_alive() == True) and (showPipe_parent.poll() == False):
            showPipe_parent.send([frame0, frame1])
        else:
            print(showPipe_parent.recv())
            break
        
    '''while proc_show.is_alive():
    showPipe_parent.send([getPipe_parent0.recv(), getPipe_parent1.recv()])'''
    
    print('main end')