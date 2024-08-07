#!/usr/bin/python3

import rospy
import cv2
import numpy as np

from std_msgs.msg import Bool
from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError



class NodeDetectMarker():
    def __init__(self) -> None:
        
        self.bridge = CvBridge()
        self.inputImage = None
        
        self.triggerSub = rospy.Subscriber("input_trigger", Bool, self.triggerCallback, queue_size=1, tcp_nodelay=True)
        self.imageSub = rospy.Subscriber("input_image", Image, self.imageCallback, queue_size=1, tcp_nodelay=True)
        
        self.imagePub = rospy.Publisher("output_image", Image, queue_size=1, tcp_nodelay=True)
        self.detectionResultPub = rospy.Publisher("output_result", Bool, queue_size=1, tcp_nodelay=True)
        
    ##############
    def triggerCallback(self, trigger: Bool):
        
        rospy.loginfo("Received trigger")
        
        if trigger.data != True:
            rospy.loginfo("Trigger is False")
            self.inputImage = None
            return
        
        if isinstance(self.inputImage, np.ndarray):
            # Copy input image
            outImg = self.inputImage.copy()
            
            outImgMsg = None
            result = self.processImage(self.inputImage, outImg)
            
            # publish result image 
            if isinstance(outImg, np.ndarray):
                rospy.loginfo("Publish result image")
                outImgMsg = self.bridge.cv2_to_imgmsg(outImg, encoding='bgr8')
                self.imagePub.publish(outImgMsg)
                
            # publish detection result
            self.detectionResultPub.publish(Bool(result))    
            
            if (result):
                rospy.loginfo("Markers detected!")
            else:
                rospy.loginfo("Markers NOT detected!")
                
                
        
        
    ##############
    def imageCallback(self, msg: Image):
        
        # rospy.loginfo("Received image")
        
        try:
            # Convert ROS Image message to OpenCV image
            self.inputImage = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
        except CvBridgeError as e:
            print(e)
            
            
    ###########
    def processImage(self, inImg, outImg) -> bool:
        
        # Convert to HSV color space
        hsv_image = cv2.cvtColor(inImg, cv2.COLOR_BGR2HSV)
        
        # Define range of red color in HSV
        lower_red = np.array([160, 80, 80])
        upper_red = np.array([179, 255, 255])
        
        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv_image, lower_red, upper_red)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rospy.loginfo(f'number of contour {len(contours)}')

        # Draw bounding boxes around detected blobs
        isDetected = False
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # rospy.loginfo(f'xy = {x}, {y}')
            if (w*h > 30) and (y > 360):
                cv2.rectangle(outImg, (x, y), (x + w, y + h), (0, 255, 0), 2)
                isDetected = True

            
        return isDetected
    
    
if __name__ == "__main__":
    rospy.init_node("node_detect_marker")

    __node = NodeDetectMarker()

    rospy.spin()   
