from utils import *             
from threadingCam import *
from threading import active_count
from time import sleep

now = datetime.now()
print("Main start: ", now.strftime('%Y-%m-%d %H:%M:%S')) # 현재 시간 출력(오디세이 로그 확인용)

# state_infoM = stateInfo()
video_getter0 = VideoGet(src=LEFT_CAM).start()
video_getter1 = VideoGet(src=RIGHT_CAM).start()
video_shower = VideoShow(frame1=video_getter0.frame, frame2=video_getter1.frame).start()

print("total thread : ", active_count()) # 총 thread 확인

# prevTime = 0

while True:
    curTime = time.time()
    if video_getter0.stopped or video_getter1.stopped or video_shower.stopped:
        video_shower.stop()
        video_getter1.stop()
        video_getter0.stop()
        break
    
    video_shower.frame1 = video_getter0.frameBuf
    video_shower.frame2 = video_getter1.frameBuf
    
    sleep(0.034)
    
    # 1초 30장 = 30 fps
    # 1 fps = 1/30 = 0.0333