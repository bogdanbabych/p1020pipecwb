'''
Created on 26 Mar 2018

@author: bogdan
'''

import sys, os, re
import pathlib
import m8510GenFileNames



class clMatchTerms(object):
	'''
	matching terms in strings generated from tmx - e.g., in hunalign output files
	'''


	def __init__(self, STxtIn, RETermsIn):
		'''
		matches RE of joined terms with the text string copied from TMX
		'''
		return 
	
	

	# end clMatchTerms class

if __name__ == '__main__':
	SReadTxtIn = pathlib.Path(sys.argv[1]).read_text()
	SFNOut = m8510GenFileNames.clGenFineNames(sys.argv[1], ['.csv']).getData()[0]

	print SFNOut