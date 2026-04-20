#!/usr/bin/env python3
import cv2
import numpy as np

# 이미지 경로 설정
image_path = '/home/unicon3/catkin_ws/src/opencv_test/images/image.jpg'
image = cv2.imread(image_path)

# 이미지 회전
(h, w) = image.shape[:2] # (height, width, channel) = image.shape[:]
center = (w / 2, h / 2)
M = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated_image = cv2.warpAffine(image, M, (w, h))
cv2.imshow('Rotated Image', rotated_image)

# 이미지 크기 조정
resized_image = cv2.resize(image, (300, 300))
cv2.imshow('Resized Image', resized_image)

# 이미지 기울이기 (Affine Transform)
pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
M = cv2.getAffineTransform(pts1, pts2)
affine_image = cv2.warpAffine(image, M, (w, h))
cv2.imshow('Affine Transformed Image', affine_image)

# User의 어떠한 입력이라도 들어오기 전까지는 다음 코드 실행 X
cv2.waitKey(0)
# User의 어떠한 입력이 들어오면 모든 OpenCV 창을 닫기
cv2.destroyAllWindows()