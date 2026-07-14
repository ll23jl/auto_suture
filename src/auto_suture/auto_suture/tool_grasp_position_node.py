import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped

import numpy as np

from PyKDL import Frame, Rotation, Vector


# Grasp position node definition
class ToolGraspPosition(Node):

    def __init__(self):
        super().__init__('tool_grasp_position')

        # subscriber to needle position
        self.subscription = self.create_subscription(
            PoseStamped,
            '/needle_position',
            self.state_callback,
            10
        )
        self.subscription  # prevent unused variable warning

        # store latest needle pose
        self.latest_needle_pose = None

        # service to find grasp position
        self.srv = self.create_service(FindGraspPosition, 'find_grasp_position', self.find_grasp_position_callback)

        # callback function for the service - finds the grasp position based on the needle position and the offset of the tool
        def find_grasp_position_callback(self, request, response):
            response = PoseStamped()
            response.header = msg.header
            response.pose.position = msg.pose.position * offset_psm1_grip.p
            response.pose.orientation = msg.pose.orientation * offset_psm1_grip.M.GetQuaternion

        return response




    def state_callback(self, msg):

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
                msg.pose.orientation.x,
                msg.pose.orientation.y,
                msg.pose.orientation.z,
                msg.pose.orientation.w
            ),
            Vector(
                msg.pose.position.x,
                msg.pose.position.y,
                msg.pose.position.z
            )
        )

        tool_frame = needle_frame * offset_psm1_grip

        pose = PoseStamped()
        pose.header = msg.header

        pose.pose.position.x = tool_frame.p.x()
        pose.pose.position.y = tool_frame.p.y()
        pose.pose.position.z = tool_frame.p.z()

        qx, qy, qz, qw = tool_frame.M.GetQuaternion()

        pose.pose.orientation.x = qx
        pose.pose.orientation.y = qy
        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw


    

def main(args=None):
    rclpy.init()

    tool_grasp_position = ToolGraspPosition()

    rclpy.spin(tool_grasp_position)

    rclpy.shutdown()


if __name__ == '__main__':
    main()