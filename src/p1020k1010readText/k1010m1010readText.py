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
		'''
		LDSegs = []
		print('in trees2seg:')
		print(str(root), '\n')
		for xmlTU in root.iter('tu'):
			print(xmlTU.attrib)
			# print(xmlTU.text)
			for xmlTUV in xmlTU.findall('tuv'):
				# testing with print 
				print('\t', xmlTUV.attrib)
				str1 = ElementTree.tostring(xmlTUV, method='xml')
				print(str1)
				# for el in xmlTUV.itertext():
				# 	print('\t\tITERTEXT', str(el))
					
				# print(xmlTUV.text, '\n')
				pass
				
		return LDSegs


if __name__ == '__main__':
	'''
	running script if the module is called from the main
	'''
	STmxIn = pathlib.Path(sys.argv[1]).read_text()
	OReadTMX = clReadTMX(STmxIn)
	# end __main__


