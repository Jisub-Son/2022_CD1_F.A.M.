import cv2
from utils import *

# display guide
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
    if camID == RIGHT_CAM: 
        frame[r:rows + r, c:cols + c] = final0 ## 캠화면에 실시간으로 출력하기 위해 합성 
    elif camID == LEFT_CAM: ## cam1 에는 flip된 영상 출력         
        frame[r:rows + r, c:cols + c] = final1   