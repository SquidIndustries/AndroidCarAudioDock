#!/bin/bash

#build proper module interfaces
sudo depmod -a -v "3.8.13-bone30"
#Update Sources and install necessary software for dock
sudo apt-get update
sudo apt-get install git alsa-base alsa-utils
sudo adduser debian audio

#Install pyusb
git clone https://github.com/walac/pyusb
cd pyusb
sudo python setup.py install

#Install docking related files
sudo cp ./dock.rules /etc/udev/rules.d/

