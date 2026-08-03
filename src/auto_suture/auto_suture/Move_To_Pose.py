


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
        return target_spec

    if isinstance(target_spec, (list, tuple)):
        values = [float(value) for value in target_spec]
    elif isinstance(target_spec, str):
        text = target_spec.strip()
        values = [float(value) for value in text.replace(',', ' ').split() if value]
    else:
        raise ValueError('Target pose must be a PyKDL Frame or six numeric values')

    if len(values) != 6:
        raise ValueError(
            'Target pose must contain six values: x y z roll pitch yaw'
        )

    x, y, z, roll, pitch, yaw = values
    translation = Vector(x, y, z)
    rotation = Rotation.RPY(roll, pitch, yaw)
    return Frame(rotation, translation)


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


        # ------------------------------ Functions ------------------------------
    

    # store the latest gripper pose as pykdl
    def gripper_pos_callback(self, msg):
        self.gripper_in_base = pose_to_pykdl(msg.pose)
    

    # store the latest base pose as pykdl
    def base_pos_callback(self, msg):
        self.base_in_world = pose_to_pykdl(msg.pose)


    # run until initial pose data is received
    def ensure_initial_data(self):
        while (
            self.base_in_world is None or
            self.gripper_in_base is None
        ):
            self.get_logger().info('Waiting for initial pose data...')
            rclpy.spin_once(self, timeout_sec=0.1)



# ---------------------------------------- Move to pose function -----------------------------------------



def move_to_pose(node, target_pose, step_name, timeout_scale=50, psm='psm2'):

    # -------------------- Blank array for error logging --------------------
    times = []
    trans_errors = []
    rot_errors = []
    start_time = time.time()

    previous_error = float('inf')
    moving_away_count = 0
    done = False
    # -------------------- Movement stage --------------------
    while not done:

        # find current gripper pose
        current_pose = node.gripper_in_base

        # calcualte next step to reach goal pose
        T_delta, done, trans_error_mag, rot_error_mag, deadband, rot_deadband, max_translation, max_rotation = cartesian_interpolate_step(
            current_pose,
            target_pose
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


# ------------------------------------------------- Main -------------------------------------------------



def main():
    rclpy.init()

    if len(sys.argv) < 3:
        tmp_node = MoveToPose()
        tmp_node.get_logger().error(
            'Usage: ros2 run auto_suture move_to_pose <psm> <x> <y> <z> <roll> <pitch> <yaw>\n'
            'or: ros2 run auto_suture move_to_pose <psm> "x,y,z,roll,pitch,yaw"'
        )
        tmp_node.destroy_node()
        rclpy.shutdown()
        return

    psm = sys.argv[1]

    if psm not in ('psm1', 'psm2'):
        tmp_node = MoveToPose()
        tmp_node.get_logger().error(f'Invalid psm "{psm}". Expected "psm1" or "psm2"')
        tmp_node.destroy_node()
        rclpy.shutdown()
        return

    try:
        if len(sys.argv) == 3:
            target_pose = parse_target_pose(sys.argv[2])
        else:
            target_pose = parse_target_pose(sys.argv[2:8])
    except ValueError as exc:
        tmp_node = MoveToPose(psm=psm)
        tmp_node.get_logger().error(str(exc))
        tmp_node.destroy_node()
        rclpy.shutdown()
        return

    move_to_pose_node = MoveToPose(psm=psm)

    # check initial data is not None
    move_to_pose_node.ensure_initial_data()

    # -------------------- Move to target --------------------

    move_to_pose_node.get_logger().info(f'\nMoving to pose:\n{target_pose}')
    move_to_pose(move_to_pose_node, target_pose, 'Requested Pose', timeout_scale=20, psm=psm)

    # -------------------- Shutdown --------------------

    move_to_pose_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
