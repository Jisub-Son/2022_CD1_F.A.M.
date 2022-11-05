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
    
# 11-05 진행 상황 공유
# threadingCam.py
# -> line 67 : 높이와 폭 설정을 해야 함, imshow 에러나 timeout이 발생하면 여기서 사이즈를 줄일 것
# -> line 185 : print으로 디버깅 해봐서 2개 프레임이 모두 같은 사이즈인지 확인할 것, 다르면 concat 에러 뜸
# -> line 235 : 주석 처리함
# -> line 240 : 주석 처리함
# -> line 249 : hconcat은 가로 방향, vconcat은 세로 방향 합치기 사이즈에 유의할 것

# utils.py
# line 13 : 다들 카메라가 다르니 카메라 인덱스 자기꺼에 맞는지 확인하기
# line 17 : 경로 문제, 윈도우는 역슬래쉬(\), 리눅스는 슬래쉬(/)로 경로를 입력해야 함
# line 138 : resize 함수는 vconcat을 위해 사이즈를 조정하는 것, Mat 타입의 table을 반환하게끔 만들었음

# 위 진행상황들은 라즈베리에서도 돌아가는 걸 확인했으니 오디세이에서도 돼야 함