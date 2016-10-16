from rn4020 import rn4020


device = rn4020('COM3')
eNum = raw_input("Enter the experiment nummber: ")
print eNum

pNum = raw_input("Enter the power: ")
print pNum


#(E#, M#, Sender-Time, Sender-Power)
device.broadcast(eNum, pNum, 3, 4)