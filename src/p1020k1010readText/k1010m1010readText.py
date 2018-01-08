'''
Created on 18 Dec 2017

@author: bogdan
'''
import sys, os, re
import pathlib
import xml.etree.ElementTree as ET
from et_xmlfile.tests.common_imports import ElementTree


class clReadTMX(object):
	'''
	main class
	readsTMX file / string and outputs one-line per-sentence output 
	'''
	def __init__(self, STmxIn):
		'''
		Generate root of the xml > tmx tree; identify segments, prepare a list of dictionaries {langID : segment} as output
		'''
		self.root = self.tmx2tree(STmxIn)
		self.LDSegs = self.tree2segs(self.root) # temporary placeholder --> function to be implemented
		return
				
	def tmx2tree(self, STmxIn):
		root = ET.fromstring(STmxIn)
		# print(str(root), '\n')
		# [experiments] with the root object can go here <<
		return root
	
	def tree2segs (self, root):
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
					DSegs[SLangID] =  xSEG
			LDSegs.append(DSegs)
		
		print(str(LDSegs))
		return LDSegs


if __name__ == '__main__':
	'''
	running script if the module is called from the main
	'''
	STmxIn = pathlib.Path(sys.argv[1]).read_text()
	OReadTMX = clReadTMX(STmxIn)
	# end __main__


