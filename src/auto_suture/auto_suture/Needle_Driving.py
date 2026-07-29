

# ---------------------------------------- Imports ----------------------------------------


import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from ambf_msgs.msg import RigidBodyState
import PyKDL
from PyKDL import Frame, Rotation, Vector
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, pykdl_to_posestamped


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

        self.needle_entry_in_world.p = entry.p
        self.needle_exit_in_world.p = exit_.p

        self.needle_entry_in_world.M = entry.M * Rotation.RPY(1.570796327, 0, 0)
        self.needle_exit_in_world.M = exit_.M * Rotation.RPY(1.570796327, 0, 0)


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
 
 
def generate_needle_arc_trajectory(start_frame, end_frame, num_steps=20, handle_frac=1.0 / 3.0):

    # extract position of start and finish poses
    start_pos = _kdl_vec_to_np(start_frame.p)
    end_pos = _kdl_vec_to_np(end_frame.p)
 
    x0 = _kdl_vec_to_np(start_frame.M.UnitX())
    y0 = _kdl_vec_to_np(start_frame.M.UnitY())
    z0 = _kdl_vec_to_np(start_frame.M.UnitZ())
 
    x1 = _kdl_vec_to_np(end_frame.M.UnitX())
    y1 = _kdl_vec_to_np(end_frame.M.UnitY())
    z1 = _kdl_vec_to_np(end_frame.M.UnitZ())
 
    # Cubic Bezier position curve, tangent-constrained at both ends
    chord_len = np.linalg.norm(end_pos - start_pos)
    h = chord_len * handle_frac
    P0 = start_pos
    P1 = start_pos + h * y0
    P2 = end_pos - h * y1
    P3 = end_pos
 
    def bezier_pos(t):
        return ((1 - t) ** 3) * P0 + 3 * ((1 - t) ** 2) * t * P1 + 3 * (1 - t) * (t ** 2) * P2 + (t ** 3) * P3
 
    def bezier_tangent(t):
        return 3 * ((1 - t) ** 2) * (P1 - P0) + 6 * (1 - t) * t * (P2 - P1) + 3 * (t ** 2) * (P3 - P2)
 
    ts = np.linspace(0.0, 1.0, num_steps)
    positions = np.array([bezier_pos(t) for t in ts])
    tangents = np.array([_normalize(bezier_tangent(t)) for t in ts])
 
    # --- Rotation-minimizing frame propagation (double reflection method) ---
    xs = np.zeros((num_steps, 3))
    xs[0] = x0
 
    for i in range(1, num_steps):
        v1 = positions[i] - positions[i - 1]
        c1 = np.dot(v1, v1)
        if c1 < 1e-12:
            xs[i] = xs[i - 1]
            continue
 
        rL = xs[i - 1] - (2.0 / c1) * np.dot(v1, xs[i - 1]) * v1
        tL = tangents[i - 1] - (2.0 / c1) * np.dot(v1, tangents[i - 1]) * v1
 
        v2 = tangents[i] - tL
        c2 = np.dot(v2, v2)
        if c2 < 1e-12:
            xs[i] = _normalize(rL)
        else:
            xs[i] = _normalize(rL - (2.0 / c2) * np.dot(v2, rL) * v2)
 
    # --- Twist correction so the trajectory ends exactly on end_frame ---
    x_last = xs[-1]
    cos_th = np.clip(np.dot(x_last, x1), -1.0, 1.0)
    sin_th = np.dot(np.cross(x_last, x1), y1)
    theta_twist = np.arctan2(sin_th, cos_th)
 
    frames = []
    for i, t in enumerate(ts):
        angle = theta_twist * t
        x_axis = _rodrigues_rotate(xs[i], tangents[i], angle)
        y_axis = tangents[i]
        z_axis = np.cross(x_axis, y_axis)
 
        rot = PyKDL.Rotation(
            PyKDL.Vector(*x_axis),
            PyKDL.Vector(*y_axis),
            PyKDL.Vector(*z_axis),
        )
        frames.append(PyKDL.Frame(rot, PyKDL.Vector(*positions[i])))
 
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
    driving_path = generate_needle_arc_trajectory(node.needle_entry_in_world, node.needle_exit_in_world, num_steps=30)
    
    # move to entry pose
    done = False

    target_gripper_in_base = node.base_in_world.Inverse() * node.needle_entry_in_world * needle_point_in_gripper.Inverse()

    target_pose_in_base = pykdl_to_posestamped(target_gripper_in_base, "psm2/baselink")

    node.get_logger().info('\nMoving to start pose')

    while not done:


        node.gripper_pub.publish(target_pose_in_base)

        rclpy.spin_once(node, timeout_sec=0.01)

        position_error = (node.needle_entry_in_world.p - node.needle_point_in_world.p).Norm()

        rotation_error = (
            node.needle_entry_in_world.M.Inverse() * node.needle_point_in_world.M
        ).GetRotAngle()[0]

        if position_error < 0.002 and rotation_error < 0.05:
            done = True


    node.get_logger().info('\nNeedle driving sequence')

    for f in driving_path:

        # get the target pose of the gripper in the base frame
        target_gripper_in_base = node.base_in_world.Inverse() * f * needle_point_in_gripper.Inverse()

        target_pose_in_base = pykdl_to_posestamped(target_gripper_in_base, "psm2/baselink")

        done = False

    
        while not done:

            node.gripper_pub.publish(target_pose_in_base)

            rclpy.spin_once(node, timeout_sec=0.01)

            position_error = (f.p - node.needle_point_in_world.p).Norm()

            rotation_error = (
                f.M.Inverse() * node.needle_point_in_world.M
            ).GetRotAngle()[0]

            if position_error < 0.002 and rotation_error < 0.05:
                done = True

    node.get_logger().info('\nNeedle driving complete...\n\nExiting...')    

    # -------------------- Shutdown --------------------
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


