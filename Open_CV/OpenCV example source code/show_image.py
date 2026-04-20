#!/usr/bin/env python3
import cv2
import numpy as np

# 이미지 경로 설정
image_path = '/home/unicon3/catkin_ws/src/opencv_test/images/image.jpg'
image = cv2.imread(image_path)

# 원본 이미지를 화면에 출력
cv2.imshow('Original Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()