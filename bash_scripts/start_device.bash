#!/bin/bash

#sudo rfkill unblock all
#sudo systemctl restart hostapd.service
#sudo apt update && upgrade -y

sudo groupadd gpio
sudo adduser $USER gpio
sudo chown root.gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem

source /opt/ros/foxy/setup.bash
source $HOME/deployment_ws/install/setup.bash
#ros2 launch dry_contact_lift_sensor chart_lift_node.launch.xml
