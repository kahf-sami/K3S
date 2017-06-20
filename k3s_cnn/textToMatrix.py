import re, sys
from nltk import word_tokenize, pos_tag
from nltk.stem.porter import PorterStemmer
import numpy as np

class TextToMatrix():


	def __init__(self, width = 50, height = 50):
		self.stemmer = PorterStemmer()
		self.stopWords = Utility.getStopWords()
		self.text = None
		self.width = 0
		self.height = 0
		self.matrixType = np.empty(shape=(width, height), dtype=int)
		self.matixVerbs = np.empty(shape=(width, height), dtype=int)
		self.matrixAdj	= np.empty(shape=(width, height), dtype=int)
		self.matrixNoun	= np.empty(shape=(width, height), dtype=int)
		self.matrix = np.empty(shape=(width, height), dtype=int)
		self.posTypes = self.getPosType()
		return


	def setText(self, text):
		self.text = text
		self.loadMatrix()
		return


	def getMatrix(self):
		return self.matrix


	def getMatrixByPosType(self):
		return self.matrixType


	def getMatrixByAdj(self):
		return self.matrixAdj


	def getMatrixByNoun(self):
		return self.matrixNoun


	def getMatrixByVerb(self):
		return self.matixVerbs


	def loadMatrix(self):
		words = word_tokenize(self.text)
		if not words:
			return

		words = pos_tag(words)
		
		iWidth = 0
		iHeight = 0

		for word in words:
			posType = word[1]
			if word[0] in ['.', '?', '!', ';']:
				iHeight += 1
				iWidth = 0


			if iWidth > self.width:
				continue

			if (posType not in self.posTypes.keys()) or (not self.posTypes[posType]):
				continue

			
			self.matrix[iHeight][iWidth] = self.getAsciiValue(word)
			self.matrixType[iHeight][iWidth] = self.posTypes[posType]

			if posType in ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$']:
				self.matrixNoun[iHeight][iWidth] = self.matrix[iHeight][iWidth]
			elif  posType in ['JJ', 'JJR', 'JJS']:
				self.matrixAdj[iHeight][iWidth] = self.matrix[iHeight][iWidth]
			elif  posType in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
				self.matixVerbs[iHeight][iWidth] = self.matrix[iHeight][iWidth]


			iWidth += 1

		return



	def getAsciiValue(data):
		asciiSum = ''
		for char in data:
			asciiSum += str(ord(char))

		return asciiSum


	def getPosType(self):
		types = {}
		types['CC'] = 0		#   coordinating conjunction
		types['CD']	= 0		#   cardinal digit
		types['DT'] = 0		#   determiner
		types['EX'] = 0 	#	existential there (like: "there is" ... think of it like "there exists")
		types['FW'] = 0		#	foreign word
		types['IN'] = 0		#   preposition/subordinating conjunction
		types['JJ'] = 1		#	adjective	'big'
		types['JJR'] = 2	#	adjective, comparative	'bigger'
		types['JJS'] = 3	#	adjective, superlative	'biggest'
		types['LS'] = 0		#	list marker	1)
		types['MD'] = 0		#	modal	could, will
		types['NN'] = 9		#	noun, singular 'desk'
		types['NNS'] = 9	#	noun plural	'desks'
		types['NNP'] = 10	#	proper noun, singular	'Harrison'
		types['NNPS'] = 10	#	proper noun, plural	'Americans'
		types['PDT'] = 0	#	predeterminer	'all the kids'
		types['POS'] = 0	#	possessive ending	parent's
		types['PRP'] = 7	#	personal pronoun	I, he, she
		types['PRP$'] = 7	#	possessive pronoun	my, his, hers
		types['RB'] = 0		#	adverb	very, silently,
		types['RBR'] = 0	#	adverb, comparative	better
		types['RBS'] = 0	#	adverb, superlative	best
		types['RP'] = 0		#	particle	give up
		types['TO'] = 0		#	to	go 'to' the store.
		types['UH'] = 0		#	interjection	errrrrrrrm
		types['VB'] = 6		#	verb, base form	take
		types['VBD'] = 6	#	verb, past tense	took
		types['VBG'] = 6	#	verb, gerund/present participle	taking
		types['VBN'] = 6	#	verb, past participle	taken
		types['VBP'] = 6	#	verb, sing. present, non-3d	take
		types['VBZ'] = 6	#	verb, 3rd person sing. present	takes
		types['WDT'] = 0	#	wh-determiner	which
		types['WP'] = 0		#	wh-pronoun	who, what
		types['WP$'] = 0	#	possessive wh-pronoun	whose
		types['WRB'] = 0	#	wh-abverb	where, when
		return types


