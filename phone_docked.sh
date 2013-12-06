#!/bin/bash

/home/debian/CarDock/android-usb-audio.py $1 $2
#reduce volume so USB dac output isn't distorted
pactl set-volume-sink alsa_output.usb-Burr-Brown_from_TI_USB_Audio_DAC-00-DAC.analog-stereo 70% &
(sleep 3s ; pactl load-module module-loopback source=`pactl list sources short | grep alsa_input.usb | cut -f 1`) &
#use following line instead of above for Fiio E10 USB Dac
#(sleep 3s ; pactl load-module module-loopback source=3) &

