from utils import *             
from threadingCam import *
from threading import active_count
from time import sleep

now_main = datetime.now()
print("Main start: ", now_main.strftime('%Y/%m/%d %H:%M:%S')) # 현재 시간

# state_infoM = stateInfo()
video_getter0 = VideoGet(src=LEFT_CAM).start()
video_getter1 = VideoGet(src=RIGHT_CAM).start()
video_shower = VideoShow(frame1=video_getter0.frame, frame2=video_getter1.frame).start()

print("total thread : ", active_count()) # 총 thread 확인

while True:
    if video_getter0.stopped or video_getter1.stopped or video_shower.stopped:
        video_shower.stop()
        video_getter1.stop()
        video_getter0.stop()
        break
    
    video_shower.frame1 = video_getter0.frameBuf
    video_shower.frame2 = video_getter1.frameBuf
    sleep(0.03)