#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
import os

def process_image(image_path):
    rospy.loginfo(f"Processing image: {image_path}")

    # 이미지 파일이 존재하는지 확인
    if not os.path.exists(image_path):
        rospy.logerr(f"Error: Image file not found at {image_path}")
        return

    # 이미지 읽기
    cv_image = cv2.imread(image_path)

    # 이미지가 정상적으로 읽혔는지 확인
    if cv_image is None:
        rospy.logerr("Error: Could not open or find the image.")
        return

    # 1. 이미지를 HSV 색 공간으로 변환
    hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    # 2. 노란색 차선 필터링 (HSV 범위 설정)
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(hsv_image, yellow_lower, yellow_upper)

    # 3. 흰색 차선 필터링 (HSV 범위 설정)
    #white_lower = np.array([0, 0, 180])
    #white_upper = np.array([255, 30, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([180, 25, 255])
    white_mask = cv2.inRange(hsv_image, white_lower, white_upper)

    # 4. 노란색과 흰색 마스크 결합
    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)

    # 5. 결과 이미지
    combined_image = cv2.bitwise_and(cv_image, cv_image, mask=combined_mask)

    # 결과 이미지 표시
    cv2.imshow('Lane Detection', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    rospy.init_node('hsv_lane_detection_node')

    # 이미지 파일 경로 설정
    image_path = '/home/unicon3/catkin_ws/src/opencv_test/images/road1.jpg'

    # 이미지 처리 함수 호출
    process_image(image_path)

if __name__ == '__main__':
    main()