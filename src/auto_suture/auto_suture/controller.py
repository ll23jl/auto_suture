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

    print("Suturing complete.")


if __name__ == "__main__":
    main()