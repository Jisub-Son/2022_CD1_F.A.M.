from multiprocessing import Pipe, shared_memory
from multiprocessing import current_process
from datetime import datetime
from threadingCam2 import GetVideo
from threadingCam2 import ShowVideo
import cv2
import time

LEFT_CAM = 1
RIGHT_CAM = 2

if __name__ == '__main__':
    now = datetime.now()
    print("Main start: ", now.strftime('%Y-%m-%d %H:%M:%S')) # 현재 시간 출력(오디세이 로그 확인용)

    getPipe_child0, getPipe_parent0 = Pipe()
    getPipe_child1, getPipe_parent1 = Pipe()
    showPipe_child, showPipe_parent = Pipe()
    # ctrlPipe_child, ctrlPipe_parent = Pipe()
    shm = shared_memory.SharedMemory(create=True, size=100)
    shmBuf = shm.buf
    print('buf created') 
    
        
    proc_get0 = GetVideo(LEFT_CAM, getPipe_child0)
    proc_get1 = GetVideo(RIGHT_CAM, getPipe_child1)
    proc_get0.start()
    proc_get1.start()
    print('main : proc_get start')

    if getPipe_parent0.recv() == 'show start' and getPipe_parent1.recv() == 'show start':
        print('ok')

    # proc_show = ShowVideo(showPipe_child)
    # proc_show.start()
    # print('main : proc_show start')

    prevTime = 0

    while True:
        frame0 = getPipe_parent0.recv()
        frame1 = getPipe_parent1.recv()
        
        # if (proc_show.is_alive() == True) and (showPipe_parent.poll() == False):
        #     showPipe_parent.send([frame0, frame1])
        # else:
        #     print(showPipe_parent.recv())
        #     break
        
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        frame_per_sec = 1 / (sec)
        str = "FPS : %0.1f" % frame_per_sec
        cv2.putText(frame0, str, (1, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.putText(frame1, str, (1, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        
        cv2.imshow('proc_show0', frame0)
        cv2.imshow('proc_show1', frame1)
        
        if cv2.waitKey(1) == ord('q'):
            break
            

    print('main : end')