

# ---------------------------------------- Imports ----------------------------------------


import sys
import rclpy
from rclpy.node import Node
import time
import matplotlib.pyplot as plt

from datetime import datetime
from PyKDL import Vector, Rotation, Frame
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, posestamped_to_pykdl, pykdl_to_posestamped
from utility.utilities import cartesian_interpolate_step, save_error_plot
from ambf_msgs.msg import RigidBodyState
from auto_suture.Move_To_Pose import move_to_pose


# --------------------------------------------- Helper Class ---------------------------------------------


# Calculates the grasp pose
class GraspPoseCalculator:
    def __init__(self, node):
        self.node = node

    # get grasp offset parameters
    def get_grasp_offset(self, psm, grasp_type, is_upside_down):
        prefix = f'grasp_offsets.{psm}.{grasp_type}.{is_upside_down}'

        x = self.node.get_parameter(prefix + '.position.x').value
        y = self.node.get_parameter(prefix + '.position.y').value
        z = self.node.get_parameter(prefix + '.position.z').value
        roll = self.node.get_parameter(prefix + '.orientation.roll').value
        pitch = self.node.get_parameter(prefix + '.orientation.pitch').value
        yaw = self.node.get_parameter(prefix + '.orientation.yaw').value

        return Frame(
            Rotation.RPY(roll, pitch, yaw),
            Vector(x, y, z)
        )

    # apply grasp offsets to find grasp pose of the tool in the baselink frame
    def compute_grasp_pose(self, psm, grasp_type, needle_pose, base_pose):
        if needle_pose is None:
            raise ValueError('No needle pose received yet')
        if base_pose is None:
            raise ValueError('No base pose received yet')
        
        needle_frame = needle_pose

        base_frame = base_pose

        if needle_frame.M[2, 2] < 0:
            # needle is upside down
            is_upside_down = "down"
            approach_offset = Frame(
                Rotation.Identity(),
                Vector(0.0, 0.0, -0.02)
            )
        else:
            # needle is facing up
            is_upside_down = "up"
            approach_offset = Frame(
                Rotation.Identity(),
                Vector(0.0, 0.0, 0.01)
            )

        offset = self.get_grasp_offset(psm, grasp_type, is_upside_down)

        needle_in_base = base_frame.Inverse() * needle_frame
        tool_frame = needle_in_base * offset

        

        approach_in_world = needle_frame * approach_offset * offset
        approach_frame = base_frame.Inverse() * approach_in_world
    


        return tool_frame, approach_frame


# ------------------------------------------ Grasp Needle Node -------------------------------------------


class GraspNeedle(Node):
    def __init__(self, psm='psm2'):
        super().__init__(f'grasp_needle_{psm}', automatically_declare_parameters_from_overrides=True)
        self.psm = psm


        # ------------------------------ Variables ------------------------------

        self.gripper_in_base = None
        self.needle_in_world = None
        self.base_in_world = None
        self.grasp_calculator = GraspPoseCalculator(self)


        # ------------------------------ Subscriptions ------------------------------

        self.gripper_meas = self.create_subscription(
            PoseStamped,
            f'/CRTK/{self.psm}/measured_cp',
            self.gripper_pos_callback,
            10
        )

        self.base_pose_meas = self.create_subscription(
            RigidBodyState,
            f'/ambf/env/{self.psm}/baselink/State',
            self.base_pos_callback,
            10
        )

        self.needle_sub = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_world_frame',
            self.needle_state_callback,
            10
        )


        # ------------------------------ Publishers ------------------------------

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

        self.jaw_angle = 0.5
        self.jaw_timer = self.create_timer(0.1, self.publish_jaw)


        # ------------------------------ Functions ------------------------------
    
    # call grasp calculator to find the grasp pose
    def calculate_grasp_pose(self, psm, grasp_type):
        return self.grasp_calculator.compute_grasp_pose(
            psm,
            grasp_type,
            self.needle_in_world,
            self.base_in_world
        )

    # store the latest gripper pose as pykdl
    def gripper_pos_callback(self, msg):
        self.gripper_in_base = pose_to_pykdl(msg.pose)
    
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

    # store the latest base pose as pykdl
    def base_pos_callback(self, msg):
        self.base_in_world = pose_to_pykdl(msg.pose)

    # store the latest needle pose as pykdl
    def needle_state_callback(self, msg):
        self.needle_in_world = pose_to_pykdl(msg.pose)
        self.get_logger().debug(
            f'Updated needle pose: '
            f'{msg.pose.position.x}, '
            f'{msg.pose.position.y}, '
            f'{msg.pose.position.z}'
        )

    # run until initial pose data is received
    def ensure_initial_data(self):
        self.get_logger().info('Waiting for initial pose data...')
        while (
            self.needle_in_world is None or
            self.base_in_world is None or
            self.gripper_in_base is None
        ):
            
            rclpy.spin_once(self, timeout_sec=0.1)




# ------------------------------------------------- Main -------------------------------------------------


def main():
    rclpy.init()
    
    if len(sys.argv) < 3:
        # No node created yet, create a temporary node to log the error
        tmp_node = GraspNeedle()
        tmp_node.get_logger().error(
            'Usage: ros2 run auto_suture grasp_needle <psm> <grasp_type>'
        )
        tmp_node.destroy_node()
        rclpy.shutdown()
        return

    psm = sys.argv[1]
    grasp_type = sys.argv[2]

    if psm not in ('psm1', 'psm2'):
        tmp_node = GraspNeedle()
        tmp_node.get_logger().error(f'Invalid psm "{psm}". Expected "psm1" or "psm2"')
        tmp_node.destroy_node()
        rclpy.shutdown()
        return

    if grasp_type not in ('grip', 'tip'):
        tmp_node = GraspNeedle()
        tmp_node.get_logger().error(f'Invalid grasp_type "{grasp_type}". Expected "grip" or "tip"')
        tmp_node.destroy_node()
        rclpy.shutdown()
        return

    node = GraspNeedle(psm=psm)

    # check initial data is not None
    node.ensure_initial_data()

    try:
        grasp_pose, approach_pose = node.calculate_grasp_pose(
            psm,
            grasp_type
        )
    except ValueError as exc:
        node.get_logger().error(str(exc))
        node.destroy_node()
        rclpy.shutdown()
        return

    # -------------------- Move to approach pose --------------------

    target_pose = node.base_in_world * approach_pose
    node.get_logger().info(f'\nMoving to approach pose:\n{target_pose}')
    move_to_pose('absolute', target_pose, 'Approach Pose', psm=psm, max_translation=0.008, max_rotation=0.15)

    # -------------------- Open jaws --------------------

    node.set_jaw(0.5)
    node.get_logger().info('\nOpening jaws')
    rclpy.spin_once(node, timeout_sec=0.01)

    # -------------------- Move to grasp pose --------------------

    target_pose = node.base_in_world * grasp_pose
    node.get_logger().info(f'\nMoving to grasp pose:\n{target_pose}')
    move_to_pose('absolute', target_pose, 'Grasp Pose', psm=psm)

    for _ in range(100):
        rclpy.spin_once(node, timeout_sec=0.01)

    # -------------------- Close jaws --------------------

    node.set_jaw(0.0)
    node.get_logger().info('\nClosing jaws')
    for _ in range(100):
        rclpy.spin_once(node, timeout_sec=0.01)

    # -------------------- Shutdown --------------------
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
