#!/bin/bash

#build proper module interfaces
sudo depmod -a -v "3.8.13-bone30" as root
#Update Sources and install necessary software for dock
sudo apt-get update
sudo apt-get install pulseaudio git
#For edimax wifi EW-7811Un
sudo apt-get install firmware-realtek
sudo echo auto wlan0 >> /etc/network/interfaces
sudo echo iface wlan0 inet dhcp >> /etc/network/interfaces
sudo echo wpa-ssid 2WIRE318 >> /etc/network/interfaces
sudo echo wpa-psk  9748584362 >> /etc/network/interfaces

#Install pyusb
git clone https://github.com/walac/pyusb
cd pyusb
sudo python setup.py install

#Install docking related files
sudo mv /etc/default/pulseaudio /etc/default/pulseaudio.old
sudo cp ./pulseaudio /etc/default/
sudo mv /etc/pulse/system.pa /etc/pulse/system.pa.old
sudo cp ./system.pa /etc/pulse/
sudo mv /etc/pulse/daemon.conf /etc/pulse/daemon.conf.old
sudo cp ./daemon.conf /etc/pulse/
sudo cp ./dock.rules /etc/udev/rules.d/

