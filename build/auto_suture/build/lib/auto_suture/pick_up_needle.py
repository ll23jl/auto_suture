
# -------------------- Imports --------------------

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from ambf_msgs.msg import RigidBodyState
from auto_suture_interfaces.srv import FindGraspPose
import sys
import time
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, posestamped_to_pykdl, pykdl_to_posestamped
from utility.utilities import cartesian_interpolate_step
from PyKDL import Frame, Rotation, Vector
from sensor_msgs.msg import JointState
import threading





# ---------------------------------------- Needle Position Node ----------------------------------------

# Node that converts needle pose in the camera frame into the world frame
# Subscribes to needle pose (in camera frame) and camera pose data given by ECM
# Transforms needle pose into the world frame
# Publishes needle pose in the world frame as PoseStamped

# -------------------- Define node --------------------
class NeedlePosition(Node):

    def __init__(self):
        super().__init__('needle_position')
        
        # Initialize variables to store needle and camera poses in camera/world frame
        self.needle_pose = None
        self.camera_pose = None


        # Subcriber to needle pose in camera frame
        self.needle_camera_subscription = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_camera_frame',
            self.needle_callback,
            10
        )

        # Subcriber to camera pose in world frame
        self.camera_world_subscription = self.create_subscription(
            RigidBodyState,
            '/ambf/env/phantom/CameraFrame/State',
            self.camera_callback,
            10
        )

        # Subscriber to

        # Publisher for needle pose in world frame
        self.needle_world_publisher_ = self.create_publisher(
            PoseStamped,
            '/needle_pose_in_world_frame',
            10
        )


    # ----- Callback function that stores needle pose in camera frame -----
    def needle_callback(self, msg):
        self.needle_pose = msg.pose
        self.calculate_transform()


    # ----- Callback function that stores camera pose in world frame -----
    def camera_callback(self, msg):
        self.camera_pose = msg.pose
        self.calculate_transform()


    # ----- Function that transforms the needle pose into the world frame -----
    def calculate_transform(self):

        if self.needle_pose is None or self.camera_pose is None:
            return


        # ----- Convert needle and camera poses in PyKDL format -----

        T_needle_camera = pose_to_pykdl(self.needle_pose)


        T_camera_world = pose_to_pykdl(self.camera_pose)
        

        # ----- Calculate the needle position in the world frame -----

        T_needle_world = (
            T_camera_world
            *
            T_needle_camera
        )

        # ----- Create a new outgoing message -----

        pose = PoseStamped()

        pose.header.frame_id = "world"

        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose = pykdl_to_pose(T_needle_world)

        self.needle_world_publisher_.publish(pose)





# ---------------------------------------- Tool Grasp Pose Node ----------------------------------------

# Node that takes needle pose in the world frame 
# and calculates the correct pose for the tool to grasp the needle
# Has multiple configurations depending on which psm is being used (psm1 or psm2) 
# and which side of the needle is being grasped (grip or tip)

# -------------------- Define node --------------------
class ToolGraspPose(Node):

    def __init__(self):
        super().__init__('tool_grasp_pose',automatically_declare_parameters_from_overrides=True)

        # Initialize variable to store latest poses
        self.latest_needle_pose = None
        self.latest_base_pose = None


        # Subscriber to needle pose
        self.needle_world_subscription = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_world_frame',
            self.needle_state_callback,
            10
        )

        # Subscriber to baselink frame state
        self.base_world_subscription = self.create_subscription(
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


    # ---------- Callback function for storing the latest needle pose ----------
    def needle_state_callback(self, msg):

        self.latest_needle_pose = msg

        self.get_logger().debug(
            f"Updated needle pose: "
            f"{msg.pose.position.x}, "
            f"{msg.pose.position.y}, "
            f"{msg.pose.position.z} "
        )


    # ---------- Callback function for storing the latest baselink pose (should not change) ----------
    def baselink_state_callback(self, msg):

        self.latest_base_pose = msg.pose

        self.get_logger().debug(
            f"Updated baselink pose: "
            f"{msg.pose.position.x}, "
            f"{msg.pose.position.y}, "
            f"{msg.pose.position.z} "
        )


    # ---------- Function for choosing the correct grasp offset for scenario ----------
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


    # ---------- Service callback function to calculate grasp pose ----------
    def find_grasp_pose_callback(self, request, response):


        # ---------- Check there is actually a pose stored ----------


        if self.latest_needle_pose is None:

            self.get_logger().warn(
                "No needle pose received yet"
            )

            response.success = False
            response.message = "No needle pose received yet"

            return response


        # ---------- Check there is actually a pose stored ----------


        if self.latest_base_pose is None:

            self.get_logger().warn(
                "No base pose received yet"
            )

            response.success = False
            response.message = "No base pose received yet"

            return response


        # ---------- Get selected grasp offset ----------


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
        

        # ---------- Set frame of approach: ----------

        # 10mm 'above' needle 
        approach_offset = Frame(
            Rotation.Identity(),
            Vector(0,0,0.01)
        )

        approach_frame = needle_in_base * approach_offset * offset


        # -------------------- Convert PyKDL Frame back to PoseStamped --------------------


        # ---------- Grasp pose: ----------


        grasp_pose = PoseStamped()

        grasp_pose.header.frame_id = "psm2/baselink"

        grasp_pose.pose = pykdl_to_pose(tool_frame)

        response.grasp_pose = grasp_pose


        # ---------- Approach pose: ----------


        approach_pose = PoseStamped()

        approach_pose.header.frame_id = "psm2/baselink"

        approach_pose.pose = pykdl_to_pose(approach_frame)

        response.approach_pose = approach_pose

        response.success = True

        response.message = "Grasp pose calculated successfully"



        return response





# ---------------------------------------- Grasp Needle Node ----------------------------------------

# Node that requests tool grasp pose from above node
# and moves the psm to that pose

# -------------------- Define Node --------------------
class PickUpNeedle(Node):

    def __init__(self):
        super().__init__('move_to_grasp')

        self.arm_pose = None

        # Service Client to find grasp pose
        self.cli = self.create_client(
            FindGraspPose,
            'find_grasp_pose'
        )

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'service not available, waiting again...'
            )

        self.req = FindGraspPose.Request()


        # subscriber to psm2 current pose
        self.arm_meas = self.create_subscription(
            PoseStamped,
            '/CRTK/psm2/measured_cp',
            self.arm_pos_callback,
            10
        )

        # publisher to move the arm
        self.arm_pub = self.create_publisher(
            PoseStamped,
            '/CRTK/psm2/servo_cp',
            10
        )

        # publisher to move jaw
        self.jaw_pub = self.create_publisher(
            JointState,
            '/CRTK/psm2/jaw/servo_jp',
            10
        )

    # ---------- Function that sends request for grasp position with given parameters (psm and grasp type) ----------
    def send_request(self, psm, grasp_type):

        req = FindGraspPose.Request()
        req.psm = psm
        req.grasp_type = grasp_type

        return self.cli.call_async(req)
    
    # ---------- Callback function that stores arm pose in baselink frame ----------
    def arm_pos_callback(self, msg):
        self.arm_pose = msg.pose





# ---------------------------------------- Main ----------------------------------------

