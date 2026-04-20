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

    # 이미지 크기
    height, width = cv_image.shape[:2]

    # 1. 관심 영역(ROI) 설정 (하단 절반)
    roi_vertices = [
        (0, height),
        (0, height // 2),
        (width, height // 2),
        (width, height)
    ]
    mask = np.zeros_like(cv_image)
    match_mask_color = (255,) * cv_image.shape[2]
    cv2.fillPoly(mask, np.array([roi_vertices], np.int32), match_mask_color)
    masked_image = cv2.bitwise_and(cv_image, mask)

    # 2. 이미지를 HSV 색 공간으로 변환
    hsv_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2HSV)

    # 3. 노란색 차선 필터링 (HSV 범위 설정)
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(hsv_image, yellow_lower, yellow_upper)

    # 4. 흰색 차선 필터링 (HSV 범위 설정)
    #white_lower = np.array([0, 0, 180])
    #white_upper = np.array([255, 30, 255])
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([180, 25, 255])
    white_mask = cv2.inRange(hsv_image, white_lower, white_upper)

    # 5. 노란색과 흰색 마스크 결합
    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)

    # 6. 에지 검출 (HSV 필터링 후)
    edges = cv2.Canny(combined_mask, 50, 150)

    # 7. Hough 변환을 사용한 선 검출
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 20, minLineLength=30, maxLineGap=200)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 5)

    # 결과 이미지 표시
    cv_image = cv2.resize(cv_image, (960, 540))  # 이미지 크기 조정
    cv2.imshow('Lane Detection', cv_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    rospy.init_node('lane_detection_hsv_node')

    # 이미지 파일 경로 설정
    image_path = '/home/unicon3/catkin_ws/src/opencv_test/images/road2.jpg'
    # 이미지 처리 함수 호출
    process_image(image_path)

if __name__ == '__main__':
    main()