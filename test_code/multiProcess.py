from multiprocessing import Process, Queue
from multiprocessing import current_process, parent_process
import cv2
from datetime import datetime
import mediapipe
import time

def getVideo(src, frameQueueMain, frameQueueSub):
    print('pid : ', current_process().pid, 'get Video frame')
    
    cap = cv2.VideoCapture(src)
    print('pid : ', current_process().pid, 'captured', src)
    
    if src == 1:                                # 가라로 만든 싱크 맞추는 구문
        while not (frameQueueMain.get() == 1):  # 1번 카메라가 먼저 캡처되서 기다림
            pass
    elif src == 0:
        frameQueueSub.put(1)
    
    now = datetime.now()
    print('pid : ', current_process().pid, 'sync...', now.strftime('%Y-%m-%d %H:%M:%S'))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        frameQueueMain.put(frame)
    
    print("getVideo end")

def showVideo(frameQueue):
    print("show Video frame")
    
    while True:
        frame = frameQueue.get()
        cv2.imshow('video', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()
    
    print("showVideo end")

class GetVideo(Process):
    def __init__(self, src, frameQueueMain, frameQueueSub):
        Process.__init__(self, daemon=True)
        self.src = src
        self.framQueueMain = frameQueueMain
        self.framQueueSub = frameQueueSub
    
    def run(self):
        self.get()
    
    def get(self):
        print('pid : ', current_process().pid, 'get Video frame')
    
        cap = cv2.VideoCapture(self.src)
        print('pid : ', current_process().pid, 'captured', self.src)
        
        if self.src == 1:                                # 가라로 만든 싱크 맞추는 구문
            while not (self.frameQueueMain.get() == 1):  # 1번 카메라가 먼저 캡처되서 기다림
                pass
        elif self.src == 0:
            self.frameQueueSub.put(1)
        
        now = datetime.now()
        print('pid : ', current_process().pid, 'sync...', now.strftime('%Y-%m-%d %H:%M:%S'))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            self.frameQueueMain.put(frame)
    
            print("getVideo end")

if __name__ == '__main__':
    print("main start")
    frameQueue0 = Queue()
    frameQueue1 = Queue()
    # proc_get0 = Process(target=getVideo, args=(0, frameQueue0, frameQueue1), daemon=True)
    # proc_get1 = Process(target=getVideo, args=(1, frameQueue1, frameQueue0), daemon=True)
    # proc_show = Process(target=showVideo, args=(frameQueue, ), deamon=True)
    proc_get0 = GetVideo(0, frameQueue0, frameQueue1)
    proc_get1 = GetVideo(1, frameQueue1, frameQueue0)
    
    proc_get0.start()
    proc_get1.start()
    
    while True:
        frame0 = frameQueue0.get()
        frame1 = frameQueue1.get()
        
        cv2.imshow('proc0', frame0)
        cv2.imshow('proc1', frame1)

        if cv2.waitKey(1) == ord('q'):
            break
    
    print("main end")