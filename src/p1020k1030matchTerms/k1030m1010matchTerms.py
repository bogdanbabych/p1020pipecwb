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
		self.LTSegsNTerms = self.matchNTagTerms(CRETerms, STextIn)
		return 
	
	def getData(self):
		return self.LTSegsNTerms
	
	
	def printData(self, SFOutput):
		FOutput = open(SFOutput, 'w')
		for (SSource, STarget, SSourceTag, STargetTag, LTTerms) in self.LTSegsNTerms:
			FOutput.write(SSourceTag + '\t' + STargetTag + '\n')
			for (STerm, LTermEquivalents) in LTTerms:
				FOutput.write('\t' + STerm + '\t' + str(LTermEquivalents) + '\n')
			
			
	
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
		
		# print(LTermsNLenSorted)
		
		# longest match first... 
		# for STerm in STermsIn.splitlines():
		for STerm, ILen in LTermsNLenSorted:
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
		the function is called to process all segments of the translation memory
		'''
		# data structure for variable handling
		LTSegsNTerms = [] # list of tuples: segments and terms: [ ( SSource, STarget, SSourceTagged, STargetTagged, LTTermsNTheirTranslCandidates ) ]
		
		
		LMatchedTerms = [] # now used for counting 
		ICountMatchSen = 0
		for SLine in STextIn.splitlines():
			# TSegsNTerms = ()
			# LTTerms = terms which are used in this specific SLine (translation unit, or segment):
			LTTerms = [] # list of tuples: [ (Term, [ (TransCandidate, Score), ... ] ), (Term, [ ...
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
			
			SSourceOri = SSource # saving a copy
			STargetOri = STarget
			if re.search(CRETerms, SSource):
				ICountMatchSen += 1
				# re.sub(CRETerms, <term>\0</term>, STextIn)
				i = 0
				for match in re.finditer(CRETerms, SSource):
					i += 1
					if i % 1000 == 0: sys.stderr.write(str(i) + '\n')
					iLong = 100 + i
					SLong = str(iLong)
					# SMatch = match.group(0)
					SSource = re.sub('(?<= )' + match.group(0) + '(?=[ ,:;\?\.!])', '<term id=%s>\g<0></term>' % SLong, SSource)
					# updating the list of terms Translations are now represented by an empty list
					LTTerms.append(( match.group(0), [] ))
					print(match.group(0))
					LMatchedTerms.append(match.group(0))
					# print(SMatch)
				print(str(ICountMatchSen) + '\t' + SSource + '\t', STarget)
				print('')
			# updating the main data structure: tuple for one translation unit / segment
			TSegsNTerms = (SSourceOri, STargetOri, SSource, STarget, LTTerms)
			LTSegsNTerms.append( TSegsNTerms )
		ILenMatchedTerms = len(LMatchedTerms)
		ILenMatchedUnique = len(set(LMatchedTerms))
		# this is printing to debug; proper handling of the output in a variable
		print('Terms:' + str(ILenMatchedTerms) + '\tUnique:' + str(ILenMatchedUnique))
		print(set(LMatchedTerms))
		
		return LTSegsNTerms
		
					

# end clMatchTerms class
	
	
	
	

if __name__ == '__main__':
	STermsIn = pathlib.Path(sys.argv[1]).read_text()
	STextIn = pathlib.Path(sys.argv[2]).read_text()

	SFNOut = m8510GenFileNames.clGenFineNames(sys.argv[1], ['-terms.txt']).getData()[0]

	# print(SFNOut)
	OMatchTerms = clMatchTerms(STermsIn, STextIn)
	LTSegsNTerms = OMatchTerms.getData()
	OMatchTerms.printData(SFNOut)



