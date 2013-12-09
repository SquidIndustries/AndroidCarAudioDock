#!/bin/bash

/home/debian/AndroidCarAudioDock/android-usb-audio.py $1 $2
#reduce volume so USB dac output isn't distorted

#test to see if pulseaudio is running. if it is, set android device as input and then start play back via HID command
if (ps -A | grep -q pulseaudio)
then (pactl set-sink-volume 0 70%) & (sleep 3s ; pactl load-module module-loopback source=`pactl list sources short | grep alsa_input.usb | cut -f 1`) & (sleep 3s ; /home/debian/AndroidCarAudioDock/start_play.py 18d1 2d02)&
fi


#pactl set-volume-sink alsa_output.usb-Burr-Brown_from_TI_USB_Audio_DAC-00-DAC.analog-stereo 70% &
#(sleep 3s ; pactl load-module module-loopback source=`pactl list sources short | grep alsa_input.usb | cut -f 1`) &
#use following line instead of above for Fiio E10 USB Dac
#(sleep 3s ; pactl load-module module-loopback source=3) &

#start play back via HID command
#(sleep 1s ; /home/debian/AndroidCarAudioDock/start_play.py 18d1 2d02)&

