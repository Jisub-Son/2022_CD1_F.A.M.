import cv2
import numpy as np
import sys
from PIL import Image, ImageSequence

cap = cv2.VideoCapture(0) ## 캠 
if cap is None:
    print('Video load failed!')
    sys.exit()
    
logo = cv2.imread("opencv.png") ## opencv 로고 (추후 졸라맨이나 gif로 변경예정)
if logo is None:
    print('Image load failed!')
    sys.exit()
    
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue    
	
    rows, cols, channels = logo.shape ## 로고 픽셀값
    roi = frame[50:rows + 50, 50:cols + 50] ## 로고를 필셀값 ROI(관심영역) (수치는 뭔지 잘 모르겠음)
    
    gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY) ## 로고를 gray로 변환
    ret, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY) ## 이진영상으로 변환 (흰색배경, 검정로고)
    mask_inv = cv2.bitwise_not(mask) ## mask 반전
 
    background = cv2.bitwise_and(roi, roi, mask = mask) ## 캠화면에 넣을 위치 black
    shadowpartner = cv2.bitwise_and(logo, logo, mask = mask_inv) ## 로고에서 캠화면에 출력할 부분
    final = cv2.bitwise_or(background, shadowpartner) ## 캠화면의 검정부분과 로고 출력부분 합성
 
    frame[50:rows + 50, 50:cols + 50] = final ## 캠화면에 실시간으로 출력하기 위해 합성

    cv2.imshow("frame", frame) ## 최종 출력 영상
 
    if cv2.waitKey(1) == ord('q'): ## q 누르면 종료
        break       
        
cap.release()
cv2.destroyAllWindows()