AndroidCarAudioDock
===================

Software for running a audio dock using Android Open Accessory Protocol 2

USB audio over AOA2 is supported on all android devices 4.1 and up. 

Current Features/limitations
----------------------------
* audio loopback device between android device and sound card are made both at boot up and when plugged in when booted
* play/pause command is sent to device when audio link is made. This should make the last open sound application start playing
* Tested with Nexus 5 and Samsung S4, other devices can be added to udev rule file dock.rules

Installation
============
OS
--
if on beaglebone black, use Debian 7.2 image from http://www.armhf.com/index.php/boards/beaglebone-black/#wheezy
I used this version
http://s3.armhf.com/debian/wheezy/bone/debian-wheezy-7.2-armhf-3.8.13-bone30.img.xz

Install to device and boot up into os. 
Then setup module dependancies
sudo depmod -a -v "3.8.13-bone30"

These directions should work on any debian based linux installation (including rasbian). You may need to remove pulseaudio if its installed though.

Install pyusb
-------------
git clone https://github.com/walac/pyusb
cd pyusb
sudo python setup.py install

Install AndroidCarAudioDock
---------------------------
cd ~/
git clone https://github.com/SquidIndustries/AndroidCarAudioDock.git
cd AndroidCarAudioDock
sudo ./install.sh

To do
=====
* implement CAN interface for receiving steering wheel button presses from BMW e90 CAN bus
* add bluetooth A2DP source
* add shairplay to support apple air play

Suggested hardware
==================
* beaglebone black
* PCM2704 based USB DAC
* Small 4 Port USB hub
* Greater than 1A car USB power adapter
* logic supply beagle bone black case

Picture of my setup. I have cut and soldered all the cords to shorter lengths.

http://imgur.com/kSC9rrV

To give credit where credit is due the following has been referenced in creation of this project

http://blog.jfedor.org/2013/01/usb-audio-dock-for-android.html
