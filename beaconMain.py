from rn4020 import rn4020
import time
from OFile import OFile

msgCount = 10

#device = rn4020('COM3')
device = rn4020('/dev/ttyUSB0')
eNum = raw_input("Enter the experiment number: ")
print eNum


outFile = OFile("beacon")
print "Output file is: " + outFile.name

msSpacing = 500

for power in [0,1,2,3,4,5,6,7]:
    powerString = str(power)
    device.setPower(powerString)
    
    startTime = 0
    targetTime = time.clock()*1000 + msSpacing
    
    for msg in range(0, msgCount):
        while time.clock()*1000 < targetTime:
            pass
        targetTime = time.clock()*1000 + msSpacing

        device.broadcast(eNum, msg, startTime, power)
        startTime += msSpacing

        #              e  m  st  p
        outFile.write([eNum, msg, startTime, power])
        
    
#(E#, M#, Sender-Time, Sender-Power)


