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


	def __init__(self, STermsIn, STextIn):
		'''
		matches RE of joined terms with the text string copied from TMX
		'''
		CRETerms = self.makeCREfromTerms(STermsIn)
		self.matchNTagTerms(CRETerms, STextIn)
		
		
		
		return 

	def makeCREfromTerms(self, STermsIn):
		'''
		one term per line format is converted into RE with disjunction
		'''
		LTerms = []
		for STerm in STermsIn.splitlines():
			STerm = STerm.rstrip()
			STerm = re.sub('[\(\)]', ' ', STerm)
			
			if STerm == '': continue
			LTerms.append(STerm)
			
		# create RE and compile it
		RETerms = '|'.join(LTerms)
		print(RETerms)
		CRETerms = re.compile(RETerms, re.I)
		
		return CRETerms
	
	def matchNTagTerms(self, CRETerms, STextIn):
		'''
		task: match, tag, write down into a separate file -- output of the annotation (only those lines where terms were matched)
		'''
		for SLine in STextIn:
			LSFields = re.split('\t', SLine)
			try:
				SSource = LSFields[0]
				STarget = LSFields[1]
			except:
				continue
			if re.search(CRETerms, SSource):
				# re.sub(CRETerms, <term>\0</term>, STextIn)
				for match in re.finditer(CRETerms, SSource):
					SSource = re.sub(match.group(0), '<term>\g<0></term>', SSource)
					# print(match.group(0))
				# print(SSource + '\t', STarget)
					
				
				
		
	

# end clMatchTerms class
	
	
	
	

if __name__ == '__main__':
	STextIn = pathlib.Path(sys.argv[1]).read_text()
	STermsIn = pathlib.Path(sys.argv[2]).read_text()
	SFNOut = m8510GenFileNames.clGenFineNames(sys.argv[1], ['-terms.txt']).getData()[0]

	# print(SFNOut)
	OMatchTerms = clMatchTerms(STermsIn, STextIn)



