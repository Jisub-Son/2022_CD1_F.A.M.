import cv2
import time
import numpy as np

cap_0 = cv2.VideoCapture(0)
cap_0.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap_0.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

cap_1 = cv2.VideoCapture(1)
cap_1.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap_1.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

while True:
    # Capture frame-by-frame
    ret_0, frame_0 = cap_0.read()
    ret_1, frame_1 = cap_1.read()
    # if frame is read correctly ret is True
    if not (ret_1 or ret_0):
        print("Can't receive frame (stream end?). Exiting ...")
        break

# calculate fps_0
    fps_0 = cap_0.get(cv2.CAP_PROP_FPS)
    # print('fps',fps)
    if fps_0 == 0.0:
        fps_0 = 30.0
    time_per_frame_video_0 = 1/fps_0
    last_time_0 = time.perf_counter()
    time_per_frame_0 = time.perf_counter() - last_time_0
    time_sleep_frame_0 = max(0,time_per_frame_video_0 - time_per_frame_0)
    time.sleep(time_sleep_frame_0)
    real_fps_0 = 1/(time.perf_counter()-last_time_0)
    last_time_0 = time.perf_counter()
    str_0 = "FPS_0 : %0.2f" % real_fps_0
    cv2.putText(frame_0, str_0, (1,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))   
    
# calculate fps_0
    fps_1 = cap_1.get(cv2.CAP_PROP_FPS)
    # print('fps',fps)
    if fps_1 == 0.0:
        fps_1 = 30.0
    time_per_frame_video_1 = 1/fps_1
    last_time_1 = time.perf_counter()
    time_per_frame_1 = time.perf_counter() - last_time_1
    time_sleep_frame_1 = max(0,time_per_frame_video_1 - time_per_frame_1)
    time.sleep(time_sleep_frame_1)
    real_fps_1 = 1/(time.perf_counter()-last_time_1)
    last_time_1 = time.perf_counter()
    str_1 = "FPS_1 : %0.2f" % real_fps_1
    cv2.putText(frame_1, str_1, (1,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))     

# Display the resulting frame
    cv2.imshow('video0', frame_0)
    cv2.imshow('video1', frame_1)
    """total = np.hconcat([frame_0], [frame_1])
    cv2.imshow("total", total)"""
    
    if cv2.waitKey(1) == ord('q'):
        break
    
# When everything done, release the capture
cap_0.release()
cap_1.release()
cv2.destroyAllWindows()
