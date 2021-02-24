#!/bin/bash

#sudo rfkill unblock all
#sudo systemctl restart hostapd.service
#sudo apt update && upgrade -y

# sudo groupadd gpio
# sudo adduser $USER gpio
# sudo chown root.gpio /dev/gpiomem
# sudo chmod g+rw /dev/gpiomem

source /opt/ros/foxy/setup.bash
source $HOME/repos/pi_driver/install/setup.bash
# udevadm trigger
ros2 launch dry_contact_lift_sensor chart_lift_node.launch.xml

# black magic command for symbolic link of udev rules
# DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd
# ln -s $DIR/99-gpio.rules /etc/udev/rules.d
