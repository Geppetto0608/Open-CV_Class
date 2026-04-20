#!/usr/bin/env python3

import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class Unicon_CV():
    def __init__(self):
        self.camera_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.camera_callback)
        self.bridge = CvBridge()

    def camera_callback(self, data):
        try:
            # Read camera data
            cv_image_raw = self.bridge.imgmsg_to_cv2(data, "bgr8")

            hsv = cv2.cvtColor(cv_image_raw, cv2.COLOR_BGR2HSV)

            # White mask HSV range
            #lower_white = np.array([0, 0, 200])
            #upper_white = np.array([180, 25, 255])
            #lower_white = np.array([0, 0, 180])
            #upper_white = np.array([255, 30, 255])
            lower_white = np.array([0, 0, 85])
            upper_white = np.array([179, 25, 255])

            # Yellow mask HSV range
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])

            mask_white = cv2.inRange(hsv, lower_white, upper_white)
            mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

            # Find white and yellow lane points
            white_lane_points = cv2.findNonZero(mask_white)
            yellow_lane_points = cv2.findNonZero(mask_yellow)

            # Draw white lane points as red dots
            if white_lane_points is not None:
                for point in white_lane_points:
                    x, y = point[0]
                    cv_image_raw[y, x] = [0, 0, 255]  # Red color

            # Draw yellow lane points as green dots
            if yellow_lane_points is not None:
                for point in yellow_lane_points:
                    x, y = point[0]
                    cv_image_raw[y, x] = [0, 255, 0]  # Green color

            cv2.imshow('Lane Detection', cv_image_raw)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                rospy.signal_shutdown("User exit with 'q' key")
                cv2.destroyAllWindows()

        except CvBridgeError as e:
            print(e)

    def main(self):
        rospy.spin()


if __name__ == "__main__":
    try:
        rospy.init_node("unicon_cv")
        unicon_cv = Unicon_CV()
        unicon_cv.main()

    except KeyboardInterrupt:
        print("sorry. don't execute")
