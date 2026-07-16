
# Node that converts needle pose in the camera frame into the world frame
# Subscribes to needle pose (in camera frame) and camera pose data given by ECM
# Transforms needle pose into the world frame
# Publishes needle pose in the world frame as PoseStamped
# -----------------------------------------------------------------------

# Imports

import rclpy
from rclpy.node import Node
from ambf_msgs.msg import RigidBodyState
from geometry_msgs.msg import PoseStamped
import PyKDL
from PyKDL import Frame, Rotation, Vector


# Define node
class NeedlePosition(Node):

    def __init__(self):
        super().__init__('needle_position')
        
        # Initialize variables to store needle and camera poses in camera/world frame
        self.needle_pose = None
        self.camera_pose = None


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

        # Publisher for needle pose in world frame
        self.publisher_ = self.create_publisher(
            PoseStamped,
            '/needle_pose_in_world_frame',
            10
        )

    # Callback function that stores needle pose in camera frame
    def needle_callback(self, msg):
        self.needle_pose = msg.pose
        self.calculate_transform()

    # Callback function that stores camera pose in world frame
    def camera_callback(self, msg):
        self.camera_pose = msg.pose
        self.calculate_transform()

    # Function that transforms the needle pose into the world frame
    def calculate_transform(self):

        if self.needle_pose is None or self.camera_pose is None:
            return

        # Convert needle and camera poses in PyKDL format
        T_needle_camera = PyKDL.Frame(
            PyKDL.Rotation.Quaternion(
                self.needle_pose.orientation.x,
                self.needle_pose.orientation.y,
                self.needle_pose.orientation.z,
                self.needle_pose.orientation.w
            ),
            PyKDL.Vector(
                self.needle_pose.position.x,
                self.needle_pose.position.y,
                self.needle_pose.position.z
            )
        )

        T_camera_world = PyKDL.Frame(
            PyKDL.Rotation.Quaternion(
                self.camera_pose.orientation.x,
                self.camera_pose.orientation.y,
                self.camera_pose.orientation.z,
                self.camera_pose.orientation.w
            ),
            PyKDL.Vector(
                self.camera_pose.position.x,
                self.camera_pose.position.y,
                self.camera_pose.position.z
            )
        )

        # Calculate the needle position in the world frame
        T_needle_world = (
            T_camera_world
            *
            T_needle_camera
        )

        # Create a new outgoing message
        pose = PoseStamped()

        pose.header.frame_id = "world"

        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.position.x = T_needle_world.p.x()
        pose.pose.position.y = T_needle_world.p.y()
        pose.pose.position.z = T_needle_world.p.z()

        qx, qy, qz, qw = T_needle_world.M.GetQuaternion()

        pose.pose.orientation.x = qx
        pose.pose.orientation.y = qy
        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw

        self.publisher_.publish(pose)

def main(args=None):
    rclpy.init(args=args)

    needle_position = NeedlePosition()

    rclpy.spin(needle_position)

    # Destroy the node explicitly
    needle_position.destroy_node()
    rclpy.shutdown()


