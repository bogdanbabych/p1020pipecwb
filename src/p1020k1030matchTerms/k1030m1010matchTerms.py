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
	
	def countWords(self, STerm):
		LTerm = re.split(' ', STerm)
		ILen = len(LTerm)
		return ILen

	def makeCREfromTerms(self, STermsIn):
		'''
		one term per line format is converted into RE with disjunction
		'''
		LTerms = []  # longer
		# LTerms0 = [] # shorter
		
		LTermsIn = STermsIn.splitlines()
		
		LTermsNLen = [ (STerm, self.countWords(STerm)) for STerm in LTermsIn  ]
		LTermsNLenSorted = sorted(LTermsNLen, key=lambda x: x[1], reverse = True)
		
		print(LTermsNLenSorted)
		
		
		for STerm in STermsIn.splitlines():
			STerm = STerm.rstrip()
			STerm = re.sub('[\(\)]', ' ', STerm)
			
			if STerm == '': continue
			
			STerm = '(?<= )' + STerm + '(?=[ ,:;\?\.!])'
			
			LTerms.append(STerm)
			
		# create RE and compile it
		RETerms = '|'.join(LTerms)
		# print(RETerms)
		CRETerms = re.compile(RETerms, re.I)
		
		return CRETerms
	
	def matchNTagTerms(self, CRETerms, STextIn):
		'''
		task: match, tag, write down into a separate file -- output of the annotation (only those lines where terms were matched)
		'''
		for SLine in STextIn.splitlines():
			SLine = SLine.rstrip()
			LSFields = re.split('\t', SLine)
			try:
				SSource = LSFields[0]
				STarget = LSFields[1]
				
				SSource = ' ' + SSource + ' '
				
			except:
				SSource = ''
				STarget = ''
				continue
			
			if re.search(CRETerms, SSource):
				# re.sub(CRETerms, <term>\0</term>, STextIn)
				i = 0
				for match in re.finditer(CRETerms, SSource):
					i += 1
					iLong = 100 + i
					SLong = str(iLong)
					# SMatch = match.group(0)
					SSource = re.sub('(?<= )' + match.group(0) + '(?=[ ,:;\?\.!])', '<term id=%s>\g<0></term>' % SLong, SSource)
					print(match.group(0))
					# print(SMatch)
				print(SSource + '\t', STarget)
				print('')
					

# end clMatchTerms class
	
	
	
	

if __name__ == '__main__':
	STermsIn = pathlib.Path(sys.argv[1]).read_text()
	STextIn = pathlib.Path(sys.argv[2]).read_text()

	SFNOut = m8510GenFileNames.clGenFineNames(sys.argv[1], ['-terms.txt']).getData()[0]

	# print(SFNOut)
	OMatchTerms = clMatchTerms(STermsIn, STextIn)



