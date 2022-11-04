# 
# 2022 CD1, CD2 Team-1
# Project Name  : F.A.M.(Fitness Assistant Module)
# Member        : 손지섭(팀장), 강태영, 이석진, 정홍택
# 

from utils import *             
from threadingCam import *

print("Main start")

# state_infoM = stateInfo()
video_getter0 = VideoGet(src=LEFT_CAM).start()
video_getter1 = VideoGet(src=RIGHT_CAM).start()
video_shower = VideoShow(frame1=video_getter0.frame, frame2=video_getter1.frame).start()
cps = CountsPerSec().start()

print("total thread : ", active_count())

while True:
    if video_getter0.stopped or video_getter1.stopped or video_shower.stopped:
        video_shower.stop()
        video_getter1.stop()
        video_getter0.stop()
        break

    frame1 = video_getter0.frameBuf
    frame2 = video_getter1.frameBuf                                
    frame1 = putIterationsPerSec(frame1, cps.countsPerSec())
    frame2 = putIterationsPerSec(frame2, cps.countsPerSec())    
    video_shower.frame1 = frame1
    video_shower.frame2 = frame2                                
    cps.increment()