import socket
import struct
import sys
import usb.core
import time
import threading

#https://bitbucket.org/hardbyte/python-can/src/4baa9ebb48c1fa6702613c617972ea46b5d4206f/can/interfaces/socketcan_native.py?at=default
#https://libbits.wordpress.com/2012/05/22/socketcan-support-in-python/
#http://www.loopybunny.co.uk/CarPC/can/1D6.html 
# CAN frame packing/unpacking (see `struct can_frame` in <linux/can.h>)
can_frame_fmt = "=IB3x8s"

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
class AOA2HID(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                #Find Device in AOA2 audio out mode 18d1 = Google 2d02 = AOA2 Audio Mode
                #other possible ID's: 0x2D03 = audio + adb, 0x2D04 = accessory + audio, 0x2D05 = accessory + audio + adb
                #so far all devices tried identify themselves to be 18d1 & 2d02 once put into audio out mode, regardless of original$
                self.dev = usb.core.find(idVendor=0x18d1, idProduct=0x2d02)
                #Register a HID device with made up ID=0x10, ACCESSORY_REGISTER_HID=54
                self.dev.ctrl_transfer(0x40, 54,0x10, len(keyboardHid), "")
                #send HID Descriptor, ACCESSORY_SET_HID_REPORT_DESC=56
                self.dev.ctrl_transfer(0x40, 56,0x10, 0, keyboardHid,1000)
                self.NotRunning = True
                self.cmd = [0x00]
                print("made thread")
        def run(self):
                if self.NotRunning:
                        self.NotRunning = False
                        #send HID Event
                        self.dev.ctrl_transfer(0x40, 57,0x10, 0,self.cmd,1000)
                        #send HID event for no keys pressed, necessary or key pressed will repeat themselves
                        self.dev.ctrl_transfer(0x40, 57,0x10, 0,NoKeys_cmd,1000)
                        self.NotRunning = True
                        print("command made")
                        print(self.cmd)
        def __del__(self):
                #unregister HID Device, ACCESSORY_UNREGISTER_HID = 55
                self.dev.ctrl_transfer(0x40, 55,0x10, 0, "")




#---------------- HID Stuff End -------------------


 
def build_can_frame(can_id, data):
        can_dlc = len(data)
        data = data.ljust(8, b'\x00')
        return struct.pack(can_frame_fmt, can_id, can_dlc, data)
 
def dissect_can_frame(frame):
        can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
        return (can_id, can_dlc, data[:can_dlc])
 
if len(sys.argv) != 2:
        print('Provide CAN device name (can0, slcan0 etc.)')
        sys.exit(0)
 
# create a raw socket and bind it to the given CAN interface
s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind((sys.argv[1],))

hid = AOA2HID()
hid.cmd = Play_cmd
hid.start()

while True:
	# Fetching the Arb ID, DLC and Data
        try:
                cf, addr = s.recvfrom(16)
                can_id, can_dlc, data = dissect_can_frame(cf)
                print('Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf))

                if can_id == 470:
                        print("CAN ID Caught")
                        int_data = int.from_bytes(data,byteorder='little',signed=False)
                        #print(int_data)
                        if int_data == 0x0CC0: #No Keys Pressed (ping)
                                print("Ping")
                        elif int_data == 0x0CE0: #Up Button
                                print("Up Button")
                                hid.cmd = Next_cmd
                                hid.start()
                        elif int_data == 0x0CD0: #Down Button
                                print("Down Button")
                                hid.cmd = Previous_cmd
                                hid.start()
                        elif int_data == 0x0CC1: #Phone Button
                                print("Phone Button")
                                hid.cmd = Play_cmd
                                hid.start()
                        elif int_data == 0x0DC0: #Voice Button
                                print("Voice Button")
        except KeyboardInterrupt:
                print("\n\nCaught Keyboard interupt")
                exit()
                del hid

#Previous_cmd = [0x01] #Previous Track
#Next_cmd = [0x02] #Next Track
#Play_cmd = [0x04] #Play/Pause
#Stop_cmd = [0x08] #Stop
#NoKeys_cmd = [0x00] #no key pressed

