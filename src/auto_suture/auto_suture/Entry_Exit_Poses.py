

# ---------------------------------------- Imports ----------------------------------------


import rclpy
from rclpy.node import Node
from ambf_msgs.msg import RigidBodyState
from geometry_msgs.msg import PoseStamped
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose


# ---------------------------------------- Entry and Exit poses node ----------------------------------------


class EntryExitPoses(Node):

    def __init__(self):
        super().__init__('entry_exit_poses')
        
        # ------------------------------ Variables ------------------------------

        self.camera_pose = None
        self.entry1_pose = None
        self.exit1_pose = None

        # ------------------------------ Subscriptions ------------------------------

        # Subcriber to camera pose in world frame
        self.camera_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/CameraFrame/State',
            self.camera_callback,
            10
        )

        # Subcriber to entry 1 pose in camera frame
        self.entry1_subscription = self.create_subscription(
            PoseStamped,
            '/entry1_pose_in_camera_frame',
            self.entry1_callback,
            10
        )

        # Subcriber to exit 1 pose in camera frame
        self.exit1_subscription = self.create_subscription(
            PoseStamped,
            '/exit1_pose_in_camera_frame',
            self.exit1_callback,
            10
        )

        # ------------------------------ Publishers ------------------------------

        # Publisher for entry 1 pose in world frame
        self.entry1_publisher_ = self.create_publisher(
            PoseStamped,
            '/entry1_pose_in_world_frame',
            10
        )

        # Publisher for exit 1 pose in world frame
        self.exit1_publisher_ = self.create_publisher(
            PoseStamped,
            '/exit1_pose_in_world_frame',
            10
        )

    # ------------------------------ Functions ------------------------------



    # Callback function that stores camera pose in world frame
    def camera_callback(self, msg):
        self.camera_pose = msg.pose
        #self.transform_camera_to_world()

    # Callback function for new entry 1 poses 
    def entry1_callback(self, msg):
        self.entry1_pose = msg.pose
        new_msg = self.transform_camera_to_world(self.entry1_pose)
        if new_msg is not None:
            self.entry1_publisher_.publish(new_msg)

    # Callback function for new exit 1 poses 
    def exit1_callback(self, msg):
        self.exit1_pose = msg.pose
        new_msg = self.transform_camera_to_world(self.exit1_pose)
        if new_msg is not None:
            self.exit1_publisher_.publish(new_msg)


    # Function that transforms the pose into the world frame 
    def transform_camera_to_world(self, pose):

        if pose is None or self.camera_pose is None:
            return


        # ----- Convert pose and camera poses in PyKDL format -----

        T_pose_camera = pose_to_pykdl(pose)


        T_camera_world = pose_to_pykdl(self.camera_pose)
        

        # ----- Calculate the pose position in the world frame -----

        T_pose_world = (
            T_camera_world
            *
            T_pose_camera
        )

        # ----- Create a new outgoing message -----

        new_pose = PoseStamped()

        new_pose.header.frame_id = "world"

        new_pose.header.stamp = self.get_clock().now().to_msg()

        new_pose.pose = pykdl_to_pose(T_pose_world)

        return(new_pose)


# ---------------------------------------- Main ----------------------------------------


def main(args=None):
    rclpy.init(args=args)

    entry_exit_poses = EntryExitPoses()

    rclpy.spin(entry_exit_poses)

    # Destroy the node explicitly
    entry_exit_poses.destroy_node()
    rclpy.shutdown()


