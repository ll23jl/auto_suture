from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os

# !!!!!!! Note: please change simulation file paths as necessary.

def generate_launch_description():

    # Launch the AMBF simulator
    simulation = ExecuteProcess(
        cmd=[
            "/home/jazmin/surgical_robotics_challenge-master/run_env_SIMPLE_LND_420006.sh"
        ],
        cwd="/home/jazmin/surgical_robotics_challenge-master",
        shell=True,
        output="log"
    )

    # Wait for AMBF to start before launching the CRTK interface
    crtk = TimerAction(
        period=5.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    "python3",
                    "/home/jazmin/surgical_robotics_challenge-master/scripts/surgical_robotics_challenge/launch_crtk_interface.py"
                ],
                cwd="/home/jazmin/surgical_robotics_challenge-master",
                env={
                    **os.environ,
                    "PYTHONPATH": os.pathsep.join([
                        "/home/jazmin/surgical_robotics_challenge-master/scripts",
                        os.environ.get("PYTHONPATH", "")
                    ])
                },
                output="log"
            )
        ]
    )


    # Simulation to ECM node
    Simulation_to_ECM_Node = Node(
        package="auto_suture",
        executable="Simulation_to_ECM",
        name="Simulation_to_ECM",
        output="screen"
    )

    # Needle poses node
    Needle_Poses = Node(
        package="auto_suture",
        executable="Needle_Poses",
        name="Needle_Poses",
        output="screen"
    )

    # Entry/exit poses node
    Entry_Exit_Poses = Node(
        package="auto_suture",
        executable="Entry_Exit_Poses",
        name="Entry_Exit_Poses",
        output="screen"
    )



    # Controller node
    Controller = Node(
        package="auto_suture",
        executable="controller",
        name="controller",
        output="screen"
    )



    return LaunchDescription([
        simulation,
        crtk,
        Simulation_to_ECM_Node,
        Needle_Poses,
        Entry_Exit_Poses,
        Controller
    ])