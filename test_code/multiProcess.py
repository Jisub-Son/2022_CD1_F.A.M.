from multiprocessing import Process, Pipe
from multiprocessing import current_process
import cv2
from datetime import datetime
import mediapipe as mp
import time

LEFT_CAM = 0
RIGHT_CAM = 1

# getVideo func using queue -> sync needed
'''def getVideo(src, frameQueueMain, frameQueueSub):
    print('pid : ', current_process().pid, 'get Video frame')
    
    cap = cv2.VideoCapture(src)
    print('pid : ', current_process().pid, 'captured', src)
    
    if src == 0:                                # 가라로 만든 싱크 맞추는 구문
        while not (frameQueueMain.get() == 1):  # 1번 카메라가 먼저 캡처되서 기다림
            pass
    elif src == 1:
        frameQueueSub.put(1)
    
    now = datetime.now()
    print('pid : ', current_process().pid, 'sync...', now.strftime('%Y-%m-%d %H:%M:%S'))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        frameQueueMain.put(frame)
    
    print("getVideo end")'''

# getVideo func using pipe -> sync not needed
'''def getVideo(src, childPipe):
    print('pid : ', current_process().pid, 'get Video frame')
    
    cap = cv2.VideoCapture(src)
    print('pid : ', current_process().pid, 'captured', src)
    
    now = datetime.now()
    print('pid : ', current_process().pid, 'start Video', now.strftime('%Y-%m-%d %H:%M:%S'))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        childPipe.send(frame)
    
    childPipe.close()
    print("getVideo end")'''

# showVideo func
'''def showVideo(frameQueue):
    print("show Video frame")
    
    while True:
        frame = frameQueue.get()
        cv2.imshow('video', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()
    
    print("showVideo end")'''

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
        
        while not self.stopped:
            if not self.grabbed:
                self.stop()
                print('GetVideo stopped')
            else:
                (self.grabbed, self.frame) = self.stream.read()
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
        
        while not self.stopped:
            frame0, frame1 = self.showPipe_child.recv()
            cv2.imshow('proc_show0', frame0)
            cv2.imshow('proc_show1', frame1)
            
            if cv2.waitKey(1) == ord('q'):
                break
        
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
        
        if proc_show.is_alive() == True:
            showPipe_parent.send([frame0, frame1])
        else:
            break
        
    '''while proc_show.is_alive():
    showPipe_parent.send([getPipe_parent0.recv(), getPipe_parent1.recv()])'''
    
    print('main end')