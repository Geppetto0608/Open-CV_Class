#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
import os

def process_image(image_path):
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

    # 1. 이미지를 회색조로 변환
    gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # 2. 가우시안 블러 필터 적용
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # 3. 에지 검출
    edges = cv2.Canny(blurred_image, 50, 150)

    # 4. Hough 변환을 사용한 선 검출
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 20, minLineLength=30, maxLineGap=200)
    line_image = np.zeros_like(cv_image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)

    # 5. 원본 이미지와 검출된 선을 합성
    combined_image = cv2.addWeighted(cv_image, 0.8, line_image, 1, 1)

    # 결과 이미지 표시
    cv2.imshow('Lane Detection', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    rospy.init_node('lane_detection_node')

    # 이미지 파일 경로 설정
    image_path = rospy.get_param('~image_path', '/home/unicon3/catkin_ws/src/opencv_test/images/road1.jpg')

    # 이미지 처리 함수 호출
    process_image(image_path)

if __name__ == '__main__':
    main()