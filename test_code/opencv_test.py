import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # frame = frame.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # frame = frame.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    frame = cv2.resize(frame, dsize=(720, 480))
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # h, w = frame.shape
    # print("h, ", h)
    # print("w, ", w)
        
    # Display the resulting frame
    cv2.imshow('video', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# 640 480 / 8 6 / 4 3 / 720 540