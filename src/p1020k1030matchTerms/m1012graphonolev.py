'''
Created on 2 Apr 2018

@author: bogdan
based on md060graphonoLev.py + md060graphonoLevV09.py
core improvements: 
- introduction of a transliteration table
- changing the order or returned arguments (first four, to be more consistent with the rest (normalised version always follows the raw version)
- use different tables of feature sets, returning as an argument from the core class -- feature sets are variables now

No optimization for speed yet...

Original 
Created on 25 Mar 2016

@author: bogdan
python3 required for operation -- due to Unicode issues
v09: returning different insertion costs for graphonological distance
'''

import sys, re, os
import copy
# from p010graphems.levenshtein import levenshtein
from collections import defaultdict
from collections import Counter




class clGraphonolev(object):
	'''
	class  computes Levenshtein distance for graphonological representations
	the purpose is to plug the module into external programmes to compute modified variants of Lev edit distance
	'''


	def __init__(self, Debug = False, DebugFile = 'md060graphonolev-debug.txt', DebugMode = 'a', SFeatueTable = 'md060graphonoLev-phonetic-features.tsv'):
		'''
		Constructor
		'''
		# self.DFeatures = {}
		self.readFeat(SFeatueTable)
		self.BDebug = False
		if Debug == True:
			self.BDebug = True
			self.FDebug = open(DebugFile, DebugMode)

		
	def readFeat(self, SFeatueTable):
		'''
		reading a table of phonological features for each letter, only needed for feature-based levenstein distance calculations
		'''
		self.DGraphemes = defaultdict(list) # the main dictionary of the project: mapping: grapheme, language --> feature sets		
		FFeatures = open(SFeatueTable, 'rU')
		for SLine in FFeatures:
			if re.match('#', SLine):
				continue
			SLine = SLine.rstrip()
			LLine = re.split('\t', SLine)
			SGrapheme = LLine[0]
			SLanguage = LLine[1]
			LFeatures = LLine[2:]
			
			LLanguages = re.split(';', SLanguage)
			
			# main representation mapping: create entries for all respective languages
			for lang in LLanguages:
				self.DGraphemes[(lang, SGrapheme)] = LFeatures
				
				# debugging, can be removed...
				'''
				FDebug.write('%(lang)s, %(SGrapheme)s, \n' % locals())
				for el in LFeatures:
					FDebug.write('\t%(el)s\n' % locals())
				'''	
		
	def str2Features(self, SWord, SLangID):
		LGraphFeat = [] # list of tuples: character + list - for each character in the word we get feature list
		LWordChars = list(SWord)
		for ch in LWordChars:
			# FDebug.write('%(SLangID)s, %(ch)s\t' % locals())
			try:
				LFeatures = self.DGraphemes[(SLangID, ch)]
				LGraphFeat.append((ch, LFeatures)) # data structure for LGraphFeat - list of graphemic features
				# FDebug.write('features: %(LFeatures)s\n' % locals())
			except:
				# FDebug.write('no features found\n')
				sys.stderr.write('no features found\n')
				
		
		return LGraphFeat # return list of lists


	def compareGraphFeat(self, LGraphFeatA, LGraphFeatB):
		# works for pairs of characters (their feature lists).
		# Prec, Rec, FMeasure = (0, 0, 0)
		# IOverlap = 0
		ILenA = len(LGraphFeatA)
		ILenB = len(LGraphFeatB)

		a_multiset = Counter(LGraphFeatA)
		b_multiset = Counter(LGraphFeatB)

		overlap = list((a_multiset & b_multiset).elements())
		IOverlap = len(overlap)
		# a_remainder = list((a_multiset - b_multiset).elements())
		# b_remainder = list((b_multiset - a_multiset).elements())		

		# Precision of List A:
		try:
			Prec = IOverlap / ILenA
			Rec = IOverlap / ILenB
			FMeasure = (2 * Prec * Rec) / (Prec + Rec)
		except:
			Prec, Rec, FMeasure = (0, 0, 0)
		
		return FMeasure


	def computeLevenshtein(self, SW1, SW2, SLangID1, SLangID2):
		''' 
		converts character string to two lists of two two tuples : (character , phonological feature list)
		'''
		s1 = self.str2Features(SW1, SLangID1)
		s2 = self.str2Features(SW2, SLangID2)
		l1 = len(s1)
		l2 = len(s2)
		# lAve = (l1 + l2) / 2 # maximum for edit distance ?
		lAve = max(l1, l2)
		lAveFeats1 = 0 # number of features in each word
		lAveFeats2 = 0
		
		for (ch, el) in s1:
			if self.BDebug == True:
				SEl = str(el)
				self.FDebug.write('%(ch)s\t%(SEl)s\n' % locals())
			lAveFeats1 += len(el)
		for (ch, el) in s2:
			if self.BDebug == True:
				SEl = str(el)
				self.FDebug.write('%(ch)s\t%(SEl)s\n' % locals())
			lAveFeats2 += len(el)
		lAveFeats = (lAveFeats1 + lAveFeats2) / 2 # average number of features per two words


	
		matrix = [list(range(l1 + 1))] * (l2 + 1)
		matrixI2 = copy.deepcopy(matrix)
		matrixI4 = copy.deepcopy(matrix)
		matrixI6 = copy.deepcopy(matrix)
		matrixI8 = copy.deepcopy(matrix)
		# different insertion costs
		matrix0 = copy.deepcopy(matrix)
		for zz in range(l2 + 1):
			matrix[zz] = list(range(zz,zz + l1 + 1))
			matrixI2[zz] = copy.deepcopy(matrix[zz])
			matrixI4[zz] = copy.deepcopy(matrix[zz])
			matrixI6[zz] = copy.deepcopy(matrix[zz])
			matrixI8[zz] = copy.deepcopy(matrix[zz])
			
			matrix0[zz] = copy.deepcopy(matrix[zz])
		for zz in range(0,l2):
			for sz in range(0,l1):
				# here: 1. compare sets of features; add the minimal substitution score here...
				# calculate P, R, F-measure of the feature sets for each symbol, report F-measure:
				# print(str(s1[sz]) + '\t' + str(s2[zz]))
				(ch1, LFeat1) = s1[sz]
				(ch2, LFeat2) = s2[zz]
				# FMeasure = self.compareGraphFeat(s1[sz], s2[zz])
				FMeasure = self.compareGraphFeat(LFeat1, LFeat2)
				OneMinusFMeasure = 1 - FMeasure
				# print('FMeasure ' + str(FMeasure))
				# if F-Measure = 1 then feature vectors are identical; we need to subtract it from 1 (at the end):
				# matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
				
				# Main work is here: # experimental question: 
				matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + OneMinusFMeasure)
				matrixI2[zz+1][sz+1] = min(matrixI2[zz+1][sz] + 0.2, matrixI2[zz][sz+1] + 0.2, matrixI2[zz][sz] + OneMinusFMeasure)
				matrixI4[zz+1][sz+1] = min(matrixI4[zz+1][sz] + 0.4, matrixI4[zz][sz+1] + 0.4, matrixI4[zz][sz] + OneMinusFMeasure)
				matrixI6[zz+1][sz+1] = min(matrixI6[zz+1][sz] + 0.6, matrixI6[zz][sz+1] + 0.6, matrixI6[zz][sz] + OneMinusFMeasure)
				matrixI8[zz+1][sz+1] = min(matrixI8[zz+1][sz] + 0.8, matrixI8[zz][sz+1] + 0.8, matrixI8[zz][sz] + OneMinusFMeasure)
				# matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 0.4, matrix[zz][sz+1] + 0.4, matrix[zz][sz] + OneMinusFMeasure)
				# insertion cost adjustment -- revert to 1 or lowering to 0.4 ?

				# now classical levenshtein distance
				# if s1[sz] == s2[zz]:
				if ch1 == ch2:
					matrix0[zz+1][sz+1] = min(matrix0[zz+1][sz] + 1, matrix0[zz][sz+1] + 1, matrix0[zz][sz])
				else:
					matrix0[zz+1][sz+1] = min(matrix0[zz+1][sz] + 1, matrix0[zz][sz+1] + 1, matrix0[zz][sz] + 1)
				
		# print("That's the Levenshtein-Matrix:")
		# self.printMatrix(matrix)
		Levenshtein0 = matrix0[l2][l1] # classical Levenshtein distance
		Levenshtein1 =  matrix[l2][l1]
		LevenshteinI2 =  matrixI2[l2][l1]
		LevenshteinI4 =  matrixI4[l2][l1]
		LevenshteinI6 =  matrixI6[l2][l1]
		LevenshteinI8 =  matrixI8[l2][l1]
		
		# debug:
		if self.BDebug == True:
			self.printMatrix(matrix0)
			self.printMatrix(matrix)
		
		try:
			Levenshtein0Norm = Levenshtein0 / lAve
		except:
			Levenshtein0Norm = 1
		try:
			# Levenshtein1Norm = Levenshtein1 / lAveFeats
			Levenshtein1Norm = Levenshtein1 / lAve
			LevenshteinI2Norm = LevenshteinI2 / lAve
			LevenshteinI4Norm = LevenshteinI4 / lAve
			LevenshteinI6Norm = LevenshteinI6 / lAve
			LevenshteinI8Norm = LevenshteinI8 / lAve
			
		except:
			Levenshtein1Norm = 1
			LevenshteinI2Norm = 1
			LevenshteinI4Norm = 1
			LevenshteinI6Norm = 1
			LevenshteinI8Norm = 1

			# sys.stderr.write('%(SW1)s, %(SW2)s, \n\t%(s1)s\n\t%(s2)s\n\t%(Levenshtein1).3f\n\t%(lAveFeats)\n\n' % locals())
			try:
				sys.stderr.write('%(SW1)s\n' % locals())
			except:
				sys.stderr.write('cannot write\n')
			try:
				sys.stderr.write('%(SW2)s\n' % locals())
			except:
				sys.stderr.write('cannot write\n')
			try:
				sys.stderr.write('%(s1)s\n' % locals())
			except:
				sys.stderr.write('cannot write s1\n')
			try:
				sys.stderr.write('%(s2)s\n' % locals())
			except:
				sys.stderr.write('cannot write s2\n')

		
		# return (Levenshtein0, Levenshtein1, Levenshtein0Norm, Levenshtein1Norm)
		return (Levenshtein0, Levenshtein1, Levenshtein0Norm, Levenshtein1Norm, LevenshteinI2, LevenshteinI2Norm, LevenshteinI4, LevenshteinI4Norm, LevenshteinI6, LevenshteinI6Norm, LevenshteinI8, LevenshteinI8Norm)


	def printMatrix(self, m):
		self.FDebug.write(' \n')
		for line in m:
			spTupel = ()
			breite = len(line)
			for column in line:
				spTupel = spTupel + (column, )
			self.FDebug.write(" %3.1f "*breite % spTupel)
			self.FDebug.write('\n')


