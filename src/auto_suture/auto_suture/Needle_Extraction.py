

# ---------------------------------------- Imports ----------------------------------------


import rclpy
import sys
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from ambf_msgs.msg import RigidBodyState
from sensor_msgs.msg import JointState
import PyKDL
from PyKDL import Frame, Rotation, Vector
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, pykdl_to_posestamped
from auto_suture.Move_To_Pose import move_to_pose
from auto_suture.Needle_Driving import generate_needle_arc_trajectory, _normalize, _kdl_vec_to_np


# ---------------------------------------- Needle extraction node ----------------------------------------


class NeedleExtraction(Node):

    def __init__(self, psm='psm1'):
        super().__init__(f'needle_extraction_{psm}')
        self.psm = psm

        # ------------------------------ Variables ------------------------------

        self.needle_to_point_offset = Frame(
            Rotation.RPY(0., 0., -0.688), 
            Vector(0.00661780871450901, 0.0069734565913677216, 0.0)
        )# note that y axis follows tangent of needle point

        self.needle_in_world = None
        
        self.needle_point_in_world = None

        self.exit1_in_world = None

        self.entry1_in_world = None

        self.base_in_world = None

        self.needle_entry_in_world = None

        self.needle_exit_in_world = None

        self.gripper_in_base = None


        # ------------------------------ Subscribers ------------------------------

        # Needle pose in world frame
        self.needle_sub = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_world_frame',
            self.needle_sub_callback,
            10
        )

        # Exit 1 pose in world frame
        self.exit1_sub = self.create_subscription(
            PoseStamped,
            '/exit1_pose_in_world_frame',
            self.exit1_sub_callback,
            10
        )

        # Entry 1 pose in world frame
        self.entry1_sub = self.create_subscription(
            PoseStamped,
            '/entry1_pose_in_world_frame',
            self.entry1_sub_callback,
            10
        )

        self.base_pose_meas = self.create_subscription(
            RigidBodyState,
            f'/ambf/env/{self.psm}/baselink/State',
            self.base_pos_callback,
            10
        )

        self.gripper_meas = self.create_subscription(
            PoseStamped,
            f'/CRTK/{self.psm}/measured_cp',
            self.gripper_pos_callback,
            10
        )
        

        # ------------------------------ Publishers ------------------------------

        # publisher to gripper pose in base frame
        self.gripper_pub = self.create_publisher(
            PoseStamped,
            f'/CRTK/{self.psm}/servo_cp',
            10
        )
        
        self.jaw_pub = self.create_publisher(
            JointState,
            f'/CRTK/{self.psm}/jaw/servo_jp',
            10
        )

        self.jaw_angle = 0.0
        self.jaw_timer = self.create_timer(0.1, self.publish_jaw)


    # ------------------------------ Callback Functions ------------------------------

    # Store needle pose in world frame as pykdl
    def needle_sub_callback(self, msg):
        self.needle_in_world = pose_to_pykdl(msg.pose)

        self.find_needle_point(self.needle_in_world)



    # Store exit 1 pose in world frame as pykdl
    def exit1_sub_callback(self, msg):
        self.exit1_in_world = pose_to_pykdl(msg.pose)


    # Store exit 1 pose in world frame as pykdl
    def entry1_sub_callback(self, msg):
        self.entry1_in_world = pose_to_pykdl(msg.pose)


    # store the latest base pose as pykdl
    def base_pos_callback(self, msg):
        self.base_in_world = pose_to_pykdl(msg.pose)


    # store the latest gripper pose as pykdl
    def gripper_pos_callback(self, msg):
        self.gripper_in_base = pose_to_pykdl(msg.pose)

    
    # ------------------------------- Other Functions -------------------------------

    # Finds the needle point pose in world frame
    def find_needle_point(self, needle_in_world):

        self.needle_point_in_world = needle_in_world * self.needle_to_point_offset



    # run until initial pose data is received
    def ensure_initial_data(self):
        while (
            self.needle_point_in_world is None or
            self.entry1_in_world is None or
            self.exit1_in_world is None or
            self.base_in_world is None or
            self.gripper_in_base is None
        ):
            self.get_logger().info('Waiting for initial pose data...')
            rclpy.spin_once(self, timeout_sec=0.1)

    def get_needle_entry_exit_poses(self, entry, exit_):
        self.needle_entry_in_world = Frame()
        self.needle_exit_in_world = Frame()

        self.needle_entry_in_world.p = entry.p + Vector(-0.003, 0.0, 0.0025)
        self.needle_exit_in_world.p = exit_.p + Vector(0.003, 0.0, 0.0025)

        self.needle_entry_in_world.M = entry.M * Rotation.RPY(-1.570796327, 1.570796327, 0)
        self.needle_exit_in_world.M = exit_.M * Rotation.RPY(-1.570796327, -1.570796327, 0)

    # publish jaw angle to jaw servo
    def publish_jaw(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['jaw']
        msg.position = [self.jaw_angle]

        self.jaw_pub.publish(msg)

    # set the jaw angle
    def set_jaw(self, angle):
        self.jaw_angle = angle




# ----------------------------------------------- Main ------------------------------------------------


def main():
    rclpy.init()
    # Optional CLI arg: psm (psm1 or psm2). Default to psm1.
    psm = 'psm1'
    if len(sys.argv) > 1:
        psm = sys.argv[1]

    node = NeedleExtraction(psm=psm)


    # check initial data is not None
    node.ensure_initial_data()
    node.get_logger().info('\nData received')

    # find needle point from gripper perspective 
    # this stays constant while needle is grasped 
    # it is used to figure out the required gripper pose for needle to follow the given trajectory

    needle_point_in_gripper = node.gripper_in_base.Inverse() * node.base_in_world.Inverse() * node.needle_point_in_world


    # -------------------- Get exit pose --------------------

    # Get entry and exit poses
    node.get_needle_entry_exit_poses(
        node.entry1_in_world,
        node.exit1_in_world
    )

    # -------------------- Define target pose --------------------

    # define transformation between start and end in driving:
    T = node.needle_exit_in_world * node.needle_entry_in_world.Inverse()

    # define target = apply transform again twice, starting at end point this time
    target_frame = T * T * node.needle_exit_in_world

    # define offset
    offset = Frame(
        Rotation.RPY(0.0, 0.0, -0.01),
        Vector(0.0, 0.0, 0.0)
    )

    # Apply offset 
    target_pose = target_frame * offset

    # -------------------- Generate extraction path --------------------

    # Generate arc steps
    extraction_path = generate_needle_arc_trajectory(node.needle_exit_in_world, target_pose, num_steps=100)


    node.get_logger().info('\nNeedle extraction sequence')


    for f in extraction_path:

        # get the target pose of the gripper in the base frame
        target_gripper_in_base = node.base_in_world.Inverse() * f * needle_point_in_gripper.Inverse()

        predicted_needle_point = (
            node.base_in_world
            * target_gripper_in_base
            * needle_point_in_gripper
        )


        target = pykdl_to_posestamped(target_gripper_in_base, f"{node.psm}/baselink")

        node.gripper_pub.publish(target)
        for _ in range(100):
            rclpy.spin_once(node, timeout_sec=0.01)


    node.get_logger().info('\nNeedle extraction complete...\n\n')    

    # -------------------- Shutdown --------------------
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


