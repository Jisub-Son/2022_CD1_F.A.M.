from multiprocessing import Process, Queue, Pipe
from multiprocessing import current_process, parent_process
import cv2
from datetime import datetime
import mediapipe
import time

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
def getVideo(src, childPipe):
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
    print("getVideo end")

# showVideo func
def showVideo(frameQueue):
    print("show Video frame")
    
    while True:
        frame = frameQueue.get()
        cv2.imshow('video', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()
    
    print("showVideo end")

# getVideo class using pipe
# class GetVideo(Process):
#     def __init__(self, src, childPipe):
#         Process.__init__(self, daemon=True)
#         self.src = src
#         self.childPipe = childPipe
    
#     def run(self):
#         self.get()
    
#     def get(self):
#         print('pid : ', current_process().pid, 'get Video frame')
        
#         cap = cv2.VideoCapture(self.src)
#         print('pid : ', current_process().pid, 'captured', self.src)
        
#         now = datetime.now()
#         print('pid : ', current_process().pid, 'start video', now.strftime('%Y-%m-%d %H:%M:%S'))
        
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 print("Can't receive frame (stream end?). Exiting ...")
#                 break
            
#             self.childPipe.send(frame)
        
#         self.childPipe.close()
        # print("getVideo end")

class GetVideo(Process):
    def __init__(self, src, childPipe):
        Process.__init__(self, daemon=True)
        # print('pid : ', current_process().pid, 'get Video class init')
        self.src = src
        self.childPipe = childPipe
        self.frame = None
        # self.stream = cv2.VideoCapture(src)
        # print('pid : ', current_process().pid, 'captured', self.src)
        # (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    
    def run(self):
        # Process(target=self.get, args=(), daemon=True)
        # return self
        self.get()
    
    def get(self):
        print('pid : ', current_process().pid, 'get Video frame')
        
        self.stream = cv2.VideoCapture(self.src)
        (self.grabbed, self.frame) = self.stream.read()
        print('pid : ', current_process().pid, 'captured', self.src)

        now = datetime.now()
        print('pid : ', current_process().pid, 'run get func', now.strftime('%Y-%m-%d %H:%M:%S'))
        
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                
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
        
        while True:
            cv2.imshow('proc0_show', self.frame0)
            cv2.imshow('proc1_show', self.frame1)

            if cv2.waitKey(1) == ord('q'):
                break

if __name__ == '__main__':
    print("main start")
    # frameQueue0 = Queue()
    # frameQueue1 = Queue()
    parnetPipe0, childPipe0 = Pipe()
    parnetPipe1, childPipe1 = Pipe()
    # proc_get0 = Process(target=getVideo, args=(0, frameQueue0, frameQueue1), daemon=True)
    # proc_get1 = Process(target=getVideo, args=(1, frameQueue1, frameQueue0), daemon=True)
    # proc_get0 = Process(target=getVideo, args=(0, childPipe0), daemon=True)
    # proc_get1 = Process(target=getVideo, args=(1, childPipe1), daemon=True)
    # proc_show = Process(target=showVideo, args=(frameQueue, ), deamon=True)
    
    proc_get1 = GetVideo(1, childPipe1)
    proc_get0 = GetVideo(0, childPipe0)
    proc_show = ShowVideo(proc_get0.frame, proc_get1.frame)
    
    proc_get1.start()
    proc_get0.start()
    proc_show.start()
    
    while True:
        # frame0 = frameQueue0.get()
        # frame1 = frameQueue1.get()
        frame0 = parnetPipe0.recv()
        frame1 = parnetPipe1.recv()
        
        proc_show.frame0 = frame0
        proc_show.frame1 = frame1
        
        cv2.imshow('proc0', frame0)
        cv2.imshow('proc1', frame1)

        if cv2.waitKey(1) == ord('q'):
            break
    
    print("main end")