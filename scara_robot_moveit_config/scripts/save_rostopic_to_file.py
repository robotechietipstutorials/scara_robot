#! /usr/bin/python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import rospkg
bridge = CvBridge()
def image_callback(msg):

    rospack = rospkg.RosPack()
    package_path = rospack.get_path('scara_robot_moveit_config')

    # Construct the full path to save the file
    file_path = package_path+'/scripts/images/output_image.jpeg'
    print(file_path)
    print("Got the image!")
    try:
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        cv2.imwrite(file_path, cv2_img)
    except Exception as e:
        print(e) 
if __name__ == '__main__':
    rospy.init_node('image_listener')
    image_topic = "/scara/camera1/image_raw"
    rospy.Subscriber(image_topic, Image, image_callback)
    rospy.spin()
