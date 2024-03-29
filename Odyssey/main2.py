# 
# 2022 CD1, CD2 Team-1
# Project Name  : F.A.M.(Fitness Assistant Module)
# Member        : 손지섭(팀장), 강태영, 이석진, 정홍택
# 

import cv2
from utils import LEFT_CAM
from utils import RIGHT_CAM
from threadingCam2 import VideoGet
from threadingCam2 import VideoShow
from datetime import datetime
from threading import active_count
import time
from multiprocessing import Pipe

now = datetime.now()
print("Main start: ", now.strftime('%Y-%m-%d %H:%M:%S')) # 현재 시간 출력(오디세이 로그 확인용)

getPipe_child0, getPipe_parent0 = Pipe()
getPipe_child1, getPipe_parent1 = Pipe()

# state_infoM = stateInfo()
video_getter0 = VideoGet(src=LEFT_CAM, getPipe_child=getPipe_child0).start()
video_getter1 = VideoGet(src=RIGHT_CAM, getPipe_child=getPipe_child1).start()
video_shower = VideoShow(frame1=video_getter0.frame, frame2=video_getter1.frame).start()

print("total thread : ", active_count()) # 총 thread 확인

prevTime = 0

while True:
    if video_getter0.stopped or video_getter1.stopped or video_shower.stopped:
        video_shower.stop()
        video_getter1.stop()
        video_getter0.stop()
        break
    
    # frame1 = getPipe_parent0.recv() 
    # frame2 = getPipe_parent1.recv() 
    
    # video_shower.frame1 = frame1
    # video_shower.frame2 = frame2
    
    video_shower.frame1 = getPipe_parent0.recv() 
    video_shower.frame2 = getPipe_parent1.recv() 
    
    # put txt: fps
    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime
    video_shower.frame_per_sec = 1 / (sec)

getPipe_child0.close()
getPipe_child1.close()
cv2.destroyAllWindows()