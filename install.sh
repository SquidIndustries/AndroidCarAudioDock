#!/bin/bash

#build proper module interfaces
#sudo depmod -a -v "3.8.13-bone30"
#Update Sources and install necessary software for dock
#sudo apt-get update
#sudo apt-get install git alsa-base alsa-utils
#sudo adduser debian audio

#Install pyusb
#git clone https://github.com/walac/pyusb
#cd pyusb
#sudo python setup.py install

#Install docking related files
cp ./systemfiles/dock.rules /etc/udev/rules.d/
chmod +x ./androiddocked.sh
cp ./androiddocked.sh /usr/local/bin/
chmod +x ./aoa2hid.py 
cp ./aoa2hid.py /usr/local/bin/
chmod +x ./aoa2usbaudio.py
cp ./aoa2usbaudio.py /usr/local/bin/
#comment the 2 following lines if youre not going to use CAN
chmod +x ./CANAOA2ctrl.py
cp CANAOA2ctrl.py /usr/local/bin/
