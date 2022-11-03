import argparse                 
from utils import *             
from threadingCam import *

# argparse setting
"""ap = argparse.ArgumentParser()  # python main.py -mode squat 로 실행가능
ap.add_argument("-mode", "--exercise", type=str, help='activity', required=True)
args = vars(ap.parse_args())"""

threadBoth(0, 1)