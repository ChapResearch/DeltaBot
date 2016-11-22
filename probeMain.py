#
# probeMain.py
#
#   Code to run the DeltaBot probes.
#

from rn4020 import rn4020
from OFile import OFile
from pprint import pprint
import signal

# 3. Turn on broadcast reception
# 4. Log each incoming broadcast
#

# Get the name of this probe for the output file

probe = raw_input("Which probe is this: ")

validProbes = ["A","B","C","D"]

if probe not in validProbes:
    print "Bad User! Valid probes are:"
    pprint(validProbes)

# Create the output file, but don't crash in to the previous one.
# 
# Note that the name of the file CANNOT have a dash in it.
# so "probe-A" is bad!  It confuses OFile. Do "probeA" instead.

outFile = OFile("probeData" + probe)
print "Output file is: " + outFile.name

# configure broadcast reception

ble = rn4020("/dev/ttyUSB0")

ble.receivePrepare()

while True:

    data = ble.receive()

    if data is None:       # bad message (wrong magic, size, etc) came in
        continue

    if not data:           # interrupted
        break;

    eNum = data[0]
    mNum = data[1]
    st = data[2]
    sp = data[3]
    rp = data[4]

    outFile.write([probe,eNum,mNum,st,sp,rp])

print
print "Closing file and exiting."
outFile.close()
