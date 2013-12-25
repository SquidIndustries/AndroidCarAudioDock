AndroidCarAudioDock
===================

Software for running a audio dock using Android Open Accessory Protocol 2.  
USB audio over AOA2 is supported on all android devices 4.1 and up. 

### Current Features/limitations

* audio loopback device between android device and sound card are made both at boot up and when plugged in when booted
* play/pause command is sent to device when audio link is made. This should make the last open sound application start playing
* Tested with Nexus 5 and Samsung S4, other devices can be added to udev rule file dock.rules

## Installation

#### OS

if on beaglebone black, use Debian 7.2 image from [armf.com](http://www.armhf.com/index.php/boards/beaglebone-black/#wheezy)  
I used [this version](http://s3.armhf.com/debian/wheezy/bone/debian-wheezy-7.2-armhf-3.8.13-bone30.img.xz)

Install to device and boot up into os.  
Then setup module dependancies

    sudo depmod -a -v "3.8.13-bone30"  

These directions should work on any debian based linux installation (including rasbian). You may need to remove pulseaudio and install alsa if its installed though.

#### Update & Install Necessary Software
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

#### Install pyusb

    git clone https://github.com/walac/pyusb
    cd pyusb
    sudo python setup.py install

#### Install AndroidCarAudioDock

    cd ~/
    git clone https://github.com/SquidIndustries/AndroidCarAudioDock.git
    cd AndroidCarAudioDock
    sudo ./install.sh

#### To do

* improve documentation
* implement CAN interface for receiving steering wheel button presses from BMW e90 CAN bus
* add bluetooth A2DP source
* add shairplay to support apple air play

#### Suggested hardware

* [Beaglebone Black](http://beagleboard.org/Products/BeagleBone+Black)
* [PCM2704 based USB DAC](http://www.amazon.com/gp/product/B00F7IHKC6/ref=oh_details_o07_s01_i01?ie=UTF8&psc=1)
* [Small 4 Port USB hub](http://www.amazon.com/gp/product/B004PBDMA0/ref=oh_details_o07_s01_i00?ie=UTF8&psc=1)
* Greater than or equal to 1A USB power adapter
* [Logic supply beagle bone black case](http://www.amazon.com/gp/product/B00EO7JYTS/ref=oh_details_o00_s01_i00?ie=UTF8&psc=1)

[Picture](http://imgur.com/kSC9rrV) of my setup. I have cut and soldered all the cords to shorter lengths.
![alt text](http://i.imgur.com/kSC9rrVl.jpg "Complete")


#### Reference
* [Jacek Fedoryński USB Audio Dock](http://blog.jfedor.org/2013/01/usb-audio-dock-for-android.html)
* [Android AOA2 Documentation](http://source.android.com/accessories/aoa2.html)
