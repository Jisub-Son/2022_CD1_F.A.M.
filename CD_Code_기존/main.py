import argparse                 
from utils import *             
from threadingCam import *

# argparse setting
ap = argparse.ArgumentParser()  # python main.py -mode squat 로 실행가능
ap.add_argument("-mode",
                "--exercise",
                type=str,
                help='activity',
                required=True)
args = vars(ap.parse_args())

# Create two threads as follows
thread1 = camThread("Camera 0", 0, args) ## 노트북 cam
thread2 = camThread("Camera 1", 1, args) ## usb cam
thread1.start()
thread2.start()