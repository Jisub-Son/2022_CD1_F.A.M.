import cv2
from utils import *

squat_down = 1 ## 초기화
squat_up = 51
pushup_down = 1
pushup_up = 60
sidelateralraise_up = 1
sidelateralraise_down = 35
    
# display guide
def shadow(file, frame, camID, r, c): 
    file_inv = cv2.flip(file, 1) ## 좌우반전
    
    if file is None:
        print('guide image load failed!')
        
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

def guide(shadow_mode, shadow_status, shadow_feedback, shadow_frame, shadow_camID): 
    global squat_down, squat_up, pushup_down, pushup_up, sidelateralraise_up, sidelateralraise_down # global 변수
    
    if (shadow_mode == "squat"):# and shadow_status == 'Up' and shadow_feedback == 'Start'): # squat: up state
        down = cv2.imread('squat\squat_' + str(squat_down) +'.jpg') ## 1번부터 읽기
        file = cv2.resize(down, dsize = (0, 0), fx = 1.15, fy = 1.15) ## 크기 조절
        squat_down += 1 ## 증가     
        if squat_down == 50: ## 범위 넘어가면
            squat_down = 1  ## 초기화        
        shadow(file, shadow_frame, shadow_camID, 20, 240) ## 가이드 불러오기
        print("squat_down", squat_down)
    else:
        squat_down = 1  ## 초기화  
    
    if (shadow_mode == "squat" and shadow_status == 'Down' and shadow_feedback == 'Success'): # squat: down state
        up = cv2.imread('squat\squat_' + str(squat_up) +'.jpg') ## 1번부터 읽기
        file = cv2.resize(up, dsize = (0, 0), fx = 1.15, fy = 1.15) ## 크기 조절
        squat_up += 1 ## 증가     
        if squat_up == 65: ## 범위 넘어가면
            squat_up = 51  ## 초기화      
        shadow(file, shadow_frame, shadow_camID, 20, 240) ## 가이드 불러오기
    else:                          
        squat_up = 51  ## 초기화 
                    
    if (shadow_mode == "pushup"):# and shadow_status == 'Up' and shadow_feedback == 'Start'): # pushup: up state 
        down = cv2.imread('pushup\pushup_' + str(pushup_down) +'.jpg') ## 1번부터 읽기
        down_flip = cv2.flip(down, 1) ## 좌우반전(실수로 반대로 찍음)
        file = cv2.resize(down_flip, dsize = (0, 0), fx = 1.5, fy = 1.5) ## 크기 조절
        pushup_down += 1 ## 증가    
        if pushup_down == 59: ## 범위 넘어가면
            pushup_down = 1 ## 초기화     
        shadow(file, shadow_frame, shadow_camID, 150, 100) ## 가이드 불러오기
    else:
        pushup_down = 1  ## 초기화
                    
    if (shadow_mode == "pushup" and shadow_status == 'Down' and shadow_feedback == 'Success'): # pushup: down state
        up = cv2.imread('pushup\pushup_' + str(pushup_up) +'.jpg')
        up_flip = cv2.flip(up, 1) ## 좌우반전(실수로 반대로 찍음)
        file = cv2.resize(up_flip, dsize = (0, 0), fx = 1.5, fy = 1.5) ## 크기 조절
        pushup_up += 1 ## 증가     
        if pushup_up == 69: ## 범위 넘어가면
            pushup_up = 60  ## 초기화        
        shadow(file, shadow_frame, shadow_camID, 150, 100)
    else:
        pushup_up = 60  ## 초기화         
                    
    if (shadow_mode == "sidelateralraise"):# and shadow_status == 'Down' and shadow_feedback == 'Start'): # side lateral raise: down state
        down = cv2.imread('sidelateralraise\sidelateralraise_' + str(sidelateralraise_up) +'.jpg') ## 1번부터 읽기
        file = cv2.resize(down, dsize = (0, 0), fx = 1.2, fy = 1.2) ## 크기 조절
        sidelateralraise_up += 1 ## 증가     
        if sidelateralraise_up == 35: ## 범위 넘어가면
            sidelateralraise_up = 1  ## 초기화        
        shadow(file, shadow_frame, shadow_camID, 20, 150)
    else:
        sidelateralraise_up = 1  ## 초기화    
                    
    if (shadow_mode == "sidelateralraise" and shadow_status == 'Up' and shadow_feedback == 'Success'): # side lateral raise: upstate
        up = cv2.imread('sidelateralraise\sidelateralraise_' + str(sidelateralraise_down) +'.jpg') ## 1번부터 읽기
        file = cv2.resize(up, dsize = (0, 0), fx = 1.2, fy = 1.2) ## 크기 조절
        sidelateralraise_down += 1 ## 증가     
        if sidelateralraise_down == 63: ## 범위 넘어가면
            sidelateralraise_down = 35  ## 초기화      
        shadow(file, shadow_frame, shadow_camID, 20, 150)
    else:                          
        sidelateralraise_down = 35  ## 초기화          