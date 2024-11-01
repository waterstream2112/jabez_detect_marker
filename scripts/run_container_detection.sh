#!/bin/bash

cd /ros1_ws
source /opt/ros/noetic/setup.bash
catkin_make --pkg jabez_detect_marker
source devel/setup.bash

roslaunch jabez_detect_marker launch_node_detect_marker.launch