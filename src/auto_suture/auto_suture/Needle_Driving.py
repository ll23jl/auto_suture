
# Needle driving script
# Tracks needle point
# Path plans
# Drives the needle
# ----------------------------------------------------------------------

# ------------------------------ Imports ------------------------------

import rclpy

from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from PyKDL import Frame, Rotation, Vector
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, pykdl_to_posestamped


# ------------------------------ Define node ------------------------------
class NeedleDriving(Node):

    def __init__(self):
        super().__init__('needle_driving')

        # -------------------- Variables --------------------

        self.needle_to_point_offset = Frame(
            Rotation.RPY(0., 0., -0.688), 
            Vector(0.00661780871450901, 0.0069734565913677216, 0.0)
        )# note that y axis follows tangent of needle point


        self.needle_in_world = None
        
        self.needle_point_in_world = None

        # -------------------- Subscribers --------------------

        # Needle pose in world frame
        self.needle_sub = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_world_frame',
            self.needle_sub_callback,
            10
        )

        # -------------------- Publishers --------------------
        
        # Needle point pose in world frame
        self.needle_point_pub = self.create_publisher(
            PoseStamped,
            '/needle_point_in_world',
            10
        )

    # -------------------- Callback Functions --------------------

    # Store needle pose in world frame as pykdl
    def needle_sub_callback(self, msg):
        self.needle_in_world = pose_to_pykdl(msg.pose)

        self.find_needle_point(self.needle_in_world)

    
    # -------------------- Other Functions --------------------

    # Finds the needle point pose in world frame
    def find_needle_point(self, needle_in_world):

        self.needle_point_in_world = needle_in_world * self.needle_to_point_offset

        msg = pykdl_to_posestamped(needle_point_in_world, "world")
        msg.header.stamp = self.get_clock().now().to_msg()

        self.needle_point_pub.publish(msg)


# --------------------------------------------------------------------------------
# -------------------------------- Path Planning ---------------------------------

def plot_driving_path(self, entry_pose_in_world, exit_pose_in_world)






# -------------------------------------------------------------------------------
# ------------------------------------ Main -------------------------------------


