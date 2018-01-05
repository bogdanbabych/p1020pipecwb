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

	def __init__(self):
		self.LFileNamesOut = []
		# self.genFileNamesOut(SFNameTemplate, LSuffixes, IStageNumber) # modifies self.LFileNamesOut
		return
	
	def getData(self):
		return self.LFileNamesOut
	

	def genFileNamesOut(self, SFNameTemplate = './clReadTMXInput.txt', LSuffixes=[''], IStageNumber = 0):
		'''
		using SFNameTemplate (normally - input file name) as a template for generating a list of output file names
		'''
		SHead, Tail = os.path.split(SFNameTemplate) # splitting directory name from file+extension name
		SRoot, SExtension = os.path.splitext(Tail) # splitting extension from the Tail (file+extension)
		
		self.LFileNamesOut = [ SRoot + '-' + SSuffix + str(100 + IStageNumber) + SExtension for SSuffix in LSuffixes ]
		SLFileNamesOut = str(self.LFileNamesOut)
		# SRootOut = SRoot + 's01' + SExtension
		# SFileNameOut = os.path.join(SHead, SRootOut)
		
		# print ("%(SHead)s %(Tail)s %(SRoot)s %(SExtension)s\n" % locals())
		print ("%(SLFileNamesOut)s" % locals())
		return LFileNamesOut # to change :: pair with langID -- to know which language where to write...
	
	def genLangIDSuffixes(self, LTuvUniq):
		# key-value pairs (attribute=val) are unique, but langIDs are not guaranteed to be unique; so we generate numeric IDs automatically, since keys cannot be in file names (contain / :, etc.)
		id = 0
		LSuffixes = []
		for key, val in LTuvUniq:
			id +=1; sID = str(10 + id)
			LSuffixes.append(sID + '-' + val)

		

class clReadTMX(object):
	'''
	main class
	readsTMX file / string and outputs one-line per-sentence output 
	'''
	def __init__(self, STmxIn):
		'''
		Constructor
		'''
		# print("output from clReadTmx\n", STmxIn)
		self.root = self.tmx2tree(STmxIn)
		return
				
	def tmx2tree(self, STmxIn):
		root = ET.fromstring(STmxIn)
		
		'''
		# experiments with the root object:
		
		print(root.tag)
		print(root.attrib)
		for child in root:
			print(child.tag, child.attrib)
		
		for tuv in root.iter('tuv'):
			print(tuv.attrib)
		'''
		
		return root
	
	def findLangIDs(self, root):
		LTuvUniq = []
		'''
		finding language identifiers in the file
		list comprehension: forming a list of key-value pairs with langauge IDs (for naming files / aligned indices)
		how it works : it is computed left to right; (key, val) become element of the list; root.iter('tuv') iterates over tuv tags that have lang id, 
		tuv.attrib.items() converts attribute=value dictionary into a tuple (key, value) in each of the cases where 'tuv' tag is processed
		list comprehensions are best explained in: http://www.secnetix.de/olli/Python/list_comprehensions.hawk & https://stackoverflow.com/questions/9138112/looping-over-a-list-in-python
		'''
		LTuv = [ (key, val) for tuv in root.iter('tuv') for (key, val) in tuv.attrib.items() ]
		# LTuv = [ tuv.attrib.items() for tuv in root.iter('tuv')]
		
		SetTuv = set(LTuv)
		LTuvUniq = list(SetTuv)
		print(str(LTuvUniq))

		
		return LTuvUniq


if __name__ == '__main__':
	'''
	running script if the module is called from the main
	'''
	STmxIn = pathlib.Path(sys.argv[1]).read_text()
	OReadTMX = clReadTMX(STmxIn)
	LLangAttr = OReadTMX.findLangIDs(OReadTMX.root) # attribute / value pairs in a list for all languages
	
	# initialise the FileName generator object
	OGenerateOutputFileNames = clGenerateOutputFileNames()
	# generate list of LangIDs from attribute / value pairs
	LLangIDs = OGenerateOutputFileNames.genLangIDSuffixes(LLangAttr)
	# generate OutputFilenames given the list of lang ids and system argv[1] :: TODO :: to change -- pair : lang ID + file name! to know which language to write where!
	# LFileNameOutNLangID = OGenerateOutputFileNames.genFileNamesOut(SFNameTemplate, LSuffixes, IStageNumber)
	LFileNameOutNLangID = OGenerateOutputFileNames.genFileNamesOut(sys.argv[1], LLangIDs, 1)
	
	# OGenerateOutputFileNames = clGenerateOutputFileNames(sys.argv[1], ['uk-UA', 'en-GB'], 1)
	# OGenerateOutputFileNames = clGenerateOutputFileNames(sys.argv[1], LLangIDs, 1)
	
	
	pass


