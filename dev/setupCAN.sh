#!/bin/bash

echo BB-DCAN1 > /sys/devices/bone_capemgr.*/slots
sleep 0.1s
ip link set can0 type can bitrate 100000 triple-sampling on
ip link set can0 up
