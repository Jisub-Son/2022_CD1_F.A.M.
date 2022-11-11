import cv2
import time

CAM_ID = 1
cam = cv2.VideoCapture(CAM_ID)

if cam.isOpened() == False:
    print('Can\'t open the CAM(%d)' % (CAM_ID))
    exit()

cv2.namedWindow('Cam')
prevTime = 0

while (True):
    ret, frame = cam.read()
    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime
    fps = 1 / (sec)
    str = "FPS : %0.1f" % fps
    
    cv2.putText(frame, str, (5, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
    print("fps ", str)
    
    cv2.imshow('Cam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cam.release()
        cv2.destroyWindow('Cam')