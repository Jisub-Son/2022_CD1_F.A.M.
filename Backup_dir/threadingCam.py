import cv2
import mediapipe as mp
import threading
from utils import *
from exercise import EXERCISE
import time

# initialize variables
def initState():        
    reps = 0                        
    status = 'Up'                   
    sets = 0                        
    feedback = 'start exercise'     
    timer = REF_TIMER               
    return [reps, status, sets, feedback, timer]

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
                
                # 카메라 좌우반전(운동 자세보기 편하게)
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
                str = "camID : {} ".format(camID) + "FPS : %0.2f" % real_fps
                cv2.putText(frame, str, (1,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                
                # put window
                if camID == 0:
                    cv2.imshow(previewName, frame)
                    cv2.moveWindow(previewName, 0, 0)   # 좌표 설정
                elif camID == 1:
                    cv2.imshow(previewName, frame) 
                    cv2.moveWindow(previewName, 640, 0) # 좌표 설정
                
            capture.release()               # 캡쳐 객체를 없애줌
            cv2.destroyAllWindows(camID)    # 모든 영상 창을 닫아줌