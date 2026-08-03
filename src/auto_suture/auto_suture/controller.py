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


    run_step([
        "ros2", "run", "auto_suture",
        "Grasp_Needle",
        "psm2",
        "grip",
        "--ros-args",
        "--params-file",
        "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
    ])

    run_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm2",
        "0.0, 0.0, -0.002, 0.0, 0.0, 0.0, 0.0"           # psm2 move 2mm up in world frame and close jaw
    ])

    run_step([
        "ros2", "run", "auto_suture",
        "Needle_Driving"
    ])

    run_step([
        "ros2", "run", "auto_suture",
        "Grasp_Needle",
        "psm1",
        "tip",
        "--ros-args",
        "--params-file",
        "/home/jazmin/auto_suture/install/auto_suture/share/auto_suture/config/grasp_offsets.yaml"
    ])


    let_go = start_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm2",
        "0.0, 0.0, -0.005, 0.0, 0.0, 0.0, 0.5"
    ])

    grab = start_step([
        "ros2", "run", "auto_suture",
        "move_to_pose",
        "psm1",
        "0.0, -0.001, -0.001, 0.0, 0.0, 0.0, 0.0"
    ])

    let_go.wait()
    grab.wait()

    print("\n\nSuturing complete... \n\nExiting...")


if __name__ == "__main__":
    main()