'''
Created on 18 Dec 2017

@author: bogdan

tmx file transformed into :
	gizapp format;
	tag-seg xml format
	tab separated HunAlign format (possible to shift around, etc. in a spreadsheet)

'''
import sys, os, re
import pathlib
import xml.etree.ElementTree as ET
from et_xmlfile.tests.common_imports import ElementTree


class clGenerateOutput(object):
	'''
	printing outputs
	'''
	def __init__(self, SFNTemplate, LDSDataSegs, LSTypesOut=['gizapp.txt']):
		'''
		constructor. Allowed LSTypesOut=['gizapp.txt', 'tseg.txt']
		'''
		self.printSegs(SFNTemplate, LDSDataSegs, LSTypesOut)
		return

	def printSegs(self, SFNTemplate, LDSDataSegs, LSTypesOut):
		ICountSegs = 1000000
		# hunalign filename:
		if 'hunalign.txt' in LSTypesOut: 
			SFNameOutHun = SFNTemplate + '-' + '-' + 'hunalign.txt'
			FNameOutHun = open(SFNameOutHun, 'w')
		# for each aligned pair/tuple of segments:
		for DSSeg in LDSDataSegs:
			ICountSegs +=1
			if ICountSegs % 3000 == 0: sys.stderr.write(str(ICountSegs) + '\n')
			# for each language string in an aligned segment pair / tuple:
			for SLangID, SSeg in sorted(DSSeg.items()):
				# fOut = pathlib.Path(SFNameOut)
				SSeg = re.sub('\n', ' ', SSeg, flags=re.IGNORECASE|re.DOTALL|re.MULTILINE)
				# removing <seg/> tags:
				if re.match('<seg>.+</seg>', SSeg, re.IGNORECASE|re.DOTALL|re.MULTILINE):
					mSeg = re.match('<seg>(.+)</seg>', SSeg, re.IGNORECASE|re.DOTALL|re.MULTILINE)
					SSegBetweenTags = mSeg.group(1)
				else:
					SSegBetweenTags = SSeg
				# printing required output format
				# special treatment for Hunalign output format:
				if 'hunalign.txt' in LSTypesOut:
					FNameOutHun.write(SSegBetweenTags + '\t')
				for STypeOut in LSTypesOut:
					SFNameOut = SFNTemplate + '-' + SLangID + '-' + STypeOut
					fOut = open(SFNameOut, 'a')
					# different output formats are printed here
					if STypeOut == 'hunalign.txt': continue # we deal with this one level up
					if STypeOut == 'gizapp.txt':
						# fOut.write(str(ICountSegs) + '\t\t\t' + SSegBetweenTags + '\n')
						fOut.write(SSegBetweenTags + '\n')						
						
					if STypeOut == 'tseg.txt':
						# fOut.write(str(ICountSegs) + '\t\t\t' + SSeg + '\n')
						fOut.write('<seg id="' + str(ICountSegs) + '">\n' + SSegBetweenTags + '\n</seg>\n\n')
			# closing each Hunalign line with a newline character
			if 'hunalign.txt' in LSTypesOut:
				FNameOutHun.write('1\n' ) # alignment probability = 1 (since comes from manually aligned data), newline character for each line
					
		return
	
class clReadTMX(object):
	'''
	main class
	readsTMX file / string and outputs one-line per-sentence output 
	'''
	def __init__(self, STmxIn, BRemoveTags=True):
		'''
		Generate root of the xml > tmx tree; identify segments, prepare a list of dictionaries {langID : segment} as output
		todo: to add -- if removeTags=True --> then remove tags itertext function; tags only obscure output --> for corpus processing ?
			unnecessary in case there is already linguistic annotation
		'''
		self.root = self.tmx2tree(STmxIn)
		self.LDSegs = self.tree2segs(self.root, BRemoveTags)
		return
	
	def getData(self):
		return self.LDSegs
				
	def tmx2tree(self, STmxIn):
		root = ET.fromstring(STmxIn)
		# [experiments] with the root object can go here <<
		return root
	
	def tree2segs (self, root, BRemoveTags):
		'''
		main processing routine: generate an LD{langID:Seg} representation which can be then printed
		documentation : https://docs.python.org/3.6/library/xml.etree.elementtree.html#elementtree-xpath
		problem resolved with tostring method: https://stackoverflow.com/questions/15304229/convert-python-elementtree-to-string
		'''
		LDSegs = []
		for xTU in root.iter('tu'):
			DSegs = {}
			for xTUV in xTU.findall('tuv'):
				for SLangID in sorted( xTUV.attrib.values() ): # normally only one attribute-value pair occurs
					xSEG = xTUV.find('seg')
					if BRemoveTags == True:
						SSeg = ''
						for el in xSEG.itertext():
							SSeg += el
					else:
						SSeg = ElementTree.tostring(xSEG, encoding='unicode', method='xml')
					DSegs[SLangID] =  SSeg
			LDSegs.append(DSegs)
		# print(str(LDSegs))
		return LDSegs


if __name__ == '__main__':
	'''
	running script if the module is called from the main;
	- you can adjust parameters here, e.g.: BRemoveTags=False, etc., no command line parameters are used
	'''
	STmxIn = pathlib.Path(sys.argv[1]).read_text()
	LDSegs = clReadTMX(STmxIn, BRemoveTags=True).getData()
	OGenerateOutput = clGenerateOutput(sys.argv[1], LDSegs, ['gizapp.txt', 'tseg.txt', 'hunalign.txt'])
	# end __main__


