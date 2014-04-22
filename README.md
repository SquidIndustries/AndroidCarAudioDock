AndroidCarAudioDock
===================
![alt text](http://i.imgur.com/qwmLS3N.png "Diagram")


Software for running a USB audio dock using Android Open Accessory Protocol 2.  
USB audio over AOA2 is supported on all Android devices with OS version 4.1 and up. 

# Current Features

* supports all Android devices with OS version 4.1 and up
* Creates alsaloop back device between Android device and sound card
* Sends Play/Pause command to device. This should cause last open APP to start playing
* Track/Play/Pause via steering wheel buttons on BMW e90. Commands are recieved via cars k-can bus (only supported on Beagebone Black)

# Limitations/issues
* USB 2.0 is limited to 500mA charge current by the USB standard. Some third party kernels for Android devices have the ability to bypass this limit.
* project is a work in progress. I try to keep code in repository functional.

# Installation

# OS
## Beaglebone Black
if on beaglebone black, use Debian 7.2 image from [armf.com](http://www.armhf.com/index.php/boards/beaglebone-black/#wheezy)  
I used [this version](http://s3.armhf.com/debian/wheezy/bone/debian-wheezy-7.2-armhf-3.8.13-bone30.img.xz)

Install to device and boot up into os using [these directions](http://www.armhf.com/index.php/getting-started-with-ubuntu-img-file/).  
Then setup module dependancies... I had to do this, later versions may not require it.

    sudo depmod -a -v "3.8.13-bone30"  


## Other

From this point on, these directions should work on any debian based linux installation. You may need to remove pulseaudio and install alsa if its installed though.

## Update & Install Necessary Software
Update OS

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get dist-upgrade
Install git & alsa

    sudo apt-get install git alsa-base alsa-utils
Give debian user permission to use audio device.

    sudo adduser debian audio
Reboot or log out of all sessions and then log in again so new permissions take hold

    sudo reboot

## Install pyusb

    git clone https://github.com/walac/pyusb
    cd pyusb
    sudo python setup.py install

## Install AndroidCarAudioDock

    cd ~/
    git clone https://github.com/SquidIndustries/AndroidCarAudioDock.git
    cd AndroidCarAudioDock
    sudo ./install.sh
    
## Setup CAN bus
* [Follow these instructions](http://www.embedded-things.com/bbb/enable-canbus-on-the-beaglebone-black/)

## Suggested hardware

* [Beaglebone Black](http://beagleboard.org/Products/BeagleBone+Black)
* [PCM2704 based USB DAC](http://www.amazon.com/gp/product/B00F7IHKC6/ref=oh_details_o07_s01_i01?ie=UTF8&psc=1)
* [Small 4 Port USB hub](http://www.amazon.com/gp/product/B005A0B3FG/ref=oh_details_o02_s00_i00?ie=UTF8&psc=1)
* Greater than or equal to 1A USB power adapter
* [Logic supply beagle bone black case](http://www.amazon.com/gp/product/B00EO7JYTS/ref=oh_details_o00_s01_i00?ie=UTF8&psc=1)

[Picture](http://imgur.com/kSC9rrV) of my setup. I have cut and soldered all the cords to shorter lengths.
![alt text](http://i.imgur.com/kSC9rrVl.jpg "Complete")
![alt text](http://i.imgur.com/V7XgFMWl.jpg "Complete")

## Reference
* [Jacek Fedoryński USB Audio Dock](http://blog.jfedor.org/2013/01/usb-audio-dock-for-android.html)
* [Android AOA2 Documentation](http://source.android.com/accessories/aoa2.html)

## To do

* improve documentation
* post a video of it working
