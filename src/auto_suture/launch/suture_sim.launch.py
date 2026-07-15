from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

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
                    "PYTHONPATH": os.pathsep.join([
                        "/home/jazmin/surgical_robotics_challenge-master/scripts",
                        os.environ.get("PYTHONPATH", "")
                    ])
                },
                output="screen"
            )
        ]
    )


    # Needle frame converter node
    needle_frame_converter = Node(
        package="auto_suture",
        executable="needle_frame_converter",
        name="needle_frame_converter",
        output="screen"
    )

    # Needle position node
    needle_position = Node(
        package="auto_suture",
        executable="needle_position",
        name="needle_position",
        output="screen"
    )

    pkg_path = get_package_share_directory('auto_suture')

    grasp_config = os.path.join(
        pkg_path,
        'config',
        'grasp_offsets.yaml'
    )


    # Tool grasp pose node
    tool_grasp_pose = Node(
        package="auto_suture",
        executable="tool_grasp_pose",
        name="tool_grasp_pose",
        parameters=[grasp_config],
        output="screen"
    )
    

    return LaunchDescription([
        simulation,
        crtk,
        needle_frame_converter,
        needle_position,
        tool_grasp_pose
    ])