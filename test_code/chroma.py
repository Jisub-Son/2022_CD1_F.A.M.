import cv2
from cv2 import rectangle
import numpy as np
import sys
from PIL import Image, ImageSequence

r = 5 ## 200, 10 지점
c = 5

cap = cv2.VideoCapture(0) ## 캠 
if cap is None:
    print('Video load failed!')
    sys.exit()
    
gif = Image.open(r'pushup\pushup.gif') ## gif (gif를 png로 변환할 때만 사용, gif가 조금만 길면 렉걸림)
if gif is None:
    print('gif load failed!')
    sys.exit()
    
sequence = [] ## gif 초기값   
i = 0 

for f in ImageSequence.Iterator(gif): ## gif를 png로 변환하여 저장(gif를 png로 변환할 때만 사용, gif가 조금만 길면 렉걸림)
    sequence.append(f.copy()) 
    i += 1  
    f.save('pushup\pushup_' + str(i) +'.png')
    
for i in range(1, 70): ## bandicam 흰색으로 masking
    first = cv2.imread('pushup\pushup_' + str(i) +'.png') ## 1번부터 읽기
    rect = cv2.rectangle(first, (0, 0), (304,30), (255, 255, 255), -1)
    cv2.imshow('test', rect)
    cv2.imwrite('pushup\pushup_' + str(i) +'.jpg', rect)
    i += 1
    
i = 1 ## output_1 부터 시작  
        
while cap.isOpened():
    success, frame = cap.read()
    
    if not success:
        continue    
     
    logo = cv2.imread('pushup\pushup_' + str(i) +'.jpg') ## 1번부터 읽기
    cv2.imshow('test', logo)
    
    if logo is None:
        print('image load failed!')
        sys.exit()
    i += 1 ## i 증가     
    if i == 70: ## 범위 넘어가면
        i = 1  ## 초기화
    
    rows, cols, channels = logo.shape ## 로고 픽셀값
    if i == 1: ## 전체 크기 확인
        print(rows, cols)
    roi = frame[r:rows + r, c:cols + c] ## 로고를 필셀값 ROI(관심영역) (수치는 뭔지 잘 모르겠음)
    
    gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY) ## 로고를 gray로 변환
    cv2.imshow("gray", gray)
    ret, mask = cv2.threshold(gray, 97, 255, cv2.THRESH_BINARY) ## 이진영상으로 변환 (흰색배경, 검정로고)
    cv2.imshow("binary", mask)
    mask_inv = cv2.bitwise_not(mask) ## mask 반전 배경
    cv2.imshow("binary_inv", mask_inv)
    background = cv2.bitwise_and(roi, roi, mask = mask) ## 캠화면에 넣을 위치 black
    cv2.imshow("background", background)
    shadowpartner = cv2.bitwise_and(logo, logo, mask = mask_inv) ## 로고에서 캠화면에 출력할 부분
    cv2.imshow("shadow", shadowpartner)
    final = cv2.bitwise_or(background, shadowpartner) ## 캠화면의 검정부분과 로고 출력부분 합성
    cv2.imshow("final",final)
    frame[r:rows + r, c:cols + c] = final ## 캠화면에 실시간으로 출력하기 위해 합성

    cv2.imshow("frame", frame) ## 최종 출력 영상
 
    if cv2.waitKey(1) == ord('q'): ## q 누르면 종료
        break       
        
cap.release()
cv2.destroyAllWindows()