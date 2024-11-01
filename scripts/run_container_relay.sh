#!/bin/bash

cd /ros1_ws
source /opt/ros/noetic/setup.bash
source devel/setup.bash

rosrun topic_tools drop /multijackal_02/argus/ar0234_front_right/image_raw 1 2 /camera #&
# rosrun topic_tools relay /trigger_detection /trigger_detection_ghost &
# rosrun topic_tools relay /detection_result_orin /detection_result & 