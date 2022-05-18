import cv2
import argparse
import mediapipe as mp
import threading
from utils import *
from keypoint import KEYPOINT
from exercise import EXERCISE

class camThread(threading.Thread):
    def __init__(self, previewName, camID, args):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.args = args
        
    def run(self):
        print("Starting " + self.previewName)
        self.camPreview(self.previewName, self.camID, self.args)
        
    def camPreview(self, previewName, camID, args):
        cv2.namedWindow(previewName)
        
        capture = cv2.VideoCapture(camID)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
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
                ret, frame = capture.read() # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret == True
                
                if not ret:                                     # ret == False일 경우(frame을 못받았을 경우)
                    print("Ignoring empty camera frame\r\n")    # 오류 메세지 출력
                    continue
                
                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 카메라 RGB
                results = pose.process(frame)   # 스켈레톤 구현
                
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # BGR
                
                try:    # 스켈레톤을 통해 운동횟수 계산
                    landmarks = results.pose_landmarks.landmark
                    reps, status, sets, feedback, timer = EXERCISE(landmarks).calculate_exercise(
                        args["exercise"], reps, status, sets, feedback, timer)
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

                cv2.imshow(previewName, frame)  # q누르면 종료
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                
            capture.release()       # 캡쳐 객체를 없애줌
            cv2.destroyAllWindows() # 모든 영상 창을 닫아줌