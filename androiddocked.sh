#!/bin/bash

# Put android device into AOA2 usb audio out mode
/usr/local/bin/aoa2usbaudio.py $1 $2
# wait 3 seconds for device to switch over, then connect android device to output device, wait 3seconds and send HID play/pause command
# AOA2 is 16bit 2 channel, 44.1hkz
# 50ms buffer
# Sync mode to match input sample rate to output sample rate
#	 5 or auto       - automatically selects the best method
#	 in this order: captshift, playshift,
#        samplerate, simple


(sleep 3s ; alsaloop -P hw:1,0,0 -C hw:2,0,0 -f S16_LE -r 44100 -t 50000 -S 2)&
#(sleep 3s ; /usr/local/bin/aoa2hid.py 18d1 2d02)

#
if /bin/grep --quiet BB-DCAN1 /sys/devices/bone_capemgr.*/slots; then
  #CAN is already setup, just run CAN interface code
  (sleep 3s ; /usr/local/bin/python3.3 /usr/local/bin/CANAOA2ctrl.py)&
else
  /bin/echo BB-DCAN1 > /sys/devices/bone_capemgr.*/slots
  sleep 0.1s
  /bin/ip link set can0 type can bitrate 100000 triple-sampling on
  /bin/ip link set can0 up
  (sleep 3s ; /usr/local/bin/python3.3 /usr/local/bin/CANAOA2ctrl.py)&
fi
