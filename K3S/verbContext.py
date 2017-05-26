from .nlp import NLP
import sys
import re
from .utility import Utility
import math
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from .dbModel import DbModel
from .nlp import NLP
from .localContextReflector import LocalContextReflector
import random 
import numpy
from .word import Word
# NodeBox package https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation

class VerbContext(DbModel):


	def __init__(self, textBlock, identifier = None, filterLowerRatedNouns = 0.2):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'verb_context'
		self.primaryKey = 'verb_contextid'
		self.fields = ['verb_contextid', 'word', 'stemmed_word', 'nouns']
		self.nlpProcessor = NLP()
		self.textBlock = textBlock
		self.cleanTextBlock = self.setCleanText(textBlock)
		self.stemmer = PorterStemmer()
		self.contexts = []
		self.representatives = []
		self.sentenceContexts = []
		self.blockWords = {}
		self.blockVerbWords = {}
		self.associatedContextForWords = {}
		self.combinedContexts = {}
		self.relatedContexts = {}
		self.positionContribution = 0
		self.positionContributionFactor = 0.8
		self.globalContributionFactor = 10
		self.properNounFactor = 5
		self.pureWords = {}
		self.orderedWords = []
		self.verbContexts = {}
		self.nVContexts = {}
		self.max = 0
		self.min = None
		self.circleSizeMultiplier = 0.5
		self.zoneColors = ['crimson', 'fuchsia', 'pink', 'plum', 
			'violet', 'darkorchid', 'royalblue', 
			'dodgerblue', 'lightskyblue', 'aqua', 'aquamarine', 'green', 
			'yellowgreen', 'yellow', 'lightyellow', 'lightsalmon', 
			'coral', 'tomato', 'brown', 'maroon', 'gray']
		self.contexts = {}


		self.concepts = {}

		#---------------------------------------------
		self.lastNounProperNoun = False
		self.lastProperNoun = None
		#---------------------------------------------

		self.buildDetails()
		return


	def setCleanText(self, textBlock):
		#textBlock = re.sub(r'\s(bin|ibn)\s', r'_\1_', str(self.textBlock), flags=re.IGNORECASE)
		#textBlock = re.sub(r'([\']s?)|(-\n)|(\")|(Volume.+Book.+:)|(\n)|(\|)', ' ', str(textBlock))
		textBlock = re.sub("-", '', str(textBlock))
		textBlock = re.sub('[^a-zA-Z0-9\.\?\!\-\_\s]+', '', str(textBlock))
		textBlock = re.sub('(\s+)|(\s\n)', ' ', str(textBlock.strip()))
		return textBlock


	def buildDetails(self):
		afterPartsOfSpeachTagging = self.nlpProcessor.getWords(self.textBlock, True);

		if not len(afterPartsOfSpeachTagging):
			return

		concepts = self.nounProcessor(afterPartsOfSpeachTagging)
		#print(concepts)
		#print(self.associatedContextForWords)
		
		i = 0
		wordConcepts = {}
		for word in self.associatedContextForWords.keys():
			#print('=========================' + word + '=============================')
			prospectiveConcept = []
			for conceptIndex in self.associatedContextForWords[word]:
				prospectiveConcept = Utility.union(prospectiveConcept, concepts[conceptIndex])

			wordConcepts[word] = Utility.unique(prospectiveConcept)
			#print(wordConcepts[word])

		self.concepts = {}
		parent = {}
		children = {}
		siblings = {}
		for word1 in self.associatedContextForWords.keys():
			#print('=========================' + word1 + '=============================')
			wordMax = self.blockWords[word1]
			wordMin = 0
			self.concepts[word1] = []
			parent[word1] = []
			children[word1] = []
			siblings[word1] = []
			for word2 in wordConcepts[word1]:
				if word1 == word2:
					continue
				#if (self.blockWords[word2] == 1) or (self.blockWords[word2] > wordMax):
				#	continue
				commonWords = Utility.intersect(wordConcepts[word1], wordConcepts[word2])
				totalCommonWords = len(commonWords)
				if self.blockWords[word2] > self.blockWords[word1]:
					parent[word1].append(word2)
				elif self.blockWords[word2] == self.blockWords[word1]:
					siblings[word1].append(word2)
				else:
					children[word1].append(word2)

				if (wordMax >= totalCommonWords) and (totalCommonWords >= wordMin):
					self.concepts[word1].append(word2 + '-' + str(len(commonWords)) + '-' + str(self.blockWords[word2]))
			
			if len(self.concepts[word1]):	
				print('=========================' + word1 + '=============================')
				print(self.concepts[word1])
				print('Parent')
				print(parent[word1])
				print('Siblings')
				print(siblings[word1])
				print('Children')
				print(children[word1])

			
		#print(self.blockWords['sun'])

		#print(self.concepts['sun'])
		#print(self.concepts['earth'])
		#print(self.concepts['moon'])

		return

	def nounProcessor(self, afterPartsOfSpeachTagging):
		concepts = {}

		index = 0
		lastNounProperNoun = False
		for item in afterPartsOfSpeachTagging:
			if (len(item[1]) == 1):
				# Puncuation
				lastNounProperNoun = False
				continue

			if (item[1] not in ['NNP', 'NNPS', 'NN', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']) or (len(item[0]) < 2):
				continue

			blockWord =  self.stemmer.stem(item[0].lower())
			self.pureWords[blockWord] = item[0].lower()

			if (item[1] in ['NNP', 'NNPS', 'NN', 'NNS']):
				if item[1] in ['NNP', 'NNPS']:
					if lastNounProperNoun:
						blockWord = concepts[index][-1] + ' ' + blockWord
						if len(concepts[index]):
							del concepts[index][-1]
					
					lastNounProperNoun = True

				if index not in concepts.keys():
					concepts[index] = []

				concepts[index].append(blockWord)

				if blockWord not in self.blockWords.keys():
					self.blockWords[blockWord] = 1
				else:
					self.blockWords[blockWord] += 1

				if blockWord not in self.associatedContextForWords.keys():
					self.associatedContextForWords[blockWord] = []

				self.associatedContextForWords[blockWord].append(index)
			else:
				index = len(concepts) + 1
				lastNounProperNoun = False

				if blockWord not in self.blockVerbWords.keys():
					self.blockVerbWords[blockWord] = 1
				else:
					self.blockVerbWords[blockWord] += 1


		return concepts


	def getSentenceContexts(self):
		if len(self.sentenceContexts):
			return self.sentenceContexts

		self.sentenceContexts = re.split('[?.!\n\(\)]', self.cleanTextBlock)
		self.positionContribution = len(self.sentenceContexts)
		return self.sentenceContexts

		return