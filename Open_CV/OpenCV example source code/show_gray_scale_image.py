#!/usr/bin/env python3
import cv2
import numpy as np

# 이미지 경로 설정
image_path = '/home/unicon3/catkin_ws/src/opencv_test/images/image.jpg'
image = cv2.imread(image_path)

# 이미지 Gray scale화 수행
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gray scale화된 이미지를 화면에 출력
cv2.imshow('Gray scale Image', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()