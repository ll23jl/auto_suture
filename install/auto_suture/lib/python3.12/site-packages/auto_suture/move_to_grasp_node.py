import sys
import rclpy
from rclpy.node import Node
import time
import matplotlib.pyplot as plt

from datetime import datetime
from PyKDL import Vector, Rotation, Frame
from auto_suture_interfaces.srv import FindGraspPose
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from utility.transform_functions import pose_to_pykdl, pykdl_to_pose, posestamped_to_pykdl, pykdl_to_posestamped
from utility.utilities import cartesian_interpolate_step
from ambf_msgs.msg import RigidBodyState



# ---------------------------------------- Define Nodes ----------------------------------------

# -------------------- Move to Grasp Node --------------------

class MoveToGrasp(Node):
    
    # ---------- Init ----------
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

        # subscriber to baselink pose in world
        self.base_pose_meas = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm2/baselink/State',
            self.base_pos_callback,
            10
        )

        # publisher to move the arm
        self.arm_pub = self.create_publisher(
            PoseStamped,
            '/CRTK/psm2/servo_cp',
            10
        )
        
        # publisher to set jaw angle
        self.jaw_pub = self.create_publisher(
            JointState,
            '/CRTK/psm2/jaw/servo_jp',
            10
        )

        # current desired jaw angle
        self.jaw_angle = 0.5   # start open

        # continuously refresh jaw command
        self.jaw_timer = self.create_timer(
            0.1,   # 10 Hz
            self.publish_jaw
        )

        

        

    # ---------- Request for grasp position with given parameters (psm and grasp type) ----------
    def send_request(self, psm, grasp_type):

        req = FindGraspPose.Request()
        req.psm = psm
        req.grasp_type = grasp_type

        return self.cli.call_async(req)
    
    # ---------- Stores arm pose in baselink frame ----------
    def arm_pos_callback(self, msg):
        self.arm_pose = msg.pose


    def publish_jaw(self):

        msg = JointState()

        msg.header.stamp = self.get_clock().now().to_msg()

        msg.name = ["jaw"]

        msg.position = [self.jaw_angle]

        self.jaw_pub.publish(msg)


    def set_jaw(self, angle):

        self.jaw_angle = angle

    # ---------- Stores base pose in world frame ----------
    def base_pos_callback(self, msg):
        self.base_pose = msg.pose




# ---------------------------------------- Main ----------------------------------------

def main():

    rclpy.init()

    move_to_grasp_node = MoveToGrasp()

    if len(sys.argv) < 3:
        move_to_grasp_node.get_logger().error(
            "Usage: ros2 run auto_suture move_to_grasp <psm> <grasp_type>"
        )
        return

    future = move_to_grasp_node.send_request(
        sys.argv[1],
        sys.argv[2]
    )

    rclpy.spin_until_future_complete(move_to_grasp_node, future)

    # store response
    response = future.result()


    # ----- Move the robot -----

    if response.success:


        # ---------- Approach pose ----------


        # measure current pose (in baselink frame)
        while move_to_grasp_node.arm_pose is None:
            move_to_grasp_node.get_logger().info("Waiting for current arm pose...")
            rclpy.spin_once(move_to_grasp_node, timeout_sec=0.1)

        # set flag to false
        done = False

        # set target pose as pykdl (in baselink frame)
        target_pose = posestamped_to_pykdl(response.approach_pose)
        move_to_grasp_node.get_logger().info(f"Moving to pose:\n{target_pose}")

        # current pose to pykdl
        current_pose = pose_to_pykdl(move_to_grasp_node.arm_pose)


        # while loop for movement
        while not done:

            # current pose to pykdl
            current_pose = pose_to_pykdl(move_to_grasp_node.arm_pose)

            # calculate step
            T_delta, done, trans_error_mag, rot_error_mag = cartesian_interpolate_step(
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
            #move_to_grasp_node.get_logger().info(f"Next pose:\n{next_pose}")
            move_to_grasp_node.arm_pub.publish(next_pose)

            # spin
            rclpy.spin_once(move_to_grasp_node, timeout_sec=0.001)
            

        # ---------- Open jaws ----------

        move_to_grasp_node.set_jaw(0.5)

        move_to_grasp_node.get_logger().info("Opening jaws")

        # spin
        rclpy.spin_once(move_to_grasp_node, timeout_sec=0.01)


        # ---------- Grasp pose ----------


        # set flag to false
        done = False

        # set target pose as pykdl (in baselink frame)
        target_pose = posestamped_to_pykdl(response.grasp_pose)
        move_to_grasp_node.get_logger().info(f"Moving to pose:\n{target_pose}")

        # current pose to pykdl
        current_pose = pose_to_pykdl(move_to_grasp_node.arm_pose)


        # while loop for movement
        while not done:

            # current pose to pykdl
            current_pose = pose_to_pykdl(move_to_grasp_node.arm_pose)

            # calculate step
            T_delta, done, trans_error_mag, rot_error_mag = cartesian_interpolate_step(
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
            #move_to_grasp_node.get_logger().info(f"Next pose:\n{next_pose}")
            move_to_grasp_node.arm_pub.publish(next_pose)

            # spin
            rclpy.spin_once(move_to_grasp_node, timeout_sec=0.01)
            


        # wait
        for _ in range(50):
            rclpy.spin_once(move_to_grasp_node, timeout_sec=0.01)

        # ---------- Close jaws ----------

        move_to_grasp_node.set_jaw(0.01)

        move_to_grasp_node.get_logger().info("Closing jaws")

        
        # wait
        for _ in range(50):
            rclpy.spin_once(move_to_grasp_node, timeout_sec=0.01)


        # ---------- Pick up ----------
        
        # ----- For plotting -----
            

        times = []
        trans_errors = []
        rot_errors = []
        start_time = time.time()

        previous_error = float("inf")
        moving_away_count = 0

        # ------------------------

        # set flag to false
        done = False

        current_pose = pose_to_pykdl(move_to_grasp_node.arm_pose)

        base_pose_in_world = pose_to_pykdl(move_to_grasp_node.base_pose)

        current_pose_world = base_pose_in_world * current_pose

        translation_offset = Vector(0.0, 0.0, 0.01)
        rotation_offset = Rotation.RotZ(0.0)

        offset = Frame(rotation_offset, translation_offset)

        target_pose_world = current_pose_world * offset

        target_pose = base_pose_in_world.Inverse() * target_pose_world


        # print target pose
        move_to_grasp_node.get_logger().info(f"Moving to pose:\n{target_pose}")


        # while loop for movement
        while not done:


            # current pose to pykdl
            current_pose = pose_to_pykdl(move_to_grasp_node.arm_pose)

            # calculate step
            T_delta, done, trans_error_mag, rot_error_mag = cartesian_interpolate_step(
                current_pose,
                target_pose
            )

            # ----- For plotting -----
            
            times.append(time.time() - start_time)
            trans_errors.append(trans_error_mag)
            rot_errors.append(rot_error_mag)

            # ----- Debug -----

            # Has the translation error increased?
            if trans_error_mag >= previous_error:
                moving_away_count += 1
            else:
                moving_away_count = 0

            previous_error = trans_error_mag

            #print("moving away count: \n")
            #print(moving_away_count)

            # Give it 10 s to settle before judging it
            if time.time() - start_time > 10:

                # Error has increased for 50 consecutive iterations
                if moving_away_count > 50:
                    move_to_grasp_node.get_logger().error(
                        "Controller diverging - aborting pickup."
                    )
                    break

            # ------------------------------------------------


            # create blank frame
            next_step = Frame()

            # new position and rotation
            next_step.p = current_pose.p + T_delta.p
            next_step.M = current_pose.M * T_delta.M

            # convert to PoseStamped
            next_pose = pykdl_to_posestamped(next_step, "psm2/baselink")

            # debug
            # print("Measured:", current_pose.p)
            # print("Target:  ", target_pose.p)
            # move_to_grasp_node.get_logger().info(f"Next pose:\n{next_pose}")
                        
            # send pose to robot
            move_to_grasp_node.arm_pub.publish(next_pose)

            # spin
            for _ in range(10):
                rclpy.spin_once(move_to_grasp_node, timeout_sec=0.01)

            

        fig, ax1 = plt.subplots(figsize=(8,5))
        ax2 = ax1.twinx()

        line1 = ax1.plot(times, trans_errors, label="Translation Error", color="b")
        line2 = ax2.plot(times, rot_errors, label="Rotation Error", color="r")

        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Translation Error (m)")
        ax2.set_ylabel("Rotation Error (rad)")
        ax1.grid(True)

        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels)
        

        plt.title("Pick Up Needle Error")

        fig.tight_layout()

        filename = f"pick_up_needle_{datetime.now():%Y%m%d_%H%M%S}.png"

        plt.savefig(
            f"/home/jazmin/auto_suture/src/auto_suture/data/{filename}",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close(fig)      




    else:
        move_to_grasp_node.get_logger().error(
            f"Failed to find grasp pose: {response.message}"
        )
        

    move_to_grasp_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()