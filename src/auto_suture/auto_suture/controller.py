#!/usr/bin/env python3

import time
import subprocess
import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from ambf_msgs.msg import RigidBodyState
from utility.transform_functions import pose_to_pykdl




def run_step(command):
    print(f"\nRunning: {' '.join(command)}")

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"Step failed with return code {result.returncode}")
        print(f"Command was: {' '.join(command)}")
        sys.exit(result.returncode)

def start_step(command):
    print(f"Starting: {' '.join(command)}")
    return subprocess.Popen(command)


# ---------------------------------------- Node ----------------------------------------


class Controller(Node):
    def __init__(self):
        super().__init__('controller')


        # -------------------- Variables --------------------

        self.psm1_gripper_in_base = None
        self.psm2_gripper_in_base = None
        self.psm1_base_in_world = None
        self.psm2_base_in_world = None
        self.needle_in_world = None
        

        # -------------------- Subscriptions --------------------

        self.psm1_meas = self.create_subscription(
            PoseStamped,
            '/CRTK/psm1/measured_cp',
            self.psm1_gripper_callback,
            10
        )

        self.psm2_meas = self.create_subscription(
            PoseStamped,
            '/CRTK/psm2/measured_cp',
            self.psm2_gripper_callback,
            10
        )

        self.psm1_base_meas = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm1/baselink/State',
            self.psm1_base_callback,
            10
        )

        self.psm2_base_meas = self.create_subscription(
            RigidBodyState,
            '/ambf/env/psm2/baselink/State',
            self.psm2_base_callback,
            10
        )

        self.needle_meas = self.create_subscription(
            PoseStamped,
            '/needle_pose_in_world_frame',
            self.needle_callback,
            10
        )
 

    # -------------------- Callback functions --------------------

    def psm1_gripper_callback(self, msg):
        self.psm1_gripper_in_base = pose_to_pykdl(msg.pose)

    def psm2_gripper_callback(self, msg):
        self.psm2_gripper_in_base = pose_to_pykdl(msg.pose)
        
    def psm1_base_callback(self, msg):
        self.psm1_base_in_world = pose_to_pykdl(msg.pose)

    def psm2_base_callback(self, msg):
        self.psm2_base_in_world = pose_to_pykdl(msg.pose)

    def needle_callback(self, msg):
        self.needle_in_world = pose_to_pykdl(msg.pose)


    # -------------------- Other functions --------------------

    # run until initial pose data is received
    def ensure_initial_data(self):
        self.get_logger().info('Waiting for initial pose data...')
        while (
            self.psm1_gripper_in_base is None or
            self.psm2_gripper_in_base is None or
            self.psm1_base_in_world is None or
            self.psm2_base_in_world is None or
            self.needle_in_world is None
        ):
            
            rclpy.spin_once(self, timeout_sec=0.1)   




# ---------------------------------------- Main ----------------------------------------


def main():

    # start controller node
    rclpy.init()
    node = Controller()

    # wait for initial data
    node.ensure_initial_data()
    node.get_logger().info('\nData received\n')


    # ---------------------------------------- PSM2 grasp needle ----------------------------------------
    run_step([
        "ros2", "run", "auto_suture",
        "Grasp_Needle",
        "psm2",
        "grip",
        "up",
        "--ros-args",
        "--params-file",
        "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
    ])

    # check if needle was placed the other way:

    if node.needle_in_world.M[2, 2] < 0:
        # needle is upside down
        # swap needle to psm1 and then back to psm2

        print('Needle in incorrect suturing position')

        run_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm2",
            "0.0, 0.0, 0.01, 1.57, 1.57, 0.0, 0.0"
        ])

        run_step([
            "ros2", "run", "auto_suture",
            "Handover"
        ])

        run_step([
            "ros2", "run", "auto_suture",
            "Handover"
        ])




    for step in range(1, 4):
        print(f"\n\nStarting suture {step}...\n\n")


        # ---------------------------------------- Needle driving through entry ----------------------------------------
        run_step([
            "ros2", "run", "auto_suture",
            "Needle_Driving",
            "psm2",
            f"{step}"   
        ])

        # ---------------------------------------- PSM1 grasp needle by tip ----------------------------------------
        run_step([
            "ros2", "run", "auto_suture",
            "Grasp_Needle",
            "psm1",
            "tip",
            "up",
            "--ros-args",
            "--params-file",
            "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
        ])

        # ---------------------------------------- PSM1 grab and PSM2 let go ----------------------------------------
        psm1_grab_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm1",
            "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
        ])


        psm2_drop_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm2",
            "0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.5"
        ])

        psm2_drop_needle.wait()
        psm1_grab_needle.wait()

        # ---------------------------------------- Needle extraction through exit ----------------------------------------
        run_step([
            "ros2", "run", "auto_suture",
            "Needle_Extraction",
            "psm1",
            f"{step}"
        ])


        # ---------------------------------------- Needle handover ----------------------------------------


        run_step([
            "ros2", "run", "auto_suture",
            "Grasp_Needle",
            "psm2",
            "grip",
            "up",
            "--ros-args",
            "--params-file",
            "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
        ])


        psm2_grab_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm2",
            "0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
        ])


        psm1_drop_needle = start_step([
            "ros2", "run", "auto_suture",
            "move_to_pose",
            "psm1",
            "0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.5"
        ])

        psm1_drop_needle.wait()
        psm2_grab_needle.wait()

    # ---------------------------------------- Exit ----------------------------------------

    print("\n\nSuturing complete... \n\nExiting...")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()