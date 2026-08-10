
# This file is a temporary file and will later be replaced with some sort of computer vision (or other method)


# ---------------------------------------- Imports ----------------------------------------


import rclpy
from rclpy.node import Node
from ambf_msgs.msg import RigidBodyState
from geometry_msgs.msg import PoseStamped
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose


# ---------------------------------------- Simulation ECM node ----------------------------------------


class SimulationECM(Node):

    def __init__(self):
        super().__init__('simulation_to_ecm')
        
        # ------------------------------ Variables ------------------------------

        self.needle_pose = None
        self.camera_pose = None
        self.entry1_pose = None
        self.exit1_pose = None


        # ------------------------------ Subscriptions ------------------------------

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

        # Subscriber to entry 1 in world frame
        self.entry1_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Entry1/State',
            self.entry1_callback,
            10
        )

        # Subscriber to exit 1 in world frame
        self.exit1_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Exit1/State',
            self.exit1_callback,
            10
        )

        # Subscriber to entry 2 in world frame
        self.entry2_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Entry2/State',
            self.entry2_callback,
            10
        )

        # Subscriber to exit 2 in world frame
        self.exit2_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Exit2/State',
            self.exit2_callback,
            10
        )

        # Subscriber to entry 3 in world frame
        self.entry3_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Entry3/State',
            self.entry3_callback,
            10
        )

        # Subscriber to exit 3 in world frame
        self.exit3_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Exit3/State',
            self.exit3_callback,
            10
        )

        # Subscriber to entry 4 in world frame
        self.entry4_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Entry4/State',
            self.entry4_callback,
            10
        )

        # Subscriber to exit 4 in world frame
        self.exit4_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/Exit4/State',
            self.exit4_callback,
            10
        )

        # ------------------------------ Publishers ------------------------------
        
        # Publisher for needle pose in camera frame
        self.needle_publisher_ = self.create_publisher(
            PoseStamped,
            '/needle_pose_in_camera_frame',
            10
        )

        # Publisher for entry 1 pose in camera frame
        self.entry1_publisher_ = self.create_publisher(
            PoseStamped,
            '/entry1_pose_in_camera_frame',
            10
        )

        # Publisher for exit 1 pose in camera frame
        self.exit1_publisher_ = self.create_publisher(
            PoseStamped,
            '/exit1_pose_in_camera_frame',
            10
        )
        # Publisher for entry 2 pose in camera frame
        self.entry2_publisher_ = self.create_publisher(
            PoseStamped,
            '/entry2_pose_in_camera_frame',
            10
        )

        # Publisher for exit 2 pose in camera frame
        self.exit2_publisher_ = self.create_publisher(
            PoseStamped,
            '/exit2_pose_in_camera_frame',
            10
        )

        # Publisher for entry 3 pose in camera frame
        self.entry3_publisher_ = self.create_publisher(
            PoseStamped,
            '/entry3_pose_in_camera_frame',
            10
        )

        # Publisher for exit 3 pose in camera frame
        self.exit3_publisher_ = self.create_publisher(
            PoseStamped,
            '/exit3_pose_in_camera_frame',
            10
        )

        # Publisher for entry 4 pose in camera frame
        self.entry4_publisher_ = self.create_publisher(
            PoseStamped,
            '/entry4_pose_in_camera_frame',
            10
        )

        # Publisher for exit 4 pose in camera frame
        self.exit4_publisher_ = self.create_publisher(
            PoseStamped,
            '/exit4_pose_in_camera_frame',
            10
        )

    # ------------------------------ Functions ------------------------------

    # Callback function for new needle poses 
    def needle_callback(self, msg):
        self.needle_pose = msg.pose
        new_msg = self.transform_world_to_camera(self.needle_pose)
        if new_msg is not None:
            self.needle_publisher_.publish(new_msg)

    # Callback function for new entry 1 poses 
    def entry1_callback(self, msg):
        self.entry1_pose = msg.pose
        new_msg = self.transform_world_to_camera(self.entry1_pose)
        if new_msg is not None:
            self.entry1_publisher_.publish(new_msg)

    # Callback function for new exit 1 poses 
    def exit1_callback(self, msg):
        self.exit1_pose = msg.pose
        new_msg = self.transform_world_to_camera(self.exit1_pose)
        if new_msg is not None:
            self.exit1_publisher_.publish(new_msg)

    # Callback function for new entry 2 poses 
    def entry2_callback(self, msg):
        self.entry2_pose = msg.pose
        new_msg = self.transform_world_to_camera(self.entry2_pose)
        if new_msg is not None:
            self.entry2_publisher_.publish(new_msg)

    # Callback function for new exit 2 poses 
    def exit2_callback(self, msg):
        self.exit2_pose = msg.pose
        new_msg = self.transform_world_to_camera(self.exit2_pose)
        if new_msg is not None:
            self.exit2_publisher_.publish(new_msg)

    # Callback function for new entry 3 poses 
    def entry3_callback(self, msg):
        self.entry3_pose = msg.pose
        new_msg = self.transform_world_to_camera(self.entry3_pose)
        if new_msg is not None:
            self.entry3_publisher_.publish(new_msg)

    # Callback function for new exit 3 poses 
    def exit3_callback(self, msg):
        self.exit3_pose = msg.pose
        new_msg = self.transform_world_to_camera(self.exit3_pose)
        if new_msg is not None:
            self.exit3_publisher_.publish(new_msg)

    # Callback function for new entry 4 poses 
    def entry4_callback(self, msg):
        self.entry4_pose = msg.pose
        new_msg = self.transform_world_to_camera(self.entry4_pose)
        if new_msg is not None:
            self.entry4_publisher_.publish(new_msg)

    # Callback function for new exit 4 poses 
    def exit4_callback(self, msg):
        self.exit4_pose = msg.pose
        new_msg = self.transform_world_to_camera(self.exit4_pose)
        if new_msg is not None:
            self.exit4_publisher_.publish(new_msg)


    # Callback function that stores camera pose in world frame 
    def camera_callback(self, msg):
        self.camera_pose = msg.pose


    # Function that transforms the given pose position into the camera frame 
    def transform_world_to_camera(self, pose):

        if pose is None or self.camera_pose is None:
            return


        # ----- Convert poses to pykdl format -----

        T_pose_world = pose_to_pykdl(pose)


        T_camera_world = pose_to_pykdl(self.camera_pose)
        

        # ----- Calculate the pose position in the camera frame -----

        T_pose_camera = (
            T_camera_world.Inverse()
            *
            T_pose_world
        )

        # ----- Create a new outgoing message -----

        new_pose = PoseStamped()

        new_pose.header.frame_id = "camera"

        new_pose.header.stamp = self.get_clock().now().to_msg()

        new_pose.pose = pykdl_to_pose(T_pose_camera)

        return new_pose


# ---------------------------------------- Main ----------------------------------------


def main(args=None):
    rclpy.init(args=args)

    simulation_to_ecm = SimulationECM()

    rclpy.spin(simulation_to_ecm)

    # Destroy the node explicitly
    simulation_to_ecm.destroy_node()
    rclpy.shutdown()