# using the class: initialising and computing Lev distances
if __name__ == '__main__':
	for el in sys.argv:
		sys.stderr.write(el + '\n')

	FInput = open(sys.argv[1], 'rU')
	SLangID1 = sys.argv[2]
	SLangID2 = sys.argv[3]
	SDebug = sys.argv[4]
	STransliterationTable = sys.argv[5]
	SFeatureTables = sys.argv[6]
	LFeatureTables = re.split(',', SFeatureTables)
	# list of features tables files
	
	if SDebug == 'Debug':
		BDebug = True
	else:
		BDebug = False
		
	# for testing purposes: argv: use comma for joining file names, not ; --> does not work correctly
	# print(FInput, SLangID1, SLangID2, SDebug, STransliterationTable, SFeatureTables)
		
		
	
	
	OGraphonolev = clGraphonolev(BDebug, SFeatueTable = LFeatureTables[0])
	# OGraphonolev.readFeat()
	for SLine in FInput:
		SLine = SLine.rstrip()
		try:
			(SW1, SW2) = re.split('\t', SLine, 1)
		except:
			SW1 = '' ; SW2 = ''
		# FDebug.write('SW1 = %(SW1)s; SLangID1 = %(SLangID1)s\n' % locals())
		# LGraphFeat1 = OGraphonolev.str2Features(SW1, SLangID1)
		# FDebug.write('SW2 = %(SW2)s; SLangID2 = %(SLangID2)s\n' % locals())
		# LGraphFeat2 = OGraphonolev.str2Features(SW2, SLangID2)
		(Lev0, Lev1, Lev0Norm, Lev1Norm, LevenshteinI2, LevenshteinI2Norm, LevenshteinI4, LevenshteinI4Norm, LevenshteinI6, LevenshteinI6Norm, LevenshteinI8, LevenshteinI8Norm) = OGraphonolev.computeLevenshtein(SW1, SW2, SLangID1, SLangID2)
		sys.stdout.write('%(SW1)s, %(SW2)s, %(Lev0)d, %(Lev1).4f, %(Lev0Norm).4f, %(Lev1Norm).4f, %(LevenshteinI2).4f, %(LevenshteinI2Norm).4f, %(LevenshteinI4).4f, %(LevenshteinI4Norm).4f, %(LevenshteinI6).4f, %(LevenshteinI6Norm).4f, %(LevenshteinI8).4f, %(LevenshteinI8Norm).4f\n' % locals())
			
		
		