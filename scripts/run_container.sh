#!/bin/bash

cd $HOME/ros1_ws

if [ $1 == "up" ]; then
    # xhost +local:docker
    docker compose -f src/jabez_detect_marker/container/docker-compose.yaml up

elif [ $1 == "exec" ]; then
    docker compose -f src/jabez_detect_marker/container/docker-compose.yaml exec jabez_detect_marker \
     /bin/bash /ros1_ws/src/jabez_detect_marker/container/startup.sh
     
elif [ $1 == "down" ]; then
    docker compose -f src/jabez_detect_marker/container/docker-compose.yaml down
fi