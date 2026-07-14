from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
import os


def generate_launch_description():

    # Launch the AMBF simulator
    simulation = ExecuteProcess(
        cmd=[
            "/home/jazmin/surgical_robotics_challenge-master/run_env_SIMPLE_LND_420006.sh"
        ],
        cwd="/home/jazmin/surgical_robotics_challenge-master",
        shell=True,
        output="screen"
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
                    "PYTHONPATH": "/home/jazmin/surgical_robotics_challenge-master/scripts"
                },
                output="screen"
            )
        ]
    )

    # Needle position node
    needle_position = Node(
        package="auto_suture",
        executable="needle_position",
        name="needle_position",
        output="screen"
    )

    # Tool grasp position node
    tool_grasp_position = Node(
        package="auto_suture",
        executable="tool_grasp_position",
        name="tool_grasp_position",
        output="screen"
    )

    return LaunchDescription([
        simulation,
        crtk,
        needle_position,
        tool_grasp_position
    ])