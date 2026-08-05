#!/usr/bin/env python3

import time
import subprocess
import sys


def run_step(command):
    print(f"\nRunning: {' '.join(command)}")

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"Step failed with return code {result.returncode}")
        sys.exit(result.returncode)

def start_step(command):
    print(f"Starting: {' '.join(command)}")
    return subprocess.Popen(command)

def main():

    # Wait for AMBF simulation and ROS nodes to initialise
    startup_delay = 10
    print(f"Waiting {startup_delay}s for simulation setup...")
    time.sleep(startup_delay)

    # ---------------------------------------- PSM2 grasp needle ----------------------------------------
    grasp_needle = start_step([
        "ros2", "run", "auto_suture",
        "Grasp_Needle",
        "psm2",
        "grip",
        "--ros-args",
        "--params-file",
        "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
    ])

    # ---------------------------------------- PSM1 approach table ----------------------------------------
    psm1_approach_table = start_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm1",
        "0.01, -0.01, 0.15, 0.0, 0.0, 0.0, 0.5"
    ])

    grasp_needle.wait()
    psm1_approach_table.wait()

    # ---------------------------------------- PSM2 pick up needle ----------------------------------------
    run_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm2",
        "0.0, 0.0, -0.002, 0.0, 0.0, 0.0, 0.0"           # psm2 move 2mm up in world frame and close jaw
    ])

    # ---------------------------------------- Needle driving through entry 1 ----------------------------------------
    run_step([
        "ros2", "run", "auto_suture",
        "Needle_Driving"
    ])

    # ---------------------------------------- PSM1 grasp needle by tip ----------------------------------------
    run_step([
        "ros2", "run", "auto_suture",
        "Grasp_Needle",
        "psm1",
        "tip",
        "--ros-args",
        "--params-file",
        "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
    ])

    # ---------------------------------------- PSM1 grab and PSM2 let go ----------------------------------------
    psm1_grab_needle = start_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm1",
        "0.0, -0.0005, -0.0005, 0.0, 0.0, 0.0, 0.0"
    ])


    psm2_drop_needle = start_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm2",
        "0.0, 0.0, -0.05, 0.0, 0.0, 0.0, 0.5"
    ])

    psm2_drop_needle.wait()
    psm1_grab_needle.wait()

    # ---------------------------------------- Needle extraction through exit 1 ----------------------------------------
    run_step([
        "ros2", "run", "auto_suture",
        "Needle_Extraction"
    ])

    
    run_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm1",
        "-0.08, 0.0, 0.0, 0.0, -2, 0.0, 0.0"
    ])

    # ---------------------------------------- Needle handover ----------------------------------------

    run_step([
        "ros2", "run", "auto_suture",
        "Grasp_Needle",
        "psm2",
        "grip",
        "--ros-args",
        "--params-file",
        "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
    ])

    psm2_grab_needle = start_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm2",
        "0.0, -0.0005, -0.0005, 0.0, 0.0, 0.0, 0.0"
    ])


    psm1_drop_needle = start_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm1",
        "0.0, 0.0, -0.05, 0.0, 0.0, 0.0, 0.5"
    ])

    psm1_drop_needle.wait()
    psm2_grab_needle.wait()


    # ---------------------------------------- Exit ----------------------------------------

    print("\n\nSuturing complete... \n\nExiting...")


if __name__ == "__main__":
    main()