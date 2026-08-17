


# ------------------------------ Imports ------------------------------


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from ambf_msgs.msg import RigidBodyState, GhostObjectState
from utility.transform_functions import pose_to_pykdl
from auto_suture.Move_To_Pose import move_to_pose
from auto_suture.controller import run_step, start_step
from PyKDL import Vector, Rotation, Frame




# ------------------------------ Node definition ------------------------------


class Handover(Node):
    def __init__(self):
        super().__init__('handover')
        
        # -------------------- Variables --------------------

        self.psm1_gripper_in_base = None
        self.psm2_gripper_in_base = None
        self.psm1_base_in_world = None
        self.psm2_base_in_world = None
        self.needle_in_world = None
        
        # define target needle handover pose in world frame:
        self.needle_target_in_world = Frame(
            Rotation.RPY(0.0, 0.0, 0.0),
            Vector(0.01, 0.2, 0.71)
        )

        self.psm1_left_has_needle = False
        self.psm1_right_has_needle = False
        self.psm2_left_has_needle = False
        self.psm2_right_has_needle = False

        self.has_needle = None


        # -------------------- Subscriptions --------------------

        self.psm1_meas = self.create_subscription(
            PoseStamped,
            '/CRTK/psm1/measured_cp',
            self.psm1_gripper_callback,
            10
        )

        self.psm2_meas = self.create_subscription(
            PoseStamped,
            '/CRTK/psm2/measured_cp',
            self.psm2_gripper_callback,
            10
        )

        self.psm1_base_meas = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm1/baselink/State',
            self.psm1_base_callback,
            10
        )

        self.psm2_base_meas = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm2/baselink/State',
            self.psm2_base_callback,
            10
        )

        self.needle_meas = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_world_frame',
            self.needle_callback,
            10
        )

        self.psm1_left_finger = self.create_subscription(
            GhostObjectState,
            '/ambf/env/ghosts/psm1/left_finger_ghost/State',
            lambda msg: self.finger_callback(msg, 'psm1_left'),
            10
        )

        self.psm1_right_finger = self.create_subscription(
            GhostObjectState,
            '/ambf/env/ghosts/psm1/right_finger_ghost/State',
            lambda msg: self.finger_callback(msg, 'psm1_right'),
            10
        )

        self.psm2_left_finger = self.create_subscription(
            GhostObjectState,
            '/ambf/env/ghosts/psm2/left_finger_ghost/State',
            lambda msg: self.finger_callback(msg, 'psm2_left'),
            10
        )

        self.psm2_right_finger = self.create_subscription(
            GhostObjectState,
            '/ambf/env/ghosts/psm2/right_finger_ghost/State',
            lambda msg: self.finger_callback(msg, 'psm2_right'),
            10
        )



    # -------------------- Callback functions --------------------

    def psm1_gripper_callback(self, msg):
        self.psm1_gripper_in_base = pose_to_pykdl(msg.pose)

    def psm2_gripper_callback(self, msg):
        self.psm2_gripper_in_base = pose_to_pykdl(msg.pose)
        
    def psm1_base_callback(self, msg):
        self.psm1_base_in_world = pose_to_pykdl(msg.pose)

    def psm2_base_callback(self, msg):
        self.psm2_base_in_world = pose_to_pykdl(msg.pose)

    def needle_callback(self, msg):
        self.needle_in_world = pose_to_pykdl(msg.pose)
    
    def finger_callback(self, msg, finger):

        has_needle = any(
            obj.data == '/ambf/env/phantom/BODY Needle'
            for obj in msg.sensed_objects
        )

        if finger == 'psm1_left':
            self.psm1_left_has_needle = has_needle

        elif finger == 'psm1_right':
            self.psm1_right_has_needle = has_needle

        elif finger == 'psm2_left':
            self.psm2_left_has_needle = has_needle

        elif finger == 'psm2_right':
            self.psm2_right_has_needle = has_needle

        # Check the pairs
        if (
            self.psm1_left_has_needle
            and self.psm1_right_has_needle
            and self.psm2_left_has_needle
            and self.psm2_right_has_needle
        ):
            self.has_needle = 'both'

        elif self.psm1_left_has_needle or self.psm1_right_has_needle:
            self.has_needle = 'psm1'

        elif self.psm2_left_has_needle or self.psm2_right_has_needle:
            self.has_needle = 'psm2'

        else:
            self.has_needle = None


        # -------------------- Other functions --------------------

    # run until initial pose data is received
    def ensure_initial_data(self):
        self.get_logger().info('Waiting for initial pose data...')
        while (
            self.psm1_gripper_in_base is None or
            self.psm2_gripper_in_base is None or
            self.psm1_base_in_world is None or
            self.psm2_base_in_world is None or
            self.needle_in_world is None or
            self.has_needle is None
        ):
            
            rclpy.spin_once(self, timeout_sec=0.1)        


# ------------------------------ Main ------------------------------


def main():
    rclpy.init()

    node = Handover()

    # wait for initial data
    node.ensure_initial_data()
    node.get_logger().info('\nData received\n')

    node.get_logger().info(f'\n{node.has_needle} has the needle\n')

    if node.has_needle == 'psm1':
        # PSM1 has needle


        # command psm2 to grasp needle at the grip
        run_step([
            "ros2", "run", "auto_suture",
            "Grasp_Needle",
            "psm2",
            "grip",
            "up",
            "--ros-args",
            "--params-file",
            "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
        ])

        # command psm2 to hold needle
        psm2_grab_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm2",
            "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
        ])

        # command psm1 to let go
        psm1_drop_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm1",
            "0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.5"
        ])

        psm1_drop_needle.wait()
        psm2_grab_needle.wait()

    elif node.has_needle == 'psm2':
        # PSM2 has needle


        # command psm1 to grasp needle at the tip
        run_step([
            "ros2", "run", "auto_suture",
            "Grasp_Needle",
            "psm1",
            "tip",
            "up",
            "--ros-args",
            "--params-file",
            "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
        ])

        # command psm1 to hold needle
        psm1_grab_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm1",
            "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
        ])

        # command psm2 to let go
        psm2_drop_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm2",
            "0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.5"
        ])

        psm2_drop_needle.wait()
        psm1_grab_needle.wait()

    else:
        # both have the needle
        
        # command psm2 to hold needle
        psm2_grab_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm2",
            "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
        ])

        # command psm1 to let go
        psm1_drop_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm1",
            "0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.5"
        ])

        psm1_drop_needle.wait()
        psm2_grab_needle.wait()



    
    
    
    # -------------------- Shutdown --------------------
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()