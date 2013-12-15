#!/bin/bash

# Put android device into AOA2 usb audio out mode
/home/debian/AndroidCarAudioDock/android-usb-audio.py $1 $2

# wait 3 seconds for device to switch over, then connect android device to output device, wait 3seconds and send HID play/pause command
# AOA2 is 16bit 2 channel, 44.1hkz
# 50ms buffer
# Sync mode to match input sample rate to output sample rate
#	 5 or auto       - automatically selects the best method
#	 in this order: captshift, playshift,
#        samplerate, simple


(sleep 3s ; alsaloop -P hw:1,0,0 -C hw:2,0,0 -f S16_LE -r 44100 -t 50000 -S 5) & (sleep 3s ; /home/debian/AndroidCarAudioDock/start_play.py 18d1 2d02)&

