from datetime import datetime
from threading import Thread
from threading import activeCount
import cv2

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
        if elapsed_time != 0: ## 0으로 나누면 float error
            return self._num_occurrences / elapsed_time

"""def putIterationsPerSec(frame, iterations_per_sec): ## 여기서 에러뜨는거 같은데?
    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame"""

class VideoGet:
    def __init__(self, src1=0, src2=0):
        self.stream1 = cv2.VideoCapture(src1)
        self.stream2 = cv2.VideoCapture(src2)
        # print("Video Get : ", src1, ", ", src2)
        (self.grabbed1, self.frame1) = self.stream1.read()
        (self.grabbed2, self.frame2) = self.stream2.read()
        self.stopped = False
        
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not (self.grabbed1 or self.grabbed2):
                self.stop()
            else:
                (self.grabbed1, self.frame1) = self.stream1.read()
                (self.grabbed2, self.frame2) = self.stream2.read()

    def stop(self):
        self.stopped = True

class VideoShow:
    def __init__(self, frame1=None, frame2=None):
        self.frame1 = frame1
        self.frame2 = frame2
        self.stopped = False
        
    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video0", self.frame1)
            cv2.imshow("Video2", self.frame2)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True
        
"""def noThreading(src1=0, src2=1):
    cap1 = cv2.VideoCapture(src1)
    cap2 = cv2.VideoCapture(src2)
    cps = CountsPerSec().start()

    while True:
        (grabbed1, frame1) = cap1.read()
        (grabbed2, frame2) = cap2.read()
        if not (grabbed1 or grabbed2) or cv2.waitKey(1) == ord("q"):
            break

        frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
        frame2 = putIterationsPerSec(frame2, cps.countsPerSec())
        cv2.imshow("Video0", frame1)
        cv2.imshow("Video1", frame2)
        cps.increment()     
# noThreading()"""
        
"""def threadVideoGet(src1=0, src2=1):
    video_getter = VideoGet(src1, src2).start()
    cps = CountsPerSec().start()
    
    print("Active Threads", activeCount())

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

        frame1 = video_getter.frame1
        frame2 = video_getter.frame2
        frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
        frame2 = putIterationsPerSec(frame2, cps.countsPerSec())
        cv2.imshow("Video0", frame1)
        cv2.imshow("Video1", frame2)
        cps.increment()
# threadVideoGet()

def threadVideoShow(src1=0, src2=1):
    cap1 = cv2.VideoCapture(src1)
    cap2 = cv2.VideoCapture(src2)
    (grabbed1, frame1) = cap1.read()
    (grabbed2, frame2) = cap2.read()
    video_shower = VideoShow(frame1, frame2).start()
    cps = CountsPerSec().start()

    while True:
        (grabbed1, frame1) = cap1.read()
        (grabbed2, frame2) = cap2.read()
        if not (grabbed1 or grabbed2) or video_shower.stopped:
            video_shower.stop()
            break

        frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
        frame2 = putIterationsPerSec(frame2, cps.countsPerSec())
        video_shower.frame1 = frame1
        video_shower.frame2 = frame2
        cps.increment()     
# threadVideoShow()"""
        
def threadBoth(src1=0, src2=1):
    video_getter = VideoGet(src1, src2).start()
    video_shower = VideoShow(frame1=video_getter.frame1, frame2=video_getter.frame2).start()
    cps = CountsPerSec().start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame1 = video_getter.frame1
        frame2 = video_getter.frame2
        ##frame1 = putIterationsPerSec(frame1, cps.countsPerSec()) ## 여기서 에러뜨는거 같은데?
        ##frame2 = putIterationsPerSec(frame2, cps.countsPerSec()) ## 여기서 에러뜨는거 같은데?
        video_shower.frame1 = frame1
        video_shower.frame2 = frame2
        cps.increment()
threadBoth()