import cv2
import time
from multiprocessing import Pipe
from datetime import datetime
from threadingCam3 import GetVideo, ShowVideo, stateInfo
from exercise3 import MEASURE
from utils import LEFT_CAM, RIGHT_CAM

if __name__ == '__main__':
    now = datetime.now()
    print("Main start: ", now.strftime('%Y-%m-%d %H:%M:%S'))

    # make pipe
    getPipe_child0, getPipe_parent0 = Pipe()
    getPipe_child1, getPipe_parent1 = Pipe()
    statePipe_show0, statePipe_get0 = Pipe()
    statePipe_show1, statePipe_get1 = Pipe()

    # set GetVideo process
    proc_get0 = GetVideo(LEFT_CAM, getPipe_child0, statePipe_get0)
    proc_get1 = GetVideo(RIGHT_CAM, getPipe_child1, statePipe_get1)
    proc_get0.start()
    proc_get1.start()
    print('main : proc_get start')

    # wait for all camera setted
    if (getPipe_parent0.recv() == 'show start') and (getPipe_parent1.recv() == 'show start'):
        print('main : received show start')

    # init state
    state_info = stateInfo()
    
    # set ShowVideo
    frame0 = getPipe_parent0.recv()
    frame1 = getPipe_parent1.recv()
    show_video = ShowVideo(frame0, frame1, state_info)
    print('main : show_video start')

    prev = 0

    # main loop
    while (proc_get0.is_alive() and proc_get1.is_alive and show_video.stopped == False):
        # send state
        getPipe_parent0.send('state')
        getPipe_parent1.send('state')
        getPipe_parent0.send([state_info.mode, state_info.status, state_info.feedback])
        getPipe_parent1.send([state_info.mode, state_info.status, state_info.feedback])
        
        # receive frame
        frame0, angle_list0 = getPipe_parent0.recv()
        frame1, angle_list1 = getPipe_parent1.recv()
        
        # mesaure exercise
        state_info = MEASURE(angle_list0, angle_list1, state_info).calculate_exercise()
        
        # set show video variable
        show_video.frame0 = frame0
        show_video.frame1 = frame1
        show_video.state_info = state_info
        
        # calculate fps
        cur = time.time()
        sec = cur - prev
        prev = cur
        fps = 1 / sec
        str = 'FPS : %0.1f' % fps
        cv2.putText(frame0, str, (1, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        
        # do show function
        show_video.show()
        
        # update state
        state_info = show_video.state_info
        
    show_video.stop()
    cv2.destroyAllWindows()
    print('main : end')
    
    
# 12월 4일 진행 상황
# main_dir에 main3.py threadingCam3.py exercise3.py 3개 업로드
# 멀티 프로세싱 적용 -> 데탑에서는 구동에는 문제 없었음(30fps 이상)
#                    -> 노트북에서도 구동에는 문제 없었음(10~12fps)
#
# main3.py : 오디세이에서 바꿔야할 거 없을 듯, 그대로 복사
# threadingCam3.py : 159줄 밑으로 풀스크린 관련 구문 주석처리되어 있음. 오디세이에서는 주석 해제. 나머진 그대로 복사
# exercise3.py : 라스트 기준값들이 오디세이에만 있음 -> 기준값 변경
#                로그 파일 관련 주석처리되어 있음 -> 주석 해제
# guide.py : import 구문만 바뀜 -> 오디세이 파일에도 변경하길 바람(사소한 차이이긴 하나 필요한 것만 import)
# keypoint.py : import 구문만 바뀜 -> 오디세이 파일에도 변경하길 바람(사소한 차이이긴 하나 필요한 것만 import)
# utils.py : 오디세이에 있는거 그대로 쓰면 됨
# 그 외 세부 코드 설명은 일단 생략
#
# runningtime 테스트 : threadingCam3.py line 93 주석 해제해서 런닝 타임 비교
# 오디세이 폴더 기준 main, main2, main3의 런닝타임 비교 바람
# 라이브러리 수정 전, 후 런닝타임 비교 바람
