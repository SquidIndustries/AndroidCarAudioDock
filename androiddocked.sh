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
echo "Dock: Alsaloop up" > /dev/kmsg

#send play command to android device
(sleep 3s ; /usr/local/bin/aoa2hid.py 18d1 2d02)&
echo "Dock: Play command sent to android device" > /dev/kmsg

#CAN stuff
COUNTER=0
while [  $COUNTER -lt 90 ]; do #try 90 times, 1 sec apart for CAN bus to come up
  if /sbin/ifconfig | /bin/grep --quiet can0; then
    #CAN bus is up, run CAN interface code
    echo "Dock: CAN bus up, starting interface code" > /dev/kmsg
    /usr/local/bin/python3.3 /usr/local/bin/CANAOA2ctrl.py&
    break
    exit 0
  else
    echo "CAN bus not up"
  fi
  sleep 1s #wait before trying again
  let COUNTER=COUNTER+1
done
if [ $COUNTER -ge 90 ]; then
  echo "Dock: gave up on waiting for CAN bus" > /dev/kmsg
fi

exit 0
