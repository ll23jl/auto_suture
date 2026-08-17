


# ------------------------------------------ Imports  -------------------------------------------

import sys
import rclpy
from rclpy.node import Node
import time
import matplotlib.pyplot as plt

from typing import Iterable

from datetime import datetime
from PyKDL import Vector, Rotation, Frame
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, posestamped_to_pykdl, pykdl_to_posestamped
from utility.utilities import cartesian_interpolate_step, save_error_plot
from ambf_msgs.msg import RigidBodyState

# ------------------------------------------ Check given target pose -------------------------------------------


def parse_target_pose(target_spec):
    if isinstance(target_spec, Frame):
        return target_spec, None

    if isinstance(target_spec, (list, tuple)):
        values = [float(value) for value in target_spec]
    elif isinstance(target_spec, str):
        text = target_spec.strip()
        values = [float(value) for value in text.replace(',', ' ').split() if value]
    else:
        raise ValueError('Target pose must be a PyKDL Frame or 6/7 numeric values')

    if len(values) not in (6, 7):
        raise ValueError(
            'Target pose must contain 6 values: x y z roll pitch yaw or 7 values with jaw_angle'
        )

    if len(values) == 6:
        x, y, z, roll, pitch, yaw = values
        jaw_angle = None
    else:
        x, y, z, roll, pitch, yaw, jaw_angle = values

    translation = Vector(x, y, z)
    rotation = Rotation.RPY(roll, pitch, yaw)
    return Frame(rotation, translation), jaw_angle


# ------------------------------------------ Move to Pose Node -------------------------------------------



class MoveToPose(Node):
    def __init__(self, psm='psm2'):
        super().__init__(f'move_to_pose_{psm}')
        self.psm = psm


        # ------------------------------ Variables ------------------------------

        self.gripper_in_base = None
        self.base_in_world = None


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

        self.jaw_angle = None
        self.jaw_timer = self.create_timer(0.1, self.publish_jaw)


        # ------------------------------ Functions ------------------------------
    

    # store the latest gripper pose as pykdl
    def gripper_pos_callback(self, msg):
        self.gripper_in_base = pose_to_pykdl(msg.pose)
    

    # store the latest base pose as pykdl
    def base_pos_callback(self, msg):
        self.base_in_world = pose_to_pykdl(msg.pose)


    # run until initial pose data is received
    def ensure_initial_data(self):
        self.get_logger().info('Waiting for initial pose data...')
        while (
            self.base_in_world is None or
            self.gripper_in_base is None
        ):
            
            rclpy.spin_once(self, timeout_sec=0.1)

    # publish jaw angle to jaw servo
    def publish_jaw(self):

        if self.jaw_angle is None:
            return

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['jaw']
        msg.position = [self.jaw_angle]

        self.jaw_pub.publish(msg)

    # set the jaw angle
    def set_jaw(self, angle):
        self.jaw_angle = angle


# ---------------------------------------- Move to pose function -----------------------------------------



def move_to_pose(move_type, target_pose, step_name, timeout_scale=50, psm='psm2',max_translation=0.005, max_rotation=0.1,jaw_angle=None):

    # -------------------- Blank array for error logging --------------------
    times = []
    trans_errors = []
    rot_errors = []
    start_time = time.time()

    previous_error = float('inf')
    moving_away_count = 0
    done = False

    node = MoveToPose(psm=psm)

    # Wait for this node to receive its own measurements
    node.ensure_initial_data()


    if move_type == 'absolute':
        # target pose in an absolute pose in the world frame

        target_pose_in_world = target_pose

        target_pose_in_base = node.base_in_world.Inverse() * target_pose_in_world

    elif move_type == 'relative':
        # target pose = offset from current pose in the world

        gripper_in_world = node.base_in_world * node.gripper_in_base

        target_pose_in_world = Frame(
            target_pose.M * gripper_in_world.M,
            gripper_in_world.p + target_pose.p
        )

        target_pose_in_base = node.base_in_world.Inverse() * target_pose_in_world

    else:
        # reject

        node.get_logger.error('\nWrong movement type. Expected relative or absolute.\n')
        return

    # -------------------- Jaw angle ----------------

    if jaw_angle is not None:
        node.set_jaw(jaw_angle)


    # -------------------- Movement stage --------------------
    while not done:

        # find current gripper pose
        current_pose = node.gripper_in_base

        # calcualte next step to reach goal pose
        T_delta, done, trans_error_mag, rot_error_mag, deadband, rot_deadband, max_translation, max_rotation = cartesian_interpolate_step(
            current_pose,
            target_pose_in_base,
            max_translation=max_translation,
            max_rotation=max_rotation,
        )

        # ------------- Error logging --------------

        times.append(time.time() - start_time)
        trans_errors.append(trans_error_mag)
        rot_errors.append(rot_error_mag)

        # ------------------------------------------
        # ---------- Check for divergence ----------

        if trans_error_mag >= previous_error:
            moving_away_count += 1
        else:
            moving_away_count = 0

        previous_error = trans_error_mag

        if time.time() - start_time > 10 and moving_away_count > timeout_scale:
            node.get_logger().error('Controller diverging - aborting movement.')
            break

        # -------------------- Apply step to gripper -------------------- 

        next_step = Frame()
        next_step.p = current_pose.p + T_delta.p
        next_step.M = current_pose.M * T_delta.M
        next_pose = pykdl_to_posestamped(next_step, f'{psm}/baselink')
        node.gripper_pub.publish(next_pose)
        rclpy.spin_once(node, timeout_sec=0.01)

    # -------------------- Plot errors --------------------
    filepath = save_error_plot(
        step_name=step_name,
        times=times,
        trans_errors=trans_errors,
        rot_errors=rot_errors,
        deadband=deadband,
        rot_deadband=rot_deadband,
        max_translation=max_translation,
        max_rotation=max_rotation,
        success=done
    )

    node.get_logger().info(f'Saved plot to {filepath}')


    # -------------------- Shutdown --------------------
    
    node.destroy_node()





# ------------------------------------------------- Main -------------------------------------------------



def main():
    rclpy.init()

    if len(sys.argv) < 3:
        print(
            'Usage: ros2 run auto_suture move_to_pose '
            '<psm> <x> <y> <z> <roll> <pitch> <yaw> [jaw_angle]'
        )
        rclpy.shutdown()
        return

    psm = sys.argv[1]

    if psm not in ('psm1', 'psm2'):
        print(
            f'Invalid psm "{psm}". Expected "psm1" or "psm2"'
        )
        rclpy.shutdown()
        return

    try:
        if len(sys.argv) == 3:
            target_pose_in_world, jaw_angle = parse_target_pose(
                sys.argv[2]
            )
        else:
            target_pose_in_world, jaw_angle = parse_target_pose(
                sys.argv[2:]
            )

    except ValueError as exc:
        print(str(exc))
        rclpy.shutdown()
        return

    # -------------------- Move --------------------

    
    move_to_pose(
        'relative',
        target_pose_in_world,
        'Requested Pose',
        timeout_scale=20,
        psm=psm,
        jaw_angle=jaw_angle
    )

    rclpy.shutdown()


if __name__ == '__main__':
    main()