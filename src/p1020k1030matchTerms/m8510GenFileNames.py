'''
Created on 26 Mar 2018

@author: bogdan
'''
import sys, os

class clGenFineNames(object):
	'''
	generates file names from input file name pattern	
	'''
	
	def __init__(self, SFNameTemplate = sys.argv[1], LFExtensionsOut= ['.out'] ):
		SHead, Tail = os.path.split(SFNameTemplate) # splitting directory name from file+extension name
		SRoot, SExtension = os.path.splitext(Tail) # splitting extension from the Tail (file+extension)
		self.LFNOut = []
		for el in LFExtensionsOut:
			SFNOut = SRoot + el
			SDirFNOut = os.path.join(SHead, SFNOut)
			self.LFNOut.append(SDirFNOut)
		
		return
	
	def getData(self):
		return self.LFNOut
	
	# end clGenFineNames class
