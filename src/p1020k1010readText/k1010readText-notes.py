'''
Created on 9 Jan 2018

@author: bogdan
'''
class MyClassExamples(object):
	'''
	removed code -- examples
	'''


	def __init__(self, params):
		'''
		Constructor
		'''

# [experiments]
	# [experiments with the root object] >> placeholder in py file, removed from there
	# [py code]
		print(root.tag)
		print(root.attrib)
		for child in root:
			print(child.tag, child.attrib)
		
		for tuv in root.iter('tuv'):
			print(tuv.attrib)
			
	# [experiments with computing the file name suffixes for all the objects in the file --> not necessary any more; this will be computed in runtime for each segment]
	# [if a segment already exists, another identifier will be generated... ]
	# [docs: url: https://docs.python.org/3.6/library/xml.etree.elementtree.html#elementtree-xpath ]
	# [py code]
	
		'''
		finding language identifiers in the file
		list comprehension: forming a list of key-value pairs with langauge IDs (for naming files / aligned indices)
		how it works : it is computed left to right; (key, val) become element of the list; root.iter('tuv') iterates over tuv tags that have lang id, 
		tuv.attrib.items() converts attribute=value dictionary into a tuple (key, value) in each of the cases where 'tuv' tag is processed
		list comprehensions are best explained in: http://www.secnetix.de/olli/Python/list_comprehensions.hawk & https://stackoverflow.com/questions/9138112/looping-over-a-list-in-python
		'''
		# is this necessary? we need only a suffix for each segment, which can be determined in run-time, not pre-computed in advance ... 
		LTuv = [ (key, val) for tuv in root.iter('tuv') for (key, val) in tuv.attrib.items() ]
		# LTuv = [ tuv.attrib.items() for tuv in root.iter('tuv')]
		
		SetTuv = set(LTuv)
		LTuvUniq = list(SetTuv)
		
		# key-value pairs (attribute=val) are unique, but langIDs are not guaranteed to be unique; so we generate numeric IDs automatically, since keys cannot be in file names (contain / :, etc.)
		i = 0
		LSuffixes = []
		for key, val in LTuvUniq:
			sID = str(10 + i); i +=1
			LSuffixes.append(sID + '-' + val)
		return LSuffixes
		print(str(LTuvUniq))

		return LTuvUniq

	# [experiments with findall, ElementTree.tostring function, etc.]
		for xmlTU in root.iter('tu'):
			# print(xmlTU.attrib)
			# print(xmlTU.text)
			for xmlTUV in xmlTU.findall('tuv'):
				# if len(xmlTUV.findall('seg')) > 1: 
				print('\t:segs=', str(len(xmlTUV.findall('seg'))))
				for xmlSeg in xmlTUV.findall('seg'):
					# if len(xmlSegs) > 1:
					print('SEG:', ElementTree.tostring(xmlSeg, encoding='unicode', method='xml'))
				# testing with print 
				
				print('\t', xmlTUV.attrib)
				# str1 = ElementTree.tostring(xmlTUV, encoding='unicode', method='xml')
				# print(str1)
				# for el in xmlTUV.itertext():
				# 	print('\t\tITERTEXT', str(el))
					
				# print(xmlTUV.text, '\n')
				pass

		print('in trees2seg:')
		print(str(root), '\n')
				

# end: examples




		
class MyClassOther(object):
	'''
	removed code -- other code
	'''


	def __init__(self, params):
		'''
		Constructor
		'''


# [removed code which is not examples]

# /2018/01/08


# removed from: class for generating file names:
class clGenerateOutput(object):
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

	def genLangIDSuffixes(self, LTuvUniq):
		# key-value pairs (attribute=val) are unique, but langIDs are not guaranteed to be unique; so we generate numeric IDs automatically, since keys cannot be in file names (contain / :, etc.)
		i = 0
		LSuffixes = []
		for key, val in LTuvUniq:
			i +=1; sID = str(10 + i)
			LSuffixes.append(sID + '-' + val)
		return LSuffixes
	

	def genFileNamesOut(self, SFNameTemplate = './clReadTMXInput.txt', LSuffixes=[''], IStageNumber = 0):
		'''
		using SFNameTemplate (normally - input file name) as a template for generating a list of output file names
		'''
		SHead, Tail = os.path.split(SFNameTemplate) # splitting directory name from file+extension name
		SRoot, SExtension = os.path.splitext(Tail) # splitting extension from the Tail (file+extension)
		
		self.LFileNamesOut = [ SRoot + '-' + SSuffix + '-' + str(100 + IStageNumber) + SExtension for SSuffix in LSuffixes ]
		SLFileNamesOut = str(self.LFileNamesOut)
		# SRootOut = SRoot + 's01' + SExtension
		# SFileNameOut = os.path.join(SHead, SRootOut)
		
		# print ("%(SHead)s %(Tail)s %(SRoot)s %(SExtension)s\n" % locals())
		print ("%(SLFileNamesOut)s" % locals())
		return self.LFileNamesOut # to change :: pair with langID -- to know which language where to write...
	

# removed from :
if __name__ == '__main__':
	# [py code]
	LLangAttr = OReadTMX.findLangIDs(OReadTMX.root) # attribute / value pairs in a list for all languages creates a list of xml:lang='EN-UK'
	
	# initialise the FileName generator object
	OGenerateOutputFileNames = clGenerateOutputFileNames()
	# generate list of LangIDs from attribute / value pairs
	LSuffixes = OGenerateOutputFileNames.genLangIDSuffixes(LLangAttr)
	# generate OutputFilenames given the list of lang ids and system argv[1] :: TODO :: to change -- pair : lang ID + file name! to know which language to write where!
	# LFileNameOutNLangID = OGenerateOutputFileNames.genFileNamesOut(SFNameTemplate, LSuffixes, IStageNumber)
	LFileNameOutNLangID = OGenerateOutputFileNames.genFileNamesOut(sys.argv[1], LSuffixes, 1)
	
	# OGenerateOutputFileNames = clGenerateOutputFileNames(sys.argv[1], ['uk-UA', 'en-GB'], 1)
	# OGenerateOutputFileNames = clGenerateOutputFileNames(sys.argv[1], LLangIDs, 1)
	
	
	pass


# 		// todo: old tuple not necessary; hide this; as we go, simply record occurrences of tags, convert them into LangID0-CountryID0-SeqNumber0 format




	'''			
	STerm1 = '(?<= )' + STerm + '(?=[ ,:;\?\.!])'
	STerm2 = '^' + STerm + '(?=[ ,:;\?!])'
	STerm3 = '(?<= )' + STerm + '$'
	STerm4 = '^' + STerm + '$'

	STerm1 = ' ' + STerm + '[ ,:;\?!]'
	STerm2 = '^' + STerm + '[ ,:;\?!]'
	STerm3 = ' ' + STerm + '$'
	STerm4 = '^' + STerm + '$'

	LTerms.append(STerm1)
	LTerms.append(STerm2)
	LTerms.append(STerm3)
	LTerms.append(STerm4)
	'''






		