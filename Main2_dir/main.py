# 
# 2022-1 CD1 Team-1
# Project Name  : F.A.M.(Fitness Assistant Module)
# Member        : 손지섭(팀장), 강태영, 이석진, 정홍택
# 
    
import argparse                 
from utils import *             
from threadingCam import camThread

# argparse setting
ap = argparse.ArgumentParser()  # python main.py -mode squat 로 실행가능
ap.add_argument("-mode",
                "--exercise",
                type=str,
                help='activity',
                required=True)
args = vars(ap.parse_args())

# Create two threads as follows
thread1 = camThread("Camera 0", 0, args)
thread2 = camThread("Camera 1", 1, args)
thread1.start()
thread2.start()