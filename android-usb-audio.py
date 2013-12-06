#!/usr/bin/env python
#http://www.beyondlogic.org/usbnutshell/usb6.shtml
#http://learn.adafruit.com/hacking-the-kinect/fuzzing


import usb.core
import time
import sys

#find the phone/(usb device)
dev = usb.core.find(idVendor=int(sys.argv[1], 16), idProduct=int(sys.argv[2], 16))
#Read Vendor data from device bmRequestType=0xC0 Device to host Type=class , bmRequest=51=ACCESSORY_GET_PROTOCOL, read 2 bytes
#returns array('B', [2, 0]) if phone is connected
#if device supports AOA2 which has usb audio it will return a 2 here
mesg = dev.ctrl_transfer(0xc0, 51, 0, 0, 2)
# here we should check if it returned version 2
time.sleep(1)
# Enable Audio support, bmRequestType=0x40 Host to device, Type=Class, Request = 58,wValue = 1, 2 channel audio,wIndex = 0,no data
dev.ctrl_transfer(0x40, 58, 1, 0, "")
# putting device in accessory mode
# bmRequestType=0x40 Host to device, Type=Class, Request=53=ACCESSORY_START,wValue = 0,wIndex = 0,no data
dev.ctrl_transfer(0x40, 53, 0, 0, "")
