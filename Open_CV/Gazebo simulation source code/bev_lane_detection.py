#!/usr/bin/env python3

import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from birdeyeview import BEV

class Unicon_CV():
    def __init__(self):
        self.camera_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.camera_callback)

        self.bridge = CvBridge()
        self.bev = BEV()

        self.y_repeat = 12
        self.left_x = 0
        self.point_scale = 10

        self.left_lane_pred = np.zeros((self.y_repeat, 2))

    def camera_setting(self, data):
        # read camera data, and ROI
        cv_image_raw = self.bridge.imgmsg_to_cv2(data, "bgr8")
        cv_image = cv_image_raw[0:640][300:480]

        # bev_tf  
        A = [(251, 13), (400, 13), (580, 140), (70, 140)] # two line
        bev_image = self.bev.birdeyeview(cv_image, A)

        hsv = cv2.cvtColor(bev_image, cv2.COLOR_BGR2HSV)

        # white mask hsv range
        #lower_white = np.array([0, 0, 200])
        #upper_white = np.array([180, 25, 255])
        #lower_white = np.array([0, 0, 180])
        #upper_white = np.array([255, 30, 255])
        lower_white = np.array([0, 0, 85])
        upper_white = np.array([179, 25, 255])
        
        mask_white = cv2.inRange(hsv, lower_white, upper_white)

        image = bev_image.copy()

        return mask_white, image

    def find_certain_color(self, mask_certain, threshold, j):
        certain_pixels = cv2.countNonZero(mask_certain[self.yy:self.yy+5, j*10:(j+1)*10])

        if certain_pixels > threshold:
            return [(j+1)*10, self.yy+2]
        else:
            return []

    def camera_callback(self, data):
        try:
            mask_white, image = self.camera_setting(data)

            for i in range(self.y_repeat):
                self.yy = 430 - (i + 1) * self.point_scale  # point_scale 간격으로 위로 이동
                self.left_x = 0

                for j in range(64):
                    self.left_lane_points = self.find_certain_color(mask_white, 15, j)  # x for white line

                    if len(self.left_lane_points) > 0:
                        self.left_x = self.left_lane_points[0]

                self.left_lane_pred[i][0] = self.left_x
                self.left_lane_pred[i][1] = self.yy+2
                image[self.yy:self.yy+5, self.left_x-20:self.left_x] = [255, 0, 0]

            cv2.imshow('BEV', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                rospy.signal_shutdown("User exit with 'q' key")
                cv2.destroyAllWindows()
                return

        except CvBridgeError as e:
            print(e)

    def main(self):
        rospy.spin()


if __name__ == "__main__":
    try:
        rospy.init_node("lane_detect")
        unicon_cv = Unicon_CV()
        unicon_cv.main()

    except KeyboardInterrupt:
        print("sorry. don't execute")
