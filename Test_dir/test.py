import time

avg_spine_angle = 0
avg_arm_angle = 0
reps = 0
sets = 0
status = 'Up'
feedback = 'Ready'
REF_REPS = 5
REF_SETS = 3
REF_TIMER = 5
REF_ARM_ANGLE = 90
REF_SPINE_ANGLE = 170

if avg_arm_angle < REF_ARM_ANGLE and avg_spine_angle > REF_SPINE_ANGLE:     # 팔꿈치를 충분히 굽히고 허리가 일자일 때
    reps += 1
    status = 'Down'
    feedback = 'Success'
    prev = time.time()
else:
    if avg_arm_angle > REF_ARM_ANGLE:     # 팔을 충분히 굽히지 않은 경우
        status = 'Up'
        feedback = 'Bend your elbows'
    elif avg_spine_angle < REF_SPINE_ANGLE: # 척추가 일자가 아닐 경우
        status = 'Up'
        feedback = 'Straight your spine'
        
if reps == REF_REPS:
    reps, status, sets, feedback, timer = self.Rest_timer(reps, status, sets, feedback, timer)  # 타이머 함수 호출
    
if sets == REF_SETS:
    reps = 0
    status = 'Up'
    sets = 0
    feedback = 'Well done!'
    