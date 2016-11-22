#
# rn4020.py
#
#    Interface to the "base station" for ARBattles.  The "base station" is
#    an rn4020 connected to a FTDI usb/serial port.  So we talk to the rn4020
#    serially.
#

import time
import serial
import re

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

        self.serial.write("Y\n")            # turn off any previous broadcast
        self.serial.readline()              # get the AOK

        # message through the RN4020 need to be in HEX

        msg = rn4020.magicNum
        msg += convertToHex(e, 1)
        msg += convertToHex(m, 1)
        msg += convertToHex(st, 2)
        msg += convertToHex(sp, 1)
        print msg

        self.serial.write("N," + msg + "\n") # set-up the message to be broadcast
        self.serial.readline()               # get the AOK

        self.serial.write("A,0000,0001\n")  # start the broadcast with a "single message" config
        self.serial.readline()              # get the AOK

        return True

    #
    # receivePrepare() - prepares the RN4020 for reception of broadcast messages.
    #                    After this is called, you should use receive() to get the
    #                    messages.  But don't take too long to get started! You
    #                    could miss a message.
    #
    def receivePrepare(self):
        self.serial.write("X\n")            # turn off any previous listening
        self.serial.flushInput()            # flush the input buffer
        self.serial.write("J,1\n")          # puts the RN4020 in observer role
        self.serial.readline()              # get the AOK
        
        # now setup the scanning - we want to go as long as possible
        # which through trial and error is 0x2800 (10240 ms, 10 sec)
        self.serial.write("F,2800,2800\n")
        self.serial.readline()                   # get the AOK

    #
    # receive() - sits and waits for a broadcast reception. Note that only those
    #             messages that have both the correct magic string and correct
    #             format will count as "being received." Other (bad) messages are
    #             quietly ignored by this routine. When a good message is received,
    #             it is returned as a list with: [E#, M#, ST, SP, RT, RP]
    #             command is called, it re-program
    def receive(self):
        msg = self.serial.readline()               # this will wait, or "block", until a line comes in

        # in one fell swoop, we check to see if it is a good message as extract
        # the data from the message. The following pattern extracts each component
        # of the message, but only if it matches the broadcast message pattern
        # and has the right magic number, otherwise it doesn't match.
        
        pattern = "([^,]+),([^,]+),([^,]+),Brcst:" + rn4020.magicNum + "(.*)"
        
        match = re.match(pattern,msg)
        if match:
            
            btMacAddr = match.group(1)            # mac address of the transmitter (48 bits)
            btAddrType = match.group(2)           # addres type (1 bit)
            rssi = match.group(3)                 # rssi (8 bit)
            imsg = match.group(4)                 # message from the sender - 10 bytes
            
            if len(imsg) < 10:
                return None
            #                  e                 m                st                sp            rp
            return [ int(imsg[0:2],16),int(imsg[2:4],16),int(imsg[4:8],16),int(imsg[8:],16),int(rssi,16) ]
                
            return None
                

