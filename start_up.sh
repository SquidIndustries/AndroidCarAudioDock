#!/bin/bash

# Check to see if phone is connectd at startup
if (lsusb | grep -q 18d1)
then (alsaloop -P hw:1,0,0 -C hw:2,0,0 -f S16_LE -r 44100 -t 50000 -S 3) & (sleep 3s ; /home/debian/AndroidCarAudioDock/start_play.py 18d1 2d02)&

fi
