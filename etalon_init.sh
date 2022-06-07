#!/bin/bash
# This scripts initializes Etalon. Run this script before installing Etalon.

##########################################################
# Set variables in the section below to your own values. #
##########################################################
H1="machine1.cs.cmu.edu" # hostname of machine 1.
H2="machine2.cs.cmu.edu" # hostname of machine 2.
H3="machine3.cs.cmu.edu" # hostname of machine 3.
SW="switch.cs.cmu.edu" # hostname of the switch machine.
DATA_IF="enp6s0f0" # data interface name.
CTRL_IF="enp6s0f0" # control interface name.
MGMT_IF="enp6s0f0" # management interface name.
##########################################################
#                 End of section.                        #
##########################################################

MGMT_MAC=$(ifconfig $MGMT_IF | grep ether | awk '{print $2}')

sed -i "s/host1 \+/host1 $H1/g" etalon/etc/handles
sed -i "s/host2 \+/host2 $H2/g" etalon/etc/handles
sed -i "s/host3 \+/host3 $H3/g" etalon/etc/handles
sed -i "s/switch \+/switch $SW/g" etalon/etc/handles
sed -i "s/DATA_IF=enp68s0/DATA_IF=$DATA_IF/g" etalon/etc/script_config.sh
sed -i "s/CONTROL_IF=eno4/CONTROL_IF=$CTRL_IF/g" etalon/etc/script_config.sh
sed -i "s/MANAGE_IF=enp68s0d1/MANAGE_IF=$MGMT_IF/g" etalon/etc/script_config.sh
sed -i "s/DATA_EXT_IF = 'enp68s0'/DATA_EXT_IF = '$DATA_IF'/g" etalon/etc/python_config.py
sed -i "s/CONTROL_EXT_IF = 'eno4'/CONTROL_EXT_IF = '$CTRL_IF'/g" etalon/etc/python_config.py
sed -i "s/MANAGE_EXT_IF = 'enp68s0d1'/MANAGE_EXT_IF = '$MGMT_IF'/g" etalon/etc/python_config.py
sed -i "s/TDN_UPDATE_SRC_MAC = 'f4:52:14:33:28:d1'/TDN_UPDATE_SRC_MAC = '$MGMT_MAC'/g" etalon/etc/python_config.py
sed -i "s/enp68s0/$DATA_IF/g" etalon/etc/netplan/99-etalon.yaml
sed -i "s/eno4/$CTRL_IF/g" etalon/etc/netplan/99-etalon.yaml
sed -i "s/enp68s0d1/$MGMT_IF/g" etalon/etc/netplan/99-etalon.yaml
