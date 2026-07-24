#!/bin/bash
set -e

cd ~/auto_suture

colcon build --symlink-install

source install/setup.bash

ros2 launch auto_suture suture_sim.launch.py