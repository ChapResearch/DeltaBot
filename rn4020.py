#
# rn4020.py
#
#    Interface to the "base station" for ARBattles.  The "base station" is
#    an rn4020 connected to a FTDI usb/serial port.  So we talk to the rn4020
#    serially.
#

import time
import serial

# it would be "nice" if we were able to figure out what port the base station is connected to
# but since we're operating in both Windows and Linux land, it's impossible.  So it has to be
# coded in the constructor.

class rn4020:

    # this needs to be called with something like COM10 on Windows, and /dev/ttyUSB0 for Linux
    # we default to the default rn4020 speed

    magicNum = "C415AB"

    def __init__(self,port):
        self.serial = serial.Serial(port,115200)
        self.moduleInit()

    #
    # moduleInit() - initialize the module for broadcast
    #
    def moduleInit(self):
        pass

    def broadcast(self,payload):

        #convert string, seperated by spaces, into hexadecimal
        

        # first set the payload with "N,"
        # then set advertising with "A" along with speed
        outString = "Y\n"

        # Send N command (for sending data), send magic number, experiment number, message number, sending-power and delta sending-time
        outString = "N," + rn4020.magicNum + payload + "\n"

        #goes for one send, smallest possible time range
        outString += "A,0000,0001\n"

        self.serial.write(outString)


