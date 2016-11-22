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

def convertToHex(i, bytes):
    if bytes == 1:
        return "%0.2X" %i
    if bytes == 2:
        return "%0.4X" %i

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

    #
    # setPower() - Tells the rn4020 the power to transmit at
    #
    def setPower(self, powerString):
        outString = "sp," + powerString
        self.serial.write(outString)

    
    #
    # broadcast() - Sends one message to the rn4020 with the given data
    #               e = experiment number between 0 and 255
    #               m = message number between 0 and 255
    #               st = sender time number between 0 and 65,535
    #               sp = sender power between 0 and 255, power assumed to be negative
    #
    def broadcast(self, e, m, st, sp):
        e = int(e)
        m = int(m)
        st = int(st)
        sp = int(sp)
        
        #convert payload to a string (Magic# (C415AB), E#, M#, Sender-Time, Sender-Power), seperated by spaces, into hexadecimal
        if e < 0 or e > 255:
            return False
        if (m < 0 or m > 255):
            return False
        if (st < 0 or st > 65535):
            return False
        if (sp < 0 or sp > 255):
            return False
        msg = rn4020.magicNum
        msg += convertToHex(e, 1)
        msg += convertToHex(m, 1)
        msg += convertToHex(st, 2)
        msg += convertToHex(sp, 1)
        print msg

        # first set the payload with "N,"
        # then set advertising with "A" along with speed
        outString = "Y\n"
        # Send N command (for sending data), send magic number, experiment number, message number, sending-power and delta sending-time
        outString = "N," + msg + "\n"

        #goes for one send, smallest possible time range
        outString += "A,0000,0001\n"

        self.serial.write(outString)

        return True

