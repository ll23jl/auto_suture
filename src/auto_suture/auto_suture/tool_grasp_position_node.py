import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from auto_suture_interfaces.srv import FindGraspPosition

import numpy as np

from PyKDL import Frame, Rotation, Vector


class ToolGraspPosition(Node):

    def __init__(self):
        super().__init__('tool_grasp_position')

        self.latest_needle_pose = None

        # Subscribe to needle position
        self.subscription = self.create_subscription(
            PoseStamped,
            '/needle_position',
            self.state_callback,
            10
        )

        # Service
        self.srv = self.create_service(
            FindGraspPosition,
            'find_grasp_position',
            self.find_grasp_position_callback
        )


    def state_callback(self, msg):
        """
        Store latest needle pose
        """
        self.latest_needle_pose = msg


    def find_grasp_position_callback(self, request, response):
        """
        Calculate grasp pose when requested
        """

        if self.latest_needle_pose is None:
            self.get_logger().warn(
                "No needle position received yet"
            )
            return response


        offset_psm1_grip = Frame(
            Rotation.RPY(-np.pi / 2., 0, 0.),
            Vector(
                0.008973019361495972,
                -0.005215135216712952,
                0.005237608169473778
            )
        )


        needle_frame = Frame(
            Rotation.Quaternion(
                self.latest_needle_pose.pose.orientation.x,
                self.latest_needle_pose.pose.orientation.y,
                self.latest_needle_pose.pose.orientation.z,
                self.latest_needle_pose.pose.orientation.w
            ),
            Vector(
                self.latest_needle_pose.pose.position.x,
                self.latest_needle_pose.pose.position.y,
                self.latest_needle_pose.pose.position.z
            )
        )


        tool_frame = needle_frame * offset_psm1_grip


        grasp_pose = PoseStamped()

        grasp_pose.header = self.latest_needle_pose.header

        grasp_pose.pose.position.x = tool_frame.p.x()
        grasp_pose.pose.position.y = tool_frame.p.y()
        grasp_pose.pose.position.z = tool_frame.p.z()


        qx, qy, qz, qw = tool_frame.M.GetQuaternion()

        grasp_pose.pose.orientation.x = qx
        grasp_pose.pose.orientation.y = qy
        grasp_pose.pose.orientation.z = qz
        grasp_pose.pose.orientation.w = qw


        response.grasp_pose = grasp_pose

        return response



def main(args=None):

    rclpy.init(args=args)

    node = ToolGraspPosition()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()