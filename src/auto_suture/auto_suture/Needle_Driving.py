

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


# ---------------------------------------- Needle driving node ----------------------------------------


class NeedleDriving(Node):

    def __init__(self, psm='psm2', entry_exit_number=1):
        super().__init__(f'needle_driving_{psm}')
        self.psm = psm
        self.entry_exit_number = entry_exit_number

        # ------------------------------ Variables ------------------------------

        self.needle_to_point_offset = Frame(
            Rotation.RPY(0., 0., -0.688), 
            Vector(0.00661780871450901, 0.0069734565913677216, 0.0)
        )# note that y axis follows tangent of needle point

        self.needle_in_world = None
        
        self.needle_point_in_world = None

        self.entry_in_world = None

        self.exit_in_world = None

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

        # Entry 1 pose in world frame
        self.entry_sub = self.create_subscription(
            PoseStamped,
            f'/entry{self.entry_exit_number}_pose_in_world_frame',
            self.entry_sub_callback,
            10
        )

        # Exit 1 pose in world frame
        self.exit_sub = self.create_subscription(
            PoseStamped,
            f'/exit{self.entry_exit_number}_pose_in_world_frame',
            self.exit_sub_callback,
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


    # Store entry 1 pose in world frame as pykdl
    def entry_sub_callback(self, msg):
        self.entry_in_world = pose_to_pykdl(msg.pose)


    # Store exit 1 pose in world frame as pykdl
    def exit_sub_callback(self, msg):
        self.exit_in_world = pose_to_pykdl(msg.pose)


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
        self.get_logger().info('Waiting for initial pose data...')
        while (
            self.needle_point_in_world is None or
            self.entry_in_world is None or
            self.exit_in_world is None or
            self.base_in_world is None or
            self.gripper_in_base is None
        ):
            
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


# ------------------------------------------- Arc Path Planning -------------------------------------------

 
def _normalize(v):
    n = np.linalg.norm(v)
    if n < 1e-12:
        return v
    return v / n
 
 
def _kdl_vec_to_np(v):
    return np.array([v.x(), v.y(), v.z()])
  


# Generate a circular arc of fixed needle radius between two poses.
# The trajectory assumes the needle point moves on a circle with the known
# needle radius while the orientation rotates rigidly with the motion.

def generate_needle_arc_trajectory(start_frame, end_frame, num_steps=100):

    needle_radius = 0.01018  # metres

    # -------------------- Extract positions --------------------

    start_pos = _kdl_vec_to_np(start_frame.p)
    end_pos = _kdl_vec_to_np(end_frame.p)

    # -------------------- Rotation axis --------------------

    rel_rot = end_frame.M * start_frame.M.Inverse()
    _, axis_kdl = rel_rot.GetRotAngle()
    axis = _normalize(_kdl_vec_to_np(axis_kdl))

    # -------------------- Chord geometry --------------------

    chord = end_pos - start_pos

    # Only use the component lying in the plane of rotation
    chord_in_plane = chord - np.dot(chord, axis) * axis
    chord_len = np.linalg.norm(chord_in_plane)

    if chord_len < 1e-9:
        return [start_frame] * num_steps

    if chord_len > 2.0 * needle_radius:
        raise ValueError(
            "Start and end points are farther apart than the needle diameter."
        )

    mid = start_pos + 0.5 * chord_in_plane

    perp = _normalize(np.cross(axis, chord_in_plane))

    dist_to_center = np.sqrt(
        needle_radius**2 - (chord_len / 2.0) ** 2
    )

    center = mid + dist_to_center * perp

    # -------------------- Radius vectors --------------------

    radius_vec0 = start_pos - center
    radius_vec1 = end_pos - center

    radius_vec0 = needle_radius * _normalize(radius_vec0)
    radius_vec1 = needle_radius * _normalize(radius_vec1)

    # -------------------- Sweep angle --------------------

    sweep_angle = np.arccos(
        np.clip(
            np.dot(
                _normalize(radius_vec0),
                _normalize(radius_vec1)
            ),
            -1.0,
            1.0
        )
    )

    # Determine clockwise / anticlockwise
    if np.dot(np.cross(radius_vec0, radius_vec1), axis) < 0:
        sweep_angle = -sweep_angle

    # -------------------- Generate trajectory --------------------

    frames = []

    for t in np.linspace(0.0, 1.0, num_steps):

        angle = sweep_angle * t

        rot = PyKDL.Rotation.Rot(
            PyKDL.Vector(*axis),
            angle
        )

        rotated_radius = _kdl_vec_to_np(
            rot * PyKDL.Vector(*radius_vec0)
        )

        pos = center + rotated_radius

        orientation = rot * start_frame.M

        frames.append(
            PyKDL.Frame(
                orientation,
                PyKDL.Vector(*pos)
            )
        )

    return frames

# ----------------------------------------------- Main ------------------------------------------------


def main():
    rclpy.init()

    # Defaults
    psm = "psm2"
    entry_exit_number = 1

    # Read command line arguments
    if len(sys.argv) > 1:
        psm = sys.argv[1]

    if len(sys.argv) > 2:
        entry_exit_number = int(sys.argv[2])

    node = NeedleDriving(
        psm=psm,
        entry_exit_number=entry_exit_number
    )
    

    # check initial data is not None
    node.ensure_initial_data()
    node.get_logger().info('\nData received')

    # find needle point from gripper perspective 
    # this stays constant while needle is grasped
    # it is used to figure out the required gripper pose for needle to follow the given trajectory

    needle_point_in_gripper = node.gripper_in_base.Inverse() * node.base_in_world.Inverse() * node.needle_point_in_world


    # -------------------- X --------------------

    # Get entry and exit poses
    node.get_needle_entry_exit_poses(
        node.entry_in_world,
        node.exit_in_world
    )

    # Generate arc steps
    driving_path = generate_needle_arc_trajectory(node.needle_entry_in_world, node.needle_exit_in_world, num_steps=100)

    # Generate approach pose
    approach_pose = Frame()
    approach_pose.p = node.needle_entry_in_world.p + Vector(-0.003, 0.0, 0.003)
    approach_pose.M = node.needle_entry_in_world.M

    # move to entry pose
    done = False

    target_gripper_in_base = node.base_in_world.Inverse() * approach_pose * needle_point_in_gripper.Inverse()

    target_gripper_in_world = node.base_in_world * target_gripper_in_base

  
    node.get_logger().info(f'\nMoving to start pose:\n{target_gripper_in_world}\n\n')
    move_to_pose('absolute', target_gripper_in_world, 'Needle Driving Start Pose', psm=node.psm)


    node.get_logger().info('\nNeedle driving sequence')


    for f in driving_path:

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


    node.get_logger().info('\nNeedle driving complete...\n\n')    

    # -------------------- Shutdown --------------------
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


