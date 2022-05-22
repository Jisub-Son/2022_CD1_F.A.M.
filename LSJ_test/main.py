import cv2                      # opencv import        
import argparse                 # 실행 인자 추가, 이거 필요없을 것 같은데 뺄 수 있음 빼자 
import mediapipe as mp          # 스켈레톤 구현 
from utils import *             # utils
from keypoint import KEYPOINT   # keypoint 불러오기
from exercise import EXERCISE   # exercise 불러오기
import threading

# argparse setting
ap = argparse.ArgumentParser()  # argparse 설정 python main.py -mode squat 로 실행가능
ap.add_argument("-mode",
                "--exercise",
                type=str,
                help='activity',
                required=True)
args = vars(ap.parse_args())

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)
        
def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    capture = cv2.VideoCapture(camID)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 400) # 가로
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300) # 세로  
   
 # mediapipe setting
 # 스켈레톤 구현
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    with mp_pose.Pose(min_detection_confidence=0.5, ## 최소감지신뢰값([0.0, 1.0]) 기본값=0.5 설정
                  min_tracking_confidence=0.5) as pose: ## 최소추적신뢰값([0.0, 1.0]) 기본값=0.5 설정
    
     reps = 0                        # rep 수 초기화
     status = 'Up'                   # 운동 상태 초기화    
     sets = 0                        # set 수 초기화
     feedback = 'start exercise'     # feedback 초기화 : 운동 시작 전
     timer = 5                       # timer 초기화(임시로 5초 설정)
    
     while capture.isOpened():
        reval, frame = capture.read() # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret == True
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV에서는 BGR 순서로 저장/RGB로 바꿔야 제대로 표시
        frame.flags.writeable = False
        results = pose.process(frame)   # 스켈레톤 구현
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # 원본 frame의 배열 RGB를 BGR로 변경
        
        try:    # 스켈레톤을 통해 운동횟수 계산
            landmarks = results.pose_landmarks.landmark
            reps, status, sets, feedback, timer, camID = EXERCISE(landmarks).calculate_exercise(
                args["exercise"], reps, status, sets, feedback, timer, camID)
        except:
            pass
        
        table(args["exercise"], reps, status, sets, feedback, timer, camID)    # 테이블 내용 표시

        # 랜드마크 감지/출력
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,     # 랜드마크 좌표
            mp_pose.POSE_CONNECTIONS,   # 스켈레톤 구현
            mp_drawing.DrawingSpec(color=(0, 0, 255),   # keypoint 연결 빨간색
                                   thickness=2, 
                                   circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 255, 0),   # keypoint 원 초록색
                                   thickness=5,
                                   circle_radius=5),
        )
        
        frame = cv2.flip(frame, 1)  # 카메라 좌우반전(운동 자세보기 편하게)
        cv2.imshow(previewName, frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    capture.release()       # 캡쳐 객체를 없애줌   
    cv2.destroyWindow(previewName)

thread1 = camThread("Camera 0", 0)
thread2 = camThread("Camera 1", 1)
thread1.start()
thread2.start() 