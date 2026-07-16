
# Node that takes needle pose in the world frame 
# and calculates the correct pose for the tool to grasp the needle
# Has multiple configurations depending on which psm is being used (psm1 or psm2) 
# and which side of the needle is being grasped (grip or tip)
# -----------------------------------------------------------------------

# Imports

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from auto_suture_interfaces.srv import FindGraspPose
from PyKDL import Frame, Rotation, Vector

# Define node
class ToolGraspPose(Node):

    def __init__(self):
        super().__init__('tool_grasp_pose',automatically_declare_parameters_from_overrides=True)

        # Initialize variable to store latest needle pose
        self.latest_needle_pose = None


        # Subscriber to needle pose
        self.subscription = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_world_frame',
            self.state_callback,
            10
        )

        # Service Server to calculate grasp pose
        self.srv = self.create_service(
            FindGraspPose,
            'find_grasp_pose',
            self.find_grasp_pose_callback
        )


    # Callback function for storing the latest needle pose
    def state_callback(self, msg):

        self.latest_needle_pose = msg

        self.get_logger().debug(
            f"Updated needle pose: "
            f"{msg.pose.position.x}, "
            f"{msg.pose.position.y}, "
            f"{msg.pose.position.z}"
        )


    # function for choosing the correct grasp offset for scenario
    def get_grasp_offset(self, psm, grasp_type):

        prefix = f'grasp_offsets.{psm}.{grasp_type}'


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


    # Service callback function to calculate grasp pose
    def find_grasp_pose_callback(self, request, response):

        # Check there is actually a pose stored
        if self.latest_needle_pose is None:

            self.get_logger().warn(
                "No needle pose received yet"
            )

            response.success = False
            response.message = "No needle pose received yet"

            return response


        # Get selected grasp offset
        offset = self.get_grasp_offset(
            request.psm,
            request.grasp_type
        )


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
        #tool_frame = needle_frame * offset
        tool_frame = needle_frame


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
        response.success = True
        response.message = "Grasp pose calculated successfully"

        return response



def main(args=None):

    rclpy.init(args=args)

    node = ToolGraspPose()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()



if __name__ == '__main__':
    main()