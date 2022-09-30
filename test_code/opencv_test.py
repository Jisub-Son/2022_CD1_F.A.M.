import cv2 as cv

cap = cv.VideoCapture(0)

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv.imshow('video', frame)
    
    if cv.waitKey(1) == ord('q'):
        break
    
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()