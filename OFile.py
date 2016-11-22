#The output file class#

import os
from os import listdir
from os.path import isfile, join

class OFile:
	
	def __init__(self, basename):
		biggest = 0
		self.basename = basename 
		files = listdir(os.path.dirname(os.path.abspath(__file__)))
		onlyfiles = []
		for f in files:
			if isfile(join(os.path.dirname(os.path.abspath(__file__)), f)):
				onlyfiles.append(f)
		for name in onlyfiles:
			nameparts = name.split('-')
			if(nameparts[0] == basename):
				if(int(nameparts[1]) >biggest):
					biggest = int(nameparts[1])
		biggest = biggest+1	
                self.name =  basename + '-' + str(biggest)
		self.fileW = open(self.name, 'w')


	#
	# write() - write the msg to the output file, where #msg is an array consisting of either 
	#		the msg revcieved by the probe or the msg sent by the beacon

	def write(self, msg):
		line = ''		
		for msgElement in msg:
			line += str(msgElement) + ','
		line += '\n'
		self.fileW.write(line)
		return True

	def close(self):
		self.fileW.close()
