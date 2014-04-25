#!/usr/bin/env python3
import socket
import struct
import sys
import usb.core
import time
import threading
import os
import logging

#To Do
# close all threads and exit gracefully when android device goes away
# wait for CAN bus to come up for a peroid of time before erroring out. this is needed for boot up with device connected

#https://bitbucket.org/hardbyte/python-can/src/4baa9ebb48c1fa6702613c617972ea46b5d4206f/can/interfaces/socketcan_native.py?at=default
#https://libbits.wordpress.com/2012/05/22/socketcan-support-in-python/
#http://www.loopybunny.co.uk/CarPC/can/1D6.html 
# CAN frame packing/unpacking (see `struct can_frame` in <linux/can.h>)
can_frame_fmt = "=IB3x8s"

#----------------Logging -------------------
logger = logging.getLogger('CANAOA2ctrl.py')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/tmp/CANAOA2.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

logger.debug('it ran')

# 'application' code
#logger.debug('debug message')
#logger.info('info message')
#logger.warn('warn message')
#logger.error('error message')
#logger.critical('critical message')



#---------------- HID Stuff Start -------------------

#HID Descriptor for device from HID Consumer Page (0x0c)
#device only has the buttons Previous, Next, Play/Pause,Stop,Eject
#HID Descriptor from http://www.picbasic.co.uk/forum/showthread.php?t=14320
picmediahid = [
0x05, 0x0C,             # USAGE_PAGE (Consumer Devices)
0x09,0x01,              # USAGE (Consumer Control)
0xA1,0x01,              # COLLECTION (Application)
0x15,0x00,              #   LOGICAL_MINIMUM (0)
0x25,0x01,              #   LOGICAL_MAXIMUM (1)
0x75,0x01,              #   REPORT_SIZE (1)
0x95,0x05,              #   REPORT_COUNT (5)
0x09,0xb6,              #   USAGE (Scan Previous Track) 0x01
0x09,0xB5,              #   USAGE (Scan Next Track) 0x02
0x09,0xCD,              #   USAGE (Play/Pause) 0x04
0x09,0xB7,              #   USAGE (Stop) 0x08
0x09,0xB8,              #   USAGE (Eject) 0x10
0x81,0x06,              #   INPUT (Data,Var,Rel)
0x95,0x02,              #   REPORT_COUNT (3)
0x09,0xE2,              #   USAGE (Mute)
0x09,0xE9,              #   USAGE (Volume Up)
0x09,0xEA,              #   USAGE (Volume Down)
0x81,0x02,              #   INPUT (Data,Var,Abs)
0xc0            # END_COLLECTION
]

Previous_cmd = [0x01] #Previous Track
Next_cmd = [0x02] #Next Track
Play_cmd = [0x04] #Play/Pause
Stop_cmd = [0x08] #Stop
NoKeys_cmd = [0x00] #no key pressed

keyboardHid = picmediahid

#================AOA2 HID Thread Function==================

class USBdevSetup(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global usbdev
		usbdev = usb.core.find(idVendor=0x18d1, idProduct=0x2d02)
		#Register a HID device with made up ID=0x10, ACCESSORY_REGISTER_HID=54
		usbdev.ctrl_transfer(0x40, 54,0x10, len(keyboardHid), "")
		#send HID Descriptor, ACCESSORY_SET_HID_REPORT_DESC=56
		usbdev.ctrl_transfer(0x40, 56,0x10, 0, keyboardHid,1000)
		self.Running = True
		logger.debug(usbdev)
		#print(usbdev)
	def run(self):
		global usbdev
		while self.Running:
			usbdev = usb.core.find(idVendor=0x18d1, idProduct=0x2d02) #make sure device is still present
			if usbdev is None:
				logger.debug('No USB device found in peroidic check...exiting')
				os._exit(1) #device is no longer present, kill program
			time.sleep(2)	
	def __del__(self):
		global usbdev
		#unregister HID Device, ACCESSORY_UNREGISTER_HID = 55
		usbdev.ctrl_transfer(0x40, 55,0x10, 0, "")
		self.Running = False
		
class AOA2HID(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.Running = True
        self.cmd = [0x00] #holds current command
    def run(self):
        while self.Running:
            threadEvent.wait() #wait without timeout for trigger to do something
            if self.Running:
                global usbdev
                usbdev = usb.core.find(idVendor=0x18d1, idProduct=0x2d02) #make sure device is still present
                logger.debug(usbdev)
                if usbdev is None:
                    logger.debug('No USB device...exiting')
                    os._exit(1) #device is no longer present, kill program 
                else:
                    usbdev.ctrl_transfer(0x40, 57,0x10, 0,self.cmd,1000)
                    #send HID event for no keys pressed, necessary or key pressed will repeat themselves
                    usbdev.ctrl_transfer(0x40, 57,0x10, 0,NoKeys_cmd,1000)
                    time.sleep(0.250)
                    threadEvent.clear() #done, clear set flag
    def __del__(self):
        self.Running = False
        threadEvent.set() #set flag so run() gets out of wait state

#---------------- HID Stuff End -------------------


 
def build_can_frame(can_id, data):
        can_dlc = len(data)
        data = data.ljust(8, b'\x00')
        return struct.pack(can_frame_fmt, can_id, can_dlc, data)
 
def dissect_can_frame(frame):
        can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
        return (can_id, can_dlc, data[:can_dlc])
 
# create a raw socket and bind it to the given CAN interface

try: 
	s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
	logger.debug(s)
except:
        e = sys.exc_info()[0]
        logger.debug("<p>Error1: %s</p>" % e )


try:
	s.bind(('can0',))
	logger.debug(s)
except:
	e = sys.exc_info()[0]
	logger.debug("<p>Error2: %s</p>" % e )
	
threadEvent = threading.Event()

usbchecker = USBdevSetup()
usbchecker.daemon = True
usbchecker.start()

hid = AOA2HID()
hid.daemon = True
hid.cmd = Play_cmd
hid.start()
#threadEvent.set() #send play command

while True:
	# Fetching the Arb ID, DLC and Data
        try:
                cf, addr = s.recvfrom(16)
                can_id, can_dlc, data = dissect_can_frame(cf)
#                logger.debug('Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf))
                if can_id == 470:
                        logger.debug('Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf))
                        if (not (hid.isAlive() & usbchecker.isAlive())):
                                logger.debug("threads are dead")
                                logger.debug(hid.isAlive())
                                logger.debug(usbchecker.isAlive())
                                exit(1)
                        int_data = int.from_bytes(data,byteorder='little',signed=False)
                        logger.debug(int_data)
                        if not threadEvent.is_set(): #check to see if thread is already busy
                                #0x0CC0: #No Keys Pressed (ping)
                                if int_data == 0x0CE0: #Up Button
                                        logger.debug("Up Button")
                                        hid.cmd = Next_cmd
                                        threadEvent.set()
                                elif int_data == 0x0CD0: #Down Button
                                        logger.debug("Down Button")
                                        hid.cmd = Previous_cmd
                                        threadEvent.set()
                                elif int_data == 0x0CC1: #Phone Button
                                        logger.debug("Phone Button")
                                        hid.cmd = Play_cmd
                                        threadEvent.set()
                                elif int_data == 0x0DC0: #Voice Button
                                        logger.debug("Voice Button")
        except KeyboardInterrupt:
                print("\n\nCaught Keyboard interupt")
                del usbchecker
                del hid
                exit()

        except OSError: #to catch when can bus isnt setup yet
                logger.debug("OSerror")
                time.sleep(1)
                continue
                break
