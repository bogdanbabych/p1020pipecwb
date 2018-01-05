'''
Created on 18 Dec 2017

@author: bogdan
'''
import sys, os, re
import pathlib
import xml.etree.ElementTree as ET


class clGenerateOutputFileNames(object):
	'''
	service file naming class:
	generates output file names, similar to pathlib function for input file names
	'''

	def __init__(self, SFNameTemplate = './clReadTMXInput.txt', LSuffixes=['out']):
		self.LFileNamesOut = []
		self.genFileNamesOut(SFNameTemplate, LSuffixes) # modifies self.LFileNamesOut
		return
	
	def getData(self):
		return self.LFileNamesOut
	

	def genFileNamesOut(self, SFNameTemplate, LSuffixes):
		'''
		using SFNameTemplate (normally - input file name) as a template for generating a list of output file names
		'''
		SHead, Tail = os.path.split(SFNameTemplate) # splitting directory name from file+extension name
		SRoot, SExtension = os.path.splitext(Tail) # splitting extension from the Tail (file+extension)
		
		self.LFileNamesOut = [ SRoot + '-' + SSuffix + 's01' + SExtension for SSuffix in LSuffixes ]
		SLFileNamesOut = str(self.LFileNamesOut)
		# SRootOut = SRoot + 's01' + SExtension
		# SFileNameOut = os.path.join(SHead, SRootOut)
		
		print ("%(SHead)s %(Tail)s %(SRoot)s %(SExtension)s %(SFileNameOut)s\n" % locals())
		print ("%(SLFileNamesOut)s" % locals())
		return
		

class clReadTMX(object):
	'''
	main class
	readsTMX file / string and outputs one-line per-sentence output 
	'''
	def __init__(self, STmxIn):
		'''
		Constructor
		'''
		print("output from clReadTmx\n", STmxIn)
		return
	
	
	def tmx2tree(self, STmxIn):
		root = ET.fromstring(STmxIn)
		return


if __name__ == '__main__':
	'''
	running script if the module is called from the main
	'''
	STmxIn = pathlib.Path(sys.argv[1]).read_text()
	OGenerateOutputFileNames = clGenerateOutputFileNames(sys.argv[1], ['uk-UA', 'en-GB'])
	OReadTMX = clReadTMX(STmxIn)
	
	pass


