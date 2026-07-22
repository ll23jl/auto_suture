
# This file is a temporary file and will later be replaced with some sort of computer vision (or other method)
# It takes the needle position in the world 
# And converts it to needle position in the camera frame
# This resembles the needle position as the computer vision would see it
# And is the main input to the needle tracking node

# ---------------------------------------

# Imports

import rclpy
from rclpy.node import Node
from ambf_msgs.msg import RigidBodyState
from geometry_msgs.msg import PoseStamped
import PyKDL
from PyKDL import Frame, Rotation, Vector
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose


# ----- Define node -----
class NeedleFrameConverter(Node):

    def __init__(self):
        super().__init__('needle_frame_converter')
        
        # Initialize variables to store needle and camera poses in world frame
        self.needle_pose = None
        self.camera_pose = None


        # Subcriber to needle pose in world frame
        self.needle_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Needle/State',
            self.needle_callback,
            10
        )

        # Subcriber to camera pose in world frame
        self.camera_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/CameraFrame/State',
            self.camera_callback,
            10
        )

        # Publisher for needle pose in camera frame
        self.publisher_ = self.create_publisher(
            PoseStamped,
            '/needle_pose_in_camera_frame',
            10
        )

    # ----- Callback function that stores needle pose in world frame -----
    def needle_callback(self, msg):
        self.needle_pose = msg.pose
        self.calculate_transform()


    # ----- Callback function that stores camera pose in world frame -----
    def camera_callback(self, msg):
        self.camera_pose = msg.pose
        self.calculate_transform()


    # ----- Function that transforms the needle position into the camera frame -----
    def calculate_transform(self):

        if self.needle_pose is None or self.camera_pose is None:
            return


        # ----- Convert needle and camera poses in PyKDL format -----

        T_needle_world = pose_to_pykdl(self.needle_pose)


        T_camera_world = pose_to_pykdl(self.camera_pose)
        

        # ----- Calculate the needle position in the camera frame -----

        T_needle_camera = (
            T_camera_world.Inverse()
            *
            T_needle_world
        )

        # ----- Create a new outgoing message -----

        pose = PoseStamped()

        pose.header.frame_id = "camera"

        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose = pykdl_to_pose(T_needle_camera)

        self.publisher_.publish(pose)


def main(args=None):
    rclpy.init(args=args)

    needle_frame_converter = NeedleFrameConverter()

    rclpy.spin(needle_frame_converter)

    # Destroy the node explicitly
    needle_frame_converter.destroy_node()
    rclpy.shutdown()


