

# ---------------------------------------- Imports ----------------------------------------


import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from ambf_msgs.msg import RigidBodyState
import PyKDL
from PyKDL import Frame, Rotation, Vector
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, pykdl_to_posestamped
from auto_suture.Grasp_Needle import move_to_pose


# ---------------------------------------- Needle driving node ----------------------------------------


class NeedleDriving(Node):

    def __init__(self):
        super().__init__('needle_driving')

        # ------------------------------ Variables ------------------------------

        self.needle_to_point_offset = Frame(
            Rotation.RPY(0., 0., -0.688), 
            Vector(0.00661780871450901, 0.0069734565913677216, 0.0)
        )# note that y axis follows tangent of needle point

        self.needle_in_world = None
        
        self.needle_point_in_world = None

        self.entry1_in_world = None

        self.exit1_in_world = None

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
        self.entry1_sub = self.create_subscription(
            PoseStamped,
            '/entry1_pose_in_world_frame',
            self.entry1_sub_callback,
            10
        )

        # Exit 1 pose in world frame
        self.exit1_sub = self.create_subscription(
            PoseStamped,
            '/exit1_pose_in_world_frame',
            self.exit1_sub_callback,
            10
        )

        self.base_pose_meas = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm2/baselink/State',
            self.base_pos_callback,
            10
        )

        self.gripper_meas = self.create_subscription(
            PoseStamped,
            '/CRTK/psm2/measured_cp',
            self.gripper_pos_callback,
            10
        )
        

        # ------------------------------ Publishers ------------------------------


        self.gripper_pub = self.create_publisher(
            PoseStamped,
            '/CRTK/psm2/servo_cp',
            10
        )


    # ------------------------------ Callback Functions ------------------------------

    # Store needle pose in world frame as pykdl
    def needle_sub_callback(self, msg):
        self.needle_in_world = pose_to_pykdl(msg.pose)

        self.find_needle_point(self.needle_in_world)


    # Store entry 1 pose in world frame as pykdl
    def entry1_sub_callback(self, msg):
        self.entry1_in_world = pose_to_pykdl(msg.pose)


    # Store exit 1 pose in world frame as pykdl
    def exit1_sub_callback(self, msg):
        self.exit1_in_world = pose_to_pykdl(msg.pose)


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

        self.needle_entry_in_world.p = entry.p + Vector(0.0, 0.0, 0.0)
        self.needle_exit_in_world.p = exit_.p + Vector(0.005, 0.0, 0.004)

        self.needle_entry_in_world.M = entry.M * Rotation.RPY(-1.570796327, 1.570796327, 0)
        self.needle_exit_in_world.M = exit_.M * Rotation.RPY(-1.570796327, -1.570796327, 0)


# ------------------------------------------- Arc Path Planning -------------------------------------------

 
def _normalize(v):
    n = np.linalg.norm(v)
    if n < 1e-12:
        return v
    return v / n
 
 
def _kdl_vec_to_np(v):
    return np.array([v.x(), v.y(), v.z()])
 
 
def _rodrigues_rotate(v, axis, angle):
    """Rotate vector v (perpendicular to axis) about unit axis by angle."""
    return v * np.cos(angle) + np.cross(axis, v) * np.sin(angle)
 

def generate_needle_arc_trajectory(start_frame, end_frame, num_steps=100):
    """
    Generates a true circular arc from start_frame to end_frame by treating
    the motion as a single rigid rotation about a fixed axis (as is physically
    the case for a rigid curved needle pivoting through tissue).
    """
    # Relative rotation that takes start orientation -> end orientation
    rel_rot = end_frame.M * start_frame.M.Inverse()
    angle, axis_kdl = rel_rot.GetRotAngle()  # returns (angle, axis) as a tuple
    axis = _normalize(_kdl_vec_to_np(axis_kdl))

    start_pos = _kdl_vec_to_np(start_frame.p)
    end_pos = _kdl_vec_to_np(end_frame.p)

    # Project the chord into the plane perpendicular to the rotation axis.
    chord = end_pos - start_pos
    chord_in_plane = chord - np.dot(chord, axis) * axis
    chord_len = np.linalg.norm(chord_in_plane)

    mid = start_pos + 0.5 * chord_in_plane
    perp = _normalize(np.cross(axis, chord_in_plane))

    half_angle = angle / 2.0
    if abs(np.sin(half_angle)) > 1e-9:
        dist_to_center = (chord_len / 2.0) / np.tan(half_angle)
    else:
        dist_to_center = 0.0  # degenerate: ~straight line, not a real arc case

    center = mid + dist_to_center * perp
    radius_vec0 = start_pos - center  # start point relative to center

    frames = []
    for t in np.linspace(0.0, 1.0, num_steps):
        a = angle * t
        rot = PyKDL.Rotation.Rot(PyKDL.Vector(*axis), a)
        rotated_radius = _kdl_vec_to_np(rot * PyKDL.Vector(*radius_vec0))
        pos = center + rotated_radius          # now numpy + numpy
        M = rot * start_frame.M
        frames.append(PyKDL.Frame(M, PyKDL.Vector(*pos)))  # convert back to PyKDL.Vector for the Frame

    return frames

# ----------------------------------------------- Main ------------------------------------------------


def main():
    rclpy.init()
    node = NeedleDriving()


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
        node.entry1_in_world,
        node.exit1_in_world
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

  
    node.get_logger().info(f'\nMoving to start pose:\n{target_gripper_in_base}\n\n')
    move_to_pose(node, target_gripper_in_base, 'Needle Driving Start Pose')


    node.get_logger().info('\nNeedle driving sequence')


    for f in driving_path:

        # get the target pose of the gripper in the base frame
        target_gripper_in_base = node.base_in_world.Inverse() * f * needle_point_in_gripper.Inverse()

        predicted_needle_point = (
            node.base_in_world
            * target_gripper_in_base
            * needle_point_in_gripper
        )

        node.get_logger().info(f'\nneedle_point_in_world::\n{node.needle_point_in_world}')
        node.get_logger().info(f'\nf - step in driving path:\n{f}')

        
        #node.get_logger().info(f'\nMoving to next pose:\n{target_gripper_in_base}')
        #move_to_pose(node, target_gripper_in_base, 'Needle Driving')

        target = pykdl_to_posestamped(target_gripper_in_base, "psm2/baselink")

        node.gripper_pub.publish(target)
        for _ in range(100):
            rclpy.spin_once(node, timeout_sec=0.01)


    node.get_logger().info('\nNeedle driving complete...\n\nExiting...')    

    # -------------------- Shutdown --------------------
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


