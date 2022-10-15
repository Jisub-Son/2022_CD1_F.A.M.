import cv2
import mediapipe as mp
import threading
from keypoint import *
from utils import *
from exercise import *
import time
import numpy as np

# initialize variables
def initState():        
    reps = 0                        
    status = 'Up'                   
    sets = 0                        
    feedback = 'start exercise'     
    timer = REF_TIMER               
    return [reps, status, sets, feedback, timer]           
 
 # display shadow partner
def shadow(file, frame, camID, r, c): 
    file_inv = cv2.flip(file, 1) ## 좌우반전
    if file is None:
        print('image load failed!')
    # logo with frame0   
    rows, cols, channels = file.shape ## 로고 픽셀값
    roi = frame[r:rows + r, c:cols + c] ## 로고를 필셀값 ROI(관심영역)
    gray = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY) ## 로고를 gray로 변환
    ret, mask = cv2.threshold(gray, 97, 255, cv2.THRESH_BINARY) ## 이진영상으로 변환 (흰색배경, 검정로고)
    mask_inv = cv2.bitwise_not(mask) ## mask 반전
    background = cv2.bitwise_and(roi, roi, mask = mask) ## 캠화면에 넣을 위치 black
    shadowpartner = cv2.bitwise_and(file, file, mask = mask_inv) ## 로고에서 캠화면에 출력할 부분
    final0 = cv2.bitwise_or(background, shadowpartner) ## 캠화면의 검정부분과 로고 출력부분 합성
    # logo with frame1
    rows, cols, channels = file_inv.shape ## 로고 픽셀값
    roi = frame[r:rows + r, c:cols + c] ## 로고를 필셀값 ROI(관심영역)
    gray = cv2.cvtColor(file_inv, cv2.COLOR_BGR2GRAY) ## 로고를 gray로 변환
    ret, mask = cv2.threshold(gray, 97, 255, cv2.THRESH_BINARY) ## 이진영상으로 변환 (흰색배경, 검정로고)
    mask_inv = cv2.bitwise_not(mask) ## mask 반전
    background = cv2.bitwise_and(roi, roi, mask = mask) ## 캠화면에 넣을 위치 black
    shadowpartner = cv2.bitwise_and(file_inv, file_inv, mask = mask_inv) ## 로고에서 캠화면에 출력할 부분
    final1 = cv2.bitwise_or(background, shadowpartner) ## 캠화면의 검정부분과 로고 출력부분 합성
    # display shadowpartner
    if camID == 0: 
        frame[r:rows + r, c:cols + c] = final0 ## 캠화면에 실시간으로 출력하기 위해 합성 
    elif camID == 1: ## cam1 에는 flip된 영상 출력         
        frame[r:rows + r, c:cols + c] = final1   
                              
