

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


# --------------------------------------------- Helper Class ---------------------------------------------


# Calculates the grasp pose
class GraspPoseCalculator:
    def __init__(self, node):
        self.node = node

    # get grasp offset parameters
    def get_grasp_offset(self, psm, grasp_type):
        prefix = f'grasp_offsets.{psm}.{grasp_type}'

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

        offset = self.get_grasp_offset(psm, grasp_type)
        needle_frame = pose_to_pykdl(needle_pose.pose)
        base_frame = pose_to_pykdl(base_pose)

        needle_in_base = base_frame.Inverse() * needle_frame
        tool_frame = needle_in_base * offset

        approach_offset = Frame(
            Rotation.Identity(),
            Vector(0, 0, 0.01)
        )

        approach_in_world = needle_frame * approach_offset * offset
        approach_frame = base_frame.Inverse() * approach_in_world

        grasp_pose = PoseStamped()
        grasp_pose.header.frame_id = 'psm2/baselink'
        grasp_pose.pose = pykdl_to_pose(tool_frame)

        approach_pose = PoseStamped()
        approach_pose.header.frame_id = 'psm2/baselink'
        approach_pose.pose = pykdl_to_pose(approach_frame)

        return grasp_pose, approach_pose


# ------------------------------------------ Grasp Needle Node -------------------------------------------


class GraspNeedle(Node):
    def __init__(self):
        super().__init__('grasp_needle', automatically_declare_parameters_from_overrides=True)


        # ------------------------------ Variables ------------------------------

        self.arm_pose = None
        self.latest_needle_pose = None
        self.latest_base_pose = None
        self.grasp_calculator = GraspPoseCalculator(self)


        # ------------------------------ Subscriptions ------------------------------

        self.arm_meas = self.create_subscription(
            PoseStamped,
            '/CRTK/psm2/measured_cp',
            self.arm_pos_callback,
            10
        )

        self.base_pose_meas = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm2/baselink/State',
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

        self.arm_pub = self.create_publisher(
            PoseStamped,
            '/CRTK/psm2/servo_cp',
            10
        )

        self.jaw_pub = self.create_publisher(
            JointState,
            '/CRTK/psm2/jaw/servo_jp',
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
            self.latest_needle_pose,
            self.latest_base_pose
        )

    # store the latest arm pose
    def arm_pos_callback(self, msg):
        self.arm_pose = msg.pose
    
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

    # store the latest base pose
    def base_pos_callback(self, msg):
        self.latest_base_pose = msg.pose

    # store the latest needle pose
    def needle_state_callback(self, msg):
        self.latest_needle_pose = msg
        self.get_logger().debug(
            f'Updated needle pose: '
            f'{msg.pose.position.x}, '
            f'{msg.pose.position.y}, '
            f'{msg.pose.position.z}'
        )

    # run until initial pose data is received
    def ensure_initial_data(self):
        while (
            self.latest_needle_pose is None or
            self.latest_base_pose is None or
            self.arm_pose is None
        ):
            self.get_logger().info('Waiting for initial pose data...')
            rclpy.spin_once(self, timeout_sec=0.1)


# ---------------------------------------- Move to pose function -----------------------------------------


def move_to_pose(node, target_pose, step_name, timeout_scale=50):

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

        # find current arm pose
        current_pose = pose_to_pykdl(node.arm_pose)

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

        # -------------------- Apply step to arm -------------------- 

        next_step = Frame()
        next_step.p = current_pose.p + T_delta.p
        next_step.M = current_pose.M * T_delta.M
        next_pose = pykdl_to_posestamped(next_step, 'psm2/baselink')
        node.arm_pub.publish(next_pose)
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
    grasp_needle_node = GraspNeedle()

    if len(sys.argv) < 3:
        grasp_needle_node.get_logger().error(
            'Usage: ros2 run auto_suture grasp_needle <psm> <grasp_type>'
        )
        grasp_needle_node.destroy_node()
        rclpy.shutdown()
        return

    # check initial data is not None
    grasp_needle_node.ensure_initial_data()

    try:
        grasp_pose, approach_pose = grasp_needle_node.calculate_grasp_pose(
            sys.argv[1],
            sys.argv[2]
        )
    except ValueError as exc:
        grasp_needle_node.get_logger().error(str(exc))
        grasp_needle_node.destroy_node()
        rclpy.shutdown()
        return

    # -------------------- Move to approach pose --------------------

    target_pose = posestamped_to_pykdl(approach_pose)
    grasp_needle_node.get_logger().info(f'\nMoving to approach pose:\n{target_pose}')
    move_to_pose(grasp_needle_node, target_pose, 'Approach Pose')

    # -------------------- Open jaws --------------------

    grasp_needle_node.set_jaw(0.5)
    grasp_needle_node.get_logger().info('\nOpening jaws')
    rclpy.spin_once(grasp_needle_node, timeout_sec=0.01)

    # -------------------- Move to grasp pose --------------------

    target_pose = posestamped_to_pykdl(grasp_pose)
    grasp_needle_node.get_logger().info(f'\nMoving to grasp pose:\n{target_pose}')
    move_to_pose(grasp_needle_node, target_pose, 'Grasp Pose')

    for _ in range(50):
        rclpy.spin_once(grasp_needle_node, timeout_sec=0.01)

    # -------------------- Close jaws --------------------

    grasp_needle_node.set_jaw(0.0)
    grasp_needle_node.get_logger().info('\nClosing jaws')
    for _ in range(50):
        rclpy.spin_once(grasp_needle_node, timeout_sec=0.01)

    # -------------------- Create target pose above the current pose --------------------

    current_pose = pose_to_pykdl(grasp_needle_node.arm_pose)
    base_pose_in_world = pose_to_pykdl(grasp_needle_node.latest_base_pose)
    current_pose_world = base_pose_in_world * current_pose
    translation_offset = Vector(0.0, 0.0, -0.05)
    rotation_offset = Rotation.RotZ(0.0)
    offset = Frame(rotation_offset, translation_offset)
    target_pose_world = current_pose_world * offset
    target_pose = base_pose_in_world.Inverse() * target_pose_world

    # -------------------- Move upwards --------------------

    grasp_needle_node.get_logger().info(f'\nMoving to pose:\n{target_pose}')
    move_to_pose(grasp_needle_node, target_pose, 'Pick Up Needle', timeout_scale=20)

    # -------------------- Shutdown --------------------
    
    grasp_needle_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
