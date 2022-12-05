import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

def draw(frame, results):
    mp_drawing.draw_landmarks(
        frame,
        results.pose_landmarks,                     # landmark ì¢Œí‘œ
        mp_pose.POSE_CONNECTIONS,                   # landmark êµ¬í˜„
        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2), # keypoint ì—°ê²°ì„  -> ë¹¨ê°„ìƒ‰
        # mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=5), # keypoint ì› -> ì´ˆë¡ìƒ‰ 
    )

with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCVì—ì„œëŠ” BGR ìˆœì„œë¡œ ì €ìž¥/RGBë¡œ ë°”ê¿”ì•¼ ì œëŒ€ë¡œ í‘œì‹œ
        image.flags.writeable = False
        results = pose.process(image)                   # landmark êµ¬í˜„
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # ì›ë³¸ frameì˜ ë°°ì—´ RGBë¥¼ BGRë¡œ ë³€ê²½
        
        draw(image, results) # draw í•¨ìˆ˜í™”
                    
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        
        if cv2.waitKey(1) == ord('q'):
            break
            
cap.release()