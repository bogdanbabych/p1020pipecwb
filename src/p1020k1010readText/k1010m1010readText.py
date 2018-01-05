'''
Created on 18 Dec 2017

@author: bogdan
'''
import sys, os, re
import pathlib
import xml.etree.ElementTree as ET


class clReadTMX(object):
	'''
	readsTMX file / string and outputs one-line per-sentence output 
	'''
	def __init__(self, STmxIn):
		'''
		Constructor
		'''

		# print("output\n", STmxIn)
		self.getFileOut(sys.argv[1])
		return
	
	def getFileOut(self, SInputFileName = './clReadTMX-input.txt'):
		SHead, Tail = os.path.split(SInputFileName)
		SRoot, SExtension = os.path.splitext(Tail)
		SRootOut = SRoot + 's01' + SExtension
		SFileNameOut = os.path.join(SHead, SRootOut)
		
		print ("%(SHead)s %(Tail)s %(SRoot)s %(SExtension)s %(SFileNameOut)s\n" % locals())
		return
	
	def tmx2tree(self, STmxIn):
		root = ET.fromstring(STmxIn)
		return

if __name__ == '__main__':
	STmxIn = pathlib.Path(sys.argv[1]).read_text()
	OReadTMX = clReadTMX(STmxIn)
	pass