# class for thread
class camThread(threading.Thread):
    def __init__(self, previewName, camID, args):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.args = args
        
    def run(self):
        print("Starting " + self.previewName)
        self.camPreview(self.previewName, self.camID, self.args)
            
    # camPreview makes opencv windows with mediapipe    
    def camPreview(self, previewName, camID, args):
        cv2.namedWindow(previewName)
        
        # video setting
        capture = cv2.VideoCapture(camID, cv2.CAP_DSHOW)
        # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # mediapipe setting
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        with mp_pose.Pose(min_detection_confidence=0.5,         # 최소감지신뢰값( [0.0, 1.0] ) 기본값 = 0.5
                        min_tracking_confidence=0.5) as pose:   # 최소추적신뢰값( [0.0, 1.0] ) 기본값 = 0.5
            
            # init variables
            reps, status, sets, feedback, timer = initState()       
            
            squat_down = 1 ## 초기화
            squat_up = 51
            pushup_down = 1
            pushup_up = 60
            sidelateralraise_up = 1
            sidelateralraise_down = 35
 
            # open opencv window
            while capture.isOpened():              
                
                # key input for exit, mode, reset
                key = cv2.waitKey(1) & 0xFF     # 키보드 입력
                if key == ord('q'):             # exit
                    break   
                elif key == ord('s'):           # squat mode
                    args["exercise"] = "squat"
                    reps, status, sets, feedback, timer = initState()
                elif key == ord('p'):           # pushup mode
                    args["exercise"] = "pushup"
                    reps, status, sets, feedback, timer = initState()
                elif key == ord('l'):           # sidelateralraise mode
                    args["exercise"] = "sidelateralraise"
                    reps, status, sets, feedback, timer = initState()    
                elif key == ord('r'):           # reset
                    status = 'Up'
                    reps, status, sets, feedback, timer = initState()
                
                ret, frame = capture.read()     # 카메라로부터 영상을 받아 frame에 저장, 잘 받았다면 ret == True
                if not ret:                                     # frame을 못받았을 경우
                    print("Ignoring empty camera frame\r\n")
                    continue
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV에서는 BGR 순서로 저장/RGB로 바꿔야 제대로 표시
                frame.flags.writeable = False
                results = pose.process(frame)                   # landmark 구현
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # 원본 frame의 배열 RGB를 BGR로 변경
                
                # measure exervise with landmarks
                try:    
                    landmarks = results.pose_landmarks.landmark
                    reps, status, sets, feedback, timer, camID = EXERCISE(landmarks).calculate_exercise(
                        args["exercise"], reps, status, sets, feedback, timer, camID)
                except:
                    pass
                
                # #landmark data 저장(마지막 프레임 데이터만)
                # if camID == 0:                  
                #     data = detections(landmarks=landmarks)
                #     data.to_csv("./data.csv")
                
                # make table
                if camID == 0:
                    table(args["exercise"], reps, status, sets, feedback, timer)
                  
                # landmark detection and output
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,                     # landmark 좌표
                    mp_pose.POSE_CONNECTIONS,                   # landmark 구현
                    mp_drawing.DrawingSpec(color=(0, 0, 255),   # keypoint 연결선 -> 빨간색
                                        thickness=2, 
                                        circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 255, 0),   # keypoint 원 -> 초록색
                                        thickness=5,
                                        circle_radius=5),
                )
                
                # 카메라 좌우반전(운동 자세 보기 편하게)
                frame = cv2.flip(frame, 1)
                        
                # calculate fps
                fps = capture.get(cv2.CAP_PROP_FPS)
                # print('fps',fps)
                if fps == 0.0:
                    fps = 30.0
                time_per_frame_video = 1/fps
                last_time = time.perf_counter()
                time_per_frame = time.perf_counter() - last_time
                time_sleep_frame = max(0,time_per_frame_video - time_per_frame)
                time.sleep(time_sleep_frame)
                real_fps = 1/(time.perf_counter()-last_time)
                last_time = time.perf_counter()
                str_fps = "camID : {} ".format(camID) + "FPS : %0.2f" % real_fps
                cv2.putText(frame, str_fps, (1,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
                
                # display shadow partner
                # squat
                if (args["exercise"] == "squat" and status == 'Up' and feedback == 'Start'): ## squat에서 서 있을 때(앉아야할 때) -> 서서 앉을 때까지만 출력
                    down = cv2.imread('squat\squat_' + str(squat_down) +'.jpg') ## 1번부터 읽기
                    file = cv2.resize(down, dsize = (0, 0), fx = 1.15, fy = 1.15) ## 크기 조절
                    squat_down += 1 ## 증가     
                    if squat_down == 50: ## 범위 넘어가면
                        squat_down = 1  ## 초기화        
                    shadow(file, frame, camID, 20, 240) ## 가이드 불러오기
                else:
                    squat_down = 1  ## 초기화    
                if (args["exercise"] == "squat" and status == 'Down' and feedback == 'Success'): ## squat에서 서 있을 때(앉아야할 때) -> 서서 앉을 때까지만 출력
                    up = cv2.imread('squat\squat_' + str(squat_up) +'.jpg') ## 1번부터 읽기
                    file = cv2.resize(up, dsize = (0, 0), fx = 1.15, fy = 1.15) ## 크기 조절
                    squat_up += 1 ## 증가     
                    if squat_up == 65: ## 범위 넘어가면
                        squat_up = 51  ## 초기화      
                    shadow(file, frame, camID, 20, 240) ## 가이드 불러오기
                else:                          
                    squat_up = 51  ## 초기화 
                # pushup    
                if (args["exercise"] == "pushup" and status == 'Up' and feedback == 'Start'): ## 푸쉬업에서 올라가있을때(내려가야함) -> 내려가는거까지만 출력
                    down = cv2.imread('pushup\pushup_' + str(pushup_down) +'.jpg') ## 1번부터 읽기
                    down_flip = cv2.flip(down, 1) ## 좌우반전(실수로 반대로 찍음)
                    file = cv2.resize(down_flip, dsize = (0, 0), fx = 1.5, fy = 1.5) ## 크기 조절
                    pushup_down += 1 ## 증가    
                    if pushup_down == 59: ## 범위 넘어가면
                        pushup_down = 1 ## 초기화     
                    shadow(file, frame, camID, 150, 100) ## 가이드 불러오기
                else:
                    pushup_down = 1  ## 초기화
                if (args["exercise"] == "pushup" and status == 'Down' and feedback == 'Success'):  ## 푸쉬업에서 내려가있을때(올라가야함) -> 올라가는거까지만 출력
                    up = cv2.imread('pushup\pushup_' + str(pushup_up) +'.jpg')
                    up_flip = cv2.flip(up, 1) ## 좌우반전(실수로 반대로 찍음)
                    file = cv2.resize(up_flip, dsize = (0, 0), fx = 1.5, fy = 1.5) ## 크기 조절
                    pushup_up += 1 ## 증가     
                    if pushup_up == 69: ## 범위 넘어가면
                        pushup_up = 60  ## 초기화        
                    shadow(file, frame, camID, 150, 100)
                else:
                    pushup_up = 60  ## 초기화         
                # side lateral raise
                if (args["exercise"] == "sidelateralraise" and status == 'Down' and feedback == 'Start'): ## 사레레에서 내려가있을때(팔올려야함) -> 올라가는거까지만 출력
                    down = cv2.imread('sidelateralraise\sidelateralraise_' + str(sidelateralraise_up) +'.jpg') ## 1번부터 읽기
                    file = cv2.resize(down, dsize = (0, 0), fx = 1.2, fy = 1.2) ## 크기 조절
                    sidelateralraise_up += 1 ## 증가     
                    if sidelateralraise_up == 35: ## 범위 넘어가면
                        sidelateralraise_up = 1  ## 초기화        
                    shadow(file, frame, camID, 20, 150)
                else:
                    sidelateralraise_up = 1  ## 초기화    
                if (args["exercise"] == "sidelateralraise" and status == 'Up' and feedback == 'Success'): ## 사레레에서 올라가있을때(팔내려야함) -> 내려가는거까지만 출력
                    up = cv2.imread('sidelateralraise\sidelateralraise_' + str(sidelateralraise_down) +'.jpg') ## 1번부터 읽기
                    file = cv2.resize(up, dsize = (0, 0), fx = 1.2, fy = 1.2) ## 크기 조절
                    sidelateralraise_down += 1 ## 증가     
                    if sidelateralraise_down == 63: ## 범위 넘어가면
                        sidelateralraise_down = 35  ## 초기화      
                    shadow(file, frame, camID, 20, 150)
                else:                          
                    sidelateralraise_down = 35  ## 초기화    
                
                # put window
                if camID == 0:
                    cv2.imshow(previewName, frame)
                    cv2.moveWindow(previewName, 0, 0)   # 좌표 설정
                elif camID == 1:
                    cv2.imshow(previewName, frame) 
                    cv2.moveWindow(previewName, 640, 0) # 좌표 설정
                
            capture.release()               # 캡쳐 객체를 없애줌
            cv2.destroyAllWindows(camID)    # 모든 영상 창을 닫아줌