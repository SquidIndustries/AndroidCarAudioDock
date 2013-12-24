AndroidCarAudioDock
===================

Software for running a audio dock using Android Open Accessory Protocol 2

USB audio over AOA2 is supported on all android devices 4.1 and up. 

Current Features/limitations

-audio loopback device between android device and sound card are made both at boot up and when plugged in when booted
-play/pause command is sent to device when audio link is made. This should make the last open sound application start playing
-currently only setup to work with Google Nexus devices only (only need to change vendor ID in udev rule)
-recent change to alsa from pulseaudio has greatly reduced CPU usage and improved sound quality

To do
-create blog page on how to setup software and hardware
-Clean up code/comments. Allow things to be configurable rather than hard coded
-implement CAN interface for receiving steering wheel button presses from BMW CAN bus
-add bluetooth A2DP source
-add shairplay to support apple air play

Suggested hardware
-beaglebone black
-PCM2704 based USB DAC
-Small 4 Port USB hub
-Greater than 1A car USB power adapter
-logic supply beagle bone black case

Picture of my setup. I have cut and soldered all the cords to shorter lengths.

http://imgur.com/kSC9rrV

To give credit where credit is due the following has been referenced in creation of this project

http://blog.jfedor.org/2013/01/usb-audio-dock-for-android.html
