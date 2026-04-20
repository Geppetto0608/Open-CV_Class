#!/usr/bin/env python3
import cv2
import numpy as np

# 이미지 경로 설정
image_path = '/home/unicon3/catkin_ws/src/opencv_test/images/image.jpg'
image = cv2.imread(image_path)

# 이미지의 Edge detection 수행
edges = cv2.Canny(image, 50, 150)

# 이미지의 Edge를 바탕으로 Contour 검출
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_image = image.copy()
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

# 원본 이미지 내 Edge를 화면에 출력
cv2.imshow('Contours', contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()