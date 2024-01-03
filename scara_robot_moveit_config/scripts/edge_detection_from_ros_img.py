#! /usr/bin/python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
bridge = CvBridge()
import rospkg
def detect_edges_and_draw_box(image):

    rospack = rospkg.RosPack()
    package_path = rospack.get_path('scara_robot_moveit_config')

    # Construct the full path to save the file
    file_path = package_path+'/scripts/images/output_image.jpeg'
    print(file_path)
    if image is None:
        print("Error: Unable to read the image.")
        return

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detector to find edges
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate over contours and draw bounding boxes
    for contour in contours:
        # Ignore small contours
        if cv2.contourArea(contour) > 100:
            # Get bounding box coordinates
            x, y, w, h = cv2.boundingRect(contour)

            # Draw the bounding box on the original image
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(file_path, image)
    
def image_callback(msg):
    print("Got the image!")
    try:
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        detect_edges_and_draw_box(cv2_img)
    except Exception as e:
        print(e) 
if __name__ == '__main__':
    rospy.init_node('image_listener')
    image_topic = "/scara/camera1/image_raw"
    rospy.Subscriber(image_topic, Image, image_callback)
    rospy.spin()
