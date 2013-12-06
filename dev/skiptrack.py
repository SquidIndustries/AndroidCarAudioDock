#!/usr/bin/env python
#http://source.android.com/accessories/aoa2.html

import usb.core
import time
import sys


#HID Descriptor for device from HID Consumer Page (0x0c)
#device only has the buttons Previous, Next, Play/Pause,Stop,Eject
#HID Descriptor from http://www.picbasic.co.uk/forum/showthread.php?t=14320
picmediahid = [
0x05, 0x0C,		# USAGE_PAGE (Consumer Devices)
0x09,0x01,		# USAGE (Consumer Control)
0xA1,0x01,		# COLLECTION (Application)
0x15,0x00,		#   LOGICAL_MINIMUM (0)
0x25,0x01,		#   LOGICAL_MAXIMUM (1)
0x75,0x01,		#   REPORT_SIZE (1)
0x95,0x05,		#   REPORT_COUNT (5)
0x09,0xb6,		#   USAGE (Scan Previous Track) 0x01
0x09,0xB5,		#   USAGE (Scan Next Track) 0x02
0x09,0xCD,		#   USAGE (Play/Pause) 0x04
0x09,0xB7,		#   USAGE (Stop) 0x08
0x09,0xB8,		#   USAGE (Eject) 0x10
0x81,0x06,		#   INPUT (Data,Var,Rel)
0x95,0x02,		#   REPORT_COUNT (3)
0x09,0xE2,		#   USAGE (Mute)
0x09,0xE9,		#   USAGE (Volume Up)
0x09,0xEA,		#   USAGE (Volume Down)
0x81,0x02,		#   INPUT (Data,Var,Abs)
0xc0		# END_COLLECTION
]


keyboardHid = picmediahid

dev = usb.core.find(idVendor=int(sys.argv[1], 16), idProduct=int(sys.argv[2], 16))
#if device is None:
#    sys.exit("Could not find MagTek USB HID Swipe Reader.")


#ACCESSORY_REGISTER_HID=54, Accessory assigned ID = 0x10(made up number)
#Register a HID device with ID=0x10 
#ctrl_transfer( bmRequestType, bRequest, wValue, wIndex, data_or_wLength=None, timeout=None)

dev.ctrl_transfer(0x40, 54,0x10, len(keyboardHid), "")


#ACCESSORY_SET_HID_REPORT_DESC=56
#send HID Descriptor
dev.ctrl_transfer(0x40, 56,0x10, 0, keyboardHid,1000)

time.sleep(0.2) #need this pause or scipt crashes

#m = [0x01] #Previous Track
m = [0x02] #Next Track
#m = [0x04] #Play/Pause
#m = [0x08] #Stop
#m = [0x10] #Eject
  
#ACCESSORY_SEND_HID_EVENT=57
#send HID Event
dev.ctrl_transfer(0x40, 57,0x10, 0,m,1000)

m = [0x00]
#send HID event for no keys pressed, necessary or key pressed will repeat themselves
dev.ctrl_transfer(0x40, 57,0x10, 0,m,1000)

time.sleep(1)
#unregister HID Device
#ACCESSORY_UNREGISTER_HID = 55
#dev.ctrl_transfer(0x40, 55,0x10, 0, "")


