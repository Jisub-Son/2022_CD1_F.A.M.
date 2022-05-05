import numpy as np ## 스켈레톤 탐지 후 각도/거리 계산
from body_part_angle import BodyPartAngle ## body_part_angle 불러오기
from body_part_distance import BodyPartDistance
from utils import * ## utils 불러오기
  
class TypeOfExercise(BodyPartAngle):
    def __init__(self, landmarks):
        super().__init__(landmarks)

    def pushup(self, counter, status, set, feedback, count): ## 푸쉬업
        left_arm_angle = self.angle_of_the_left_arm()
        right_arm_angle = self.angle_of_the_left_arm()
        avg_arm_angle = (left_arm_angle + right_arm_angle) // 2 ## 팔꿈치 각도

        if status:
            if (avg_arm_angle < 70) or ( (170 < self.angle_of_the_abdomen) and (self.angle_of_the_abdomen<190) ): ## 구부릴때
                counter += 1 ## 카운트
                status = False

                if counter == 15:
                    counter = 0
                    set +=1
                    feedback = "Take some rest, 60sec"
                    count = 60


                if count == 0:
                    feedback = "Rest time is done, Start exercise"
                if set == 5:
                    feedback = "exercise is done"
                    
        else:
            if avg_arm_angle > 160: ## 안구부릴때
                status = True
                feedback = "Ready"

        return [counter, status, set, feedback, count]p

    def squat(self, counter, status, set, feedback, count): ## 스쿼트
        left_leg_angle = self.angle_of_the_right_leg() ## 무릎각도
        right_leg_angle = self.angle_of_the_left_leg()
        avg_leg_angle = (left_leg_angle + right_leg_angle) // 2
        foot_index_distance = self.distance_between_the_foot_index()
        heel_index_distance = self.distance_between_the_heel()
        avg_feet_distance = (foot_index_distance + heel_index_distance) // 2
        
##        if pose_feedback:
##            if foot_index_distance == heel_index_distance:
##                pose_feedback = True
##        else:
##            if foot_index_distance != heel_index_distance:
##                pose_feedback = False
               
        if status:      
            if avg_leg_angle < 70: ## 무릎을 충분히 굽힐 때
                counter += 1 ## 카운트
                status = False
                feedback = "Success" ## 성공
                if counter == 5: ## 1세트
                  counter = 0 ## 초기화
                  set += 1 ## 1세트 종료
                  feedback = "Tack some rest, 60sec" ## 1분 휴식
                  count = 60 ## 타이머 60초
                  
                if count == 0: ## 타이머 0초
                    feedback = "Rest time is done, Start exercise" ## 휴식시간 1분
                if set == 5: ## 운동 끝
                  feedback = "exercise is done" ## 운동 끝
        else:          
            if avg_leg_angle > 160: ## 무릎을 충분히 굽히지 않을 때
                status = True
                feedback = "Ready" ## 준비
        return [counter, status, set, feedback,count]

    def calculate_exercise(self, exercise_type, counter, status, set, feedback, count): ## 운동횟수 계산
        if exercise_type == "pushup":
            counter, status, set, feedback, count = TypeOfExercise(self.landmarks).pushup(
                counter, status, set, feedback, count)
        elif exercise_type == "squat":
            counter, status, set, feedback, count = TypeOfExercise(self.landmarks).squat(
                counter, status, set, feedback, count)
        return [counter, status, set, feedback, count]
