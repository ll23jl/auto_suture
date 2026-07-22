
# Node that takes needle pose in the world frame 
# and calculates the correct pose for the tool to grasp the needle
# Has multiple configurations depending on which psm is being used (psm1 or psm2) 
# and which side of the needle is being grasped (grip or tip)
# -----------------------------------------------------------------------

# Imports

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from ambf_msgs.msg import RigidBodyState
from auto_suture_interfaces.srv import FindGraspPose
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose
from PyKDL import Frame, Rotation, Vector


# ----- Define node -----
class ToolGraspPose(Node):

    def __init__(self):
        super().__init__('tool_grasp_pose',automatically_declare_parameters_from_overrides=True)

        # Initialize variable to store latest poses
        self.latest_needle_pose = None
        self.latest_base_pose = None


        # Subscriber to needle pose
        self.subscription = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_world_frame',
            self.needle_state_callback,
            10
        )

        # Subscriber to baselink frame state
        self.subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm2/baselink/State',
            self.baselink_state_callback,
            10
        )

        # Service Server to calculate grasp pose
        self.srv = self.create_service(
            FindGraspPose,
            'find_grasp_pose',
            self.find_grasp_pose_callback
        )


    # ----- Callback function for storing the latest needle pose -----
    def needle_state_callback(self, msg):

        self.latest_needle_pose = msg

        self.get_logger().debug(
            f"Updated needle pose: "
            f"{msg.pose.position.x}, "
            f"{msg.pose.position.y}, "
            f"{msg.pose.position.z} "
        )


    # ----- Callback function for storing the latest baselink pose (should not change) -----
    def baselink_state_callback(self, msg):

        self.latest_base_pose = msg.pose

        self.get_logger().debug(
            f"Updated baselink pose: "
            f"{msg.pose.position.x}, "
            f"{msg.pose.position.y}, "
            f"{msg.pose.position.z} "
        )


    # ----- Function for choosing the correct grasp offset for scenario -----
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


    # ----- Service callback function to calculate grasp pose -----
    def find_grasp_pose_callback(self, request, response):


        # ----- Check there is actually a pose stored -----


        if self.latest_needle_pose is None:

            self.get_logger().warn(
                "No needle pose received yet"
            )

            response.success = False
            response.message = "No needle pose received yet"

            return response


        # ----- Check there is actually a pose stored -----


        if self.latest_base_pose is None:

            self.get_logger().warn(
                "No base pose received yet"
            )

            response.success = False
            response.message = "No base pose received yet"

            return response


        # ----- Get selected grasp offset -----


        offset = self.get_grasp_offset(
            request.psm,
            request.grasp_type
        )

        # Convert needle Pose(Stamped) to PyKDL Frame
        needle_frame = pose_to_pykdl(self.latest_needle_pose.pose)
        base_frame = pose_to_pykdl(self.latest_base_pose)

        # Convert to baselink frame:
        needle_in_base = base_frame.Inverse() * needle_frame

        # Apply offset:
        tool_frame = needle_in_base * offset
        

        # ----- Set frame of approach: -----
        # 10mm 'above' needle 

        approach_offset = Frame(
            Rotation.Identity(),
            Vector(0,0,0.005)
        )

        approach_in_world = needle_frame * approach_offset * offset

        approach_frame = base_frame.Inverse() * approach_in_world


        # ------ Convert PyKDL Frame back to PoseStamped ------


        # ----- Grasp pose: -----


        grasp_pose = PoseStamped()

        grasp_pose.header.frame_id = "psm2/baselink"

        grasp_pose.pose = pykdl_to_pose(tool_frame)

        response.grasp_pose = grasp_pose


        # ----- Approach pose: -----


        approach_pose = PoseStamped()

        approach_pose.header.frame_id = "psm2/baselink"

        approach_pose.pose = pykdl_to_pose(approach_frame)

        response.approach_pose = approach_pose

        response.success = True

        response.message = "Grasp pose calculated successfully"

        # --------------------------

        return response



def main(args=None):

    rclpy.init(args=args)

    node = ToolGraspPose()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()



if __name__ == '__main__':
    main()