from rn4020 import rn4020


device = rn4020('COM3')
device.broadcast(1,2,3,4)
