import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from auto_suture_interfaces.srv import FindGraspPosition

from PyKDL import Frame, Rotation, Vector


class ToolGraspPosition(Node):

    def __init__(self):
        super().__init__('tool_grasp_position')

        self.latest_needle_pose = None

        # Parameters selecting which grasp offset to use
        self.declare_parameter('psm', 'psm1')
        self.declare_parameter('grasp_type', 'grip')

        self.psm = self.get_parameter('psm').value
        self.grasp_type = self.get_parameter('grasp_type').value

        self.get_logger().info(
            f"Using offset: {self.psm} {self.grasp_type}"
        )


        # Subscribe to needle position
        self.subscription = self.create_subscription(
            PoseStamped,
            '/needle_position',
            self.state_callback,
            10
        )


        # Service to calculate grasp pose
        self.srv = self.create_service(
            FindGraspPosition,
            'find_grasp_position',
            self.find_grasp_position_callback
        )


    # ---------------------------------------------------------
    # Store latest needle pose
    # ---------------------------------------------------------
    def state_callback(self, msg):

        self.latest_needle_pose = msg

        self.get_logger().debug(
            f"Updated needle pose: "
            f"{msg.pose.position.x}, "
            f"{msg.pose.position.y}, "
            f"{msg.pose.position.z}"
        )


    # ---------------------------------------------------------
    # Load grasp offset from YAML parameters
    # ---------------------------------------------------------
    def get_grasp_offset(self):

        prefix = (
            f'grasp_offsets.'
            f'{self.psm}.'
            f'{self.grasp_type}'
        )


        x = self.get_parameter(
            prefix + '.position.x'
        ).value

        y = self.get_parameter(
            prefix + '.position.y'
        ).value

        z = self.get_parameter(
            prefix + '.position.z'
        ).value


        roll = self.get_parameter(
            prefix + '.orientation.roll'
        ).value

        pitch = self.get_parameter(
            prefix + '.orientation.pitch'
        ).value

        yaw = self.get_parameter(
            prefix + '.orientation.yaw'
        ).value


        return Frame(
            Rotation.RPY(
                roll,
                pitch,
                yaw
            ),
            Vector(
                x,
                y,
                z
            )
        )


    # ---------------------------------------------------------
    # Calculate grasp position service callback
    # ---------------------------------------------------------
    def find_grasp_position_callback(self, request, response):

        if self.latest_needle_pose is None:

            self.get_logger().warn(
                "No needle pose received yet"
            )

            return response


        # Get selected grasp offset
        offset = self.get_grasp_offset()


        # Convert needle PoseStamped to PyKDL Frame
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


        # Apply offset:
        # T_tool = T_needle * T_offset
        tool_frame = needle_frame * offset


        # Convert PyKDL Frame back to PoseStamped
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