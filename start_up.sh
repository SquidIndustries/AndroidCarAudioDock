#!/bin/bash

# Check to see if phone is connectd at startup
if (lsusb | grep -q 18d1)
then (pactl set-sink-volume 0 70%) & (pactl load-module module-loopback source=`pactl list sources short | grep alsa_input.usb | cut -f 1`) & (sleep 3s ; /home/debian/AndroidCarAudioDock/start_play.py 18d1 2d02)
fi
