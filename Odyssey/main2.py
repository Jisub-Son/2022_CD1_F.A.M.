from utils import *             
from threadingCam import *
import cv2
import mediapipe as mp
from datetime import datetime
from exercise import *
from guide import *
from time import sleep

# initialize variables
class stateInfo:
    def __init__(self):        
        self.mode = 'Choose'
        self.reps = 0                        
        self.status = 'Up'                   
        self.sets = 0                        
        self.feedback = 'start exercise'     
        self.timer = REF_TIMER

# drawing skeleton        
def draw(frame, results):
    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,                     # landmark 좌표
        mp_pose.POSE_CONNECTIONS,                   # landmark 구현
        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2), # keypoint 연결선 -> 빨간색
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5), # keypoint 원 -> 초록색 
    )

def capture(src):
    stream = cv2.VideoCapture(src)
    stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return stream

def getVideo(stream, src):
    global state_info

    (grabbed, frame) = stream.read()
    camID = src
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    frame.flags.writeable = False
    results = pose.process(frame)                  
    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # measure exercise with landmarks 
    try:    
        landmarks = results.pose_landmarks.landmark
        state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer, self.camID = EXERCISE(landmarks).calculate_exercise(
            state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer, self.camID)
    except:
        pass
    
    # draw 함수화
    draw(frame, results)
    
    # 카메라 좌우반전(운동 자세보기 편하게)
    frameBuf = cv2.flip(frame, 1)
    
    # display guide
    guide(state_info.mode, state_info.status, state_info.feedback, frameBuf, camID)
    
    return frameBuf

def showVideo(frame1, frame2, stop):
    # key input for exit, mode, reset
    key = cv2.waitKey(1) & 0xFF     # 키보드 입력
    if key == ord('q'):             # exit
        stop = True  
    elif key == ord('s'):           # squat mode
        state_info.__init__()
        state_info.mode = "squat"
        voiceFeedback('squat')
    elif key == ord('p'):           # push up mode
        state_info.__init__()
        state_info.mode = "pushup"
        voiceFeedback('pushup')
    elif key == ord('l'):           # side lateral raise mode
        state_info.__init__()
        state_info.mode = "sidelateralraise"
        voiceFeedback('sidelateralraise')
    elif key == ord('r'):           # reset
        state_info.__init__()
        state_info.feedback = "choose exercise"
        voiceFeedback('reset')
        
    # make table
    tableMat = table(state_info.mode, state_info.reps, state_info.status, state_info.sets, state_info.feedback, state_info.timer)
    totalFrame = cv2.hconcat([frame1, frame2])    # hconcat : 가로 방향 합치기(높이가 같아야 함)
    totalShow = cv2.vconcat([totalFrame, tableMat])         # vconcat : 세로 방향 합치기(폭이 같아야 함)
    cv2.imshow("totalShow", totalShow) # 합쳐진 frame
    # cv2.moveWindow("totalShow", 0, 0) # 좌표 설정
    
    return stop

# ---------------------- main function -------------------------- #

now = datetime.now()
print("Main start: ", now.strftime('%Y-%m-%d %H:%M:%S')) # 현재 시간 출력(오디세이 로그 확인용)

state_info = stateInfo()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

stop = False

stream1 = capture(src=0)
stream2 = capture(src=2)

prevTime = 0

with mp_pose.Pose(model_complexity=0,
                smooth_landmarks=True,
                smooth_segmentation=True,
                min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                min_tracking_confidence=0.5) as pose:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5    

    while not stop:
        frame1 = getVideo(stream1, 0)
        
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        print("getVideo0 : {:.03f} ms".format(sec*10**3))
        
        frame2 = getVideo(stream2, 2)
        
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        print("getVideo1 : {:.03f} ms".format(sec*10**3))
        
        stop = showVideo(frame1, frame2, stop)
        
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        print("showVideo : {:.03f} ms".format(sec*10**3))