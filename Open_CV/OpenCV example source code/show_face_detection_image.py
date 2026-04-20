#!/usr/bin/env python3
import cv2
import numpy as np

# 이미지 경로 설정
image_path = '/home/unicon3/catkin_ws/src/opencv_test/images/image.jpg'
image = cv2.imread(image_path)

# Face Cascade(haarcascades)를 통해 이미지 속 사람의 얼굴을 검출
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(image, 1.3, 5)
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

# 원본 이미지 내 Edge를 화면에 출력
cv2.imshow('Face Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()