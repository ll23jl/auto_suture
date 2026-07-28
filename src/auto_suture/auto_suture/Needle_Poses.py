

# ---------------------------------------- Imports ----------------------------------------


import rclpy
from rclpy.node import Node
from ambf_msgs.msg import RigidBodyState
from geometry_msgs.msg import PoseStamped
import PyKDL
from PyKDL import Frame, Rotation, Vector
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose


# ---------------------------------------- Needle poses node ----------------------------------------


class NeedlePoses(Node):

    def __init__(self):
        super().__init__('needle_poses')
        
        # ------------------------------ Variables ------------------------------

        self.needle_pose = None
        self.camera_pose = None

        # ------------------------------ Subscriptions ------------------------------

        # Subcriber to needle pose in camera frame
        self.needle_subscription = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_camera_frame',
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

        # ------------------------------ Publishers ------------------------------

        # Publisher for needle pose in world frame
        self.publisher_ = self.create_publisher(
            PoseStamped,
            '/needle_pose_in_world_frame',
            10
        )

    # ------------------------------ Functions ------------------------------

    # ----- Callback function that stores needle pose in camera frame -----
    def needle_callback(self, msg):
        self.needle_pose = msg.pose
        self.calculate_transform()


    # ----- Callback function that stores camera pose in world frame -----
    def camera_callback(self, msg):
        self.camera_pose = msg.pose
        self.calculate_transform()


    # ----- Function that transforms the needle pose into the world frame -----
    def calculate_transform(self):

        if self.needle_pose is None or self.camera_pose is None:
            return


        # ----- Convert needle and camera poses in PyKDL format -----

        T_needle_camera = pose_to_pykdl(self.needle_pose)


        T_camera_world = pose_to_pykdl(self.camera_pose)
        

        # ----- Calculate the needle position in the world frame -----

        T_needle_world = (
            T_camera_world
            *
            T_needle_camera
        )

        # ----- Create a new outgoing message -----

        pose = PoseStamped()

        pose.header.frame_id = "world"

        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose = pykdl_to_pose(T_needle_world)

        self.publisher_.publish(pose)


# ---------------------------------------- Main ----------------------------------------


def main(args=None):
    rclpy.init(args=args)

    needle_poses = NeedlePoses()

    rclpy.spin(needle_poses)

    # Destroy the node explicitly
    needle_poses.destroy_node()
    rclpy.shutdown()