def main():

    # -------------------- Init --------------------

    rclpy.init()

    tool_grasp_pose_node = ToolGraspPose()
    needle_position_node = NeedlePosition()
    pick_up_needle_node = PickUpNeedle()

    executor = rclpy.executors.MultiThreadedExecutor()

    executor.add_node(tool_grasp_pose_node)
    executor.add_node(needle_position_node)
    executor.add_node(pick_up_needle_node)

    executor_thread = threading.Thread(
        target=executor.spin,
        daemon=True
    )

    executor_thread.start()


    if len(sys.argv) < 3:
        pick_up_needle_node.get_logger().error(
            "Usage: ros2 run auto_suture move_to_grasp <psm> <grasp_type>"
        )
        return

    future = pick_up_needle_node.send_request(
        sys.argv[1],
        sys.argv[2]
    )

    while not future.done():
        time.sleep(0.01)
        
    # store response
    response = future.result()


    # -------------------- Move the robot --------------------

    if response.success:


        # ---------- Approach pose ----------


        # measure current pose (in baselink frame)
        while pick_up_needle_node.arm_pose is None:
            pick_up_needle_node.get_logger().info("Waiting for current arm pose...")
            rclpy.spin_once(pick_up_needle_node, timeout_sec=0.1)

        # set flag to false
        done = False

        # set target pose as pykdl (in baselink frame)
        target_pose = posestamped_to_pykdl(response.approach_pose)
        pick_up_needle_node.get_logger().info(f"Moving to pose:\n{target_pose}")

        # current pose to pykdl
        current_pose = pose_to_pykdl(pick_up_needle_node.arm_pose)


        # while loop for movement
        while not done:

            # current pose to pykdl
            current_pose = pose_to_pykdl(pick_up_needle_node.arm_pose)

            # calculate step
            T_delta, done = cartesian_interpolate_step(
                current_pose,
                target_pose
            )

            # create blank frame
            next_step = Frame()

            # new position and rotation
            next_step.p = current_pose.p + T_delta.p
            next_step.M = current_pose.M * T_delta.M

            # convert to PoseStamped
            next_pose = pykdl_to_posestamped(next_step, "psm2/baselink")

            # send pose to robot
            #pick_up_needle_node.get_logger().info(f"Next pose:\n{next_pose}")
            pick_up_needle_node.arm_pub.publish(next_pose)

            # spin
            rclpy.spin_once(pick_up_needle_node, timeout_sec=0.001)
            

        # ---------- Open jaws ----------


        jaw_pos = JointState()
        jaw_pos.header.stamp = pick_up_needle_node.get_clock().now().to_msg()
        jaw_pos.name = ["jaw"]
        jaw_pos.position = [0.5]

        pick_up_needle_node.jaw_pub.publish(jaw_pos)
        
        pick_up_needle_node.get_logger().info("Opening jaws")

        # spin
        rclpy.spin_once(pick_up_needle_node, timeout_sec=0.01)


        # ---------- Grasp pose ----------


        # set flag to false
        done = False

        # set target pose as pykdl (in baselink frame)
        target_pose = posestamped_to_pykdl(response.grasp_pose)
        pick_up_needle_node.get_logger().info(f"Moving to pose:\n{target_pose}")

        # current pose to pykdl
        current_pose = pose_to_pykdl(pick_up_needle_node.arm_pose)


        # while loop for movement
        while not done:

            # current pose to pykdl
            current_pose = pose_to_pykdl(pick_up_needle_node.arm_pose)

            # calculate step
            T_delta, done = cartesian_interpolate_step(
                current_pose,
                target_pose
            )

            # create blank frame
            next_step = Frame()

            # new position and rotation
            next_step.p = current_pose.p + T_delta.p
            next_step.M = current_pose.M * T_delta.M

            # convert to PoseStamped
            next_pose = pykdl_to_posestamped(next_step, "psm2/baselink")

            # send pose to robot
            #pick_up_needle_node.get_logger().info(f"Next pose:\n{next_pose}")
            pick_up_needle_node.arm_pub.publish(next_pose)

            # spin
            rclpy.spin_once(pick_up_needle_node, timeout_sec=0.01)


        # ---------- Close jaws ----------


        jaw_pos = JointState()
        jaw_pos.header.stamp = pick_up_needle_node.get_clock().now().to_msg()
        jaw_pos.name = ["jaw"]
        jaw_pos.position = [0.0]

        pick_up_needle_node.jaw_pub.publish(jaw_pos)
        
        pick_up_needle_node.get_logger().info("Closing jaws")

        # wait
        for _ in range(10):
            rclpy.spin_once(pick_up_needle_node, timeout_sec=0.1) 


        # ---------- Pick up ----------
        



        # set flag to false
        done = False

        # current pose to pykdl
        current_pose = pose_to_pykdl(pick_up_needle_node.arm_pose)

        # set target pose as pykdl (in baselink frame)
        target_pose.p = current_pose.p + Vector(0.0, 0.0, 0.01)

        # print target pose
        pick_up_needle_node.get_logger().info(f"Moving to pose:\n{target_pose}")


        # while loop for movement
        while not done:

            # keep jaws closed
            jaw_pos = JointState()
            jaw_pos.header.stamp = pick_up_needle_node.get_clock().now().to_msg()
            jaw_pos.name = ["jaw"]
            jaw_pos.position = [0.01]

            #pick_up_needle_node.jaw_pub.publish(jaw_pos)

            # current pose to pykdl
            current_pose = pose_to_pykdl(pick_up_needle_node.arm_pose)

            # calculate step
            T_delta, done = cartesian_interpolate_step(
                current_pose,
                target_pose
            )

            # create blank frame
            next_step = Frame()

            # new position and rotation
            next_step.p = current_pose.p + T_delta.p
            next_step.M = current_pose.M * T_delta.M

            # convert to PoseStamped
            next_pose = pykdl_to_posestamped(next_step, "psm2/baselink")

            # debug
            print("Measured:", current_pose.p)
            print("Target:  ", target_pose.p)
            pick_up_needle_node.get_logger().info(f"Next pose:\n{next_pose}")
                        
            # send pose to robot
            pick_up_needle_node.arm_pub.publish(next_pose)

            # spin
            rclpy.spin_once(pick_up_needle_node, timeout_sec=0.1)

            # wait
            time.sleep(0.05)

            



    else:
        pick_up_needle_node.get_logger().error(
            f"Failed to find grasp pose: {response.message}"
        )


    # -------------------- Shutdown --------------------    

    # destroy nodes
    needle_position_node.destroy_node()
    tool_grasp_pose_node.destroy_node()
    pick_up_needle_node.destroy_node()

    # shutdown
    rclpy.shutdown()


if __name__ == '__main__':
    main()



