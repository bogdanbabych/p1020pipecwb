'''
Created on 26 Mar 2018

@author: bogdan
'''

import sys, os, re
import pathlib

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
			self.LSFNOut.append(SDirFNOut)
		
		return
	
	def getData(self):
		return self.LFNOut
	
	# end clGenFineNames class

class clReadTermsFromText(object):
	'''
	reads terminology separated by hyphen; creates field of term list for search
	expected format: 
	2 fields per line separated by " — "; Term / Definition
	'''


	def __init__(self, SReadTxtIn):
		'''
		Constructor sends processing to appropriate functions...
		'''
		self.LTTermNDefinition = self.parseStringsTerms(SReadTxtIn)
	
		
		return
	
	def getData(self):
		return self.LTTermNDefinition
	
	def parseStringsTerms(self, SReadTxtIn):
		
		RECPattern = re.compile('^(.+?) — (.+)', re.M)
		LTTermNDefinition = re.findall(RECPattern, SReadTxtIn, re.M)
				
		return LTTermNDefinition
	
	def printData(self, SFNOutput, LColumnNumbers = [0]):
		'''
		print selected column numbers
		'''
		FNOutput = open(SFNOutput, 'w')
		for TColumns in LTTermNDefinition:
			LOut = []
			for el in LColumnNumbers:
				LOut.append(LTTermNDefinition[el])
			SOut = '\t'.join(LOut)
			FNOutput.write(SOut + '\n')
		
		return


	# end clReadTermsFromText class
	
if __name__ == '__main__':
	SReadTxtIn = pathlib.Path(sys.argv[1]).read_text()
	SFNOut = clGenFineNames(sys.argv[1], ['.csv']).getData()[0]
	
	OReadTermsFromText = clReadTermsFromText(SReadTxtIn)
	OReadTermsFromText.printData(SFNOut, [0,1])
	
	
	