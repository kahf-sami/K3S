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
from operator import itemgetter, attrgetter
from nltk.corpus import stopwords

# NodeBox package https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation

class VerbContext(DbModel):


	def __init__(self, textBlock, identifier = None, filterLowerRatedNouns = 0.2):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'verb_context'
		self.primaryKey = 'verb_contextid'
		self.fields = ['verb_contextid', 'word', 'stemmed_word', 'nouns']
		self.nlpProcessor = NLP()
		self.textBlock = self.setCleanText(textBlock)
		self.stemmer = PorterStemmer()
		self.contexts = []
		self.representatives = []
		self.sentenceContexts = []
		self.blockWords = {}
		self.blockVerbWords = {}
		self.contributionOfWords = {}
		self.associatedContextForWords = {}
		self.combinedContexts = {}
		self.relatedContexts = {}
		self.positionContribution = 0
		self.positionContributionFactor = 0.8
		self.globalContributionFactor = 10
		self.properNounFactor = 5
		self.pureWords = {}
		self.orderedWords = {}
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
		self.parent = {}
		self.children = {}
		self.siblings = {}
		self.properNouns = {}
		self.allowedScore = 0
		self.distance = {}

		self.buildDetails()
		return


	def setCleanText(self, textBlock):
		textBlock = re.sub("-", '', str(textBlock))
		textBlock = re.sub('[^a-zA-Z0-9\.\?\!\-\_\s,!\?:;\']+', '', str(textBlock))
		textBlock = re.sub('(\s+)|(\s\n)', ' ', str(textBlock.strip()))
		return textBlock


	def buildDetails(self):
		afterPartsOfSpeachTagging = self.nlpProcessor.getWords(self.textBlock, True);

		if not len(afterPartsOfSpeachTagging):
			return

		concepts = self.nounProcessor(afterPartsOfSpeachTagging) 

		self.wordConceptsProcessor(concepts)

		self.allowedScore = self.contributionOfWords[0][1] / 10
		maxContribution = self.contributionOfWords[0][1]
		mostImportantWord = self.contributionOfWords[0][0]
		mostImportantWordOccurance = self.blockWords[mostImportantWord]
		print(mostImportantWord)

		for (word, score) in self.contributionOfWords:
			if score < self.allowedScore:
				break
			if self.allowedScore == score:
				self.distance[word] = 0
			else:
				commonWords = len(Utility.intersect(self.concepts[word], self.concepts[mostImportantWord]))
				if commonWords:
					self.distance[word] = (mostImportantWordOccurance - commonWords) * 100 % mostImportantWordOccurance

		self.distance =  [(k, self.distance[k]) for k in sorted(self.distance, key=self.distance.get, reverse=True)]
		

		print(self.distance)

		'''
		print(self.concepts['sun'])
		print(self.parent['sun'])
		print(self.siblings['sun'])
		print(self.children['sun'])
		print(self.getChildren(self.allowedScore, 'sun'))
		'''
		

		return


	def calculateDistance(self, maxContribution):
		return


	def getChildren(self, allowedScore, parent = None):
		children = []
		for (word, score) in self.contributionOfWords:
			if score < allowedScore:
				continue
			if not parent and not len(self.parent[word]):
				children.append(word)
			elif parent in self.parent[word]:
				children.append(word)
		return children


	def wordConceptsProcessor(self, concepts):
		self.contributionOfWords =  [(k, self.contributionOfWords[k]) for k in sorted(self.contributionOfWords, key=self.contributionOfWords.get, reverse=True)]
		
		#print(concepts)
		#print(self.associatedContextForWords)
		
		i = 0
		wordConcepts = {}
		for (word, score) in self.contributionOfWords:
			#print('=========================' + word + '=============================')
			prospectiveConcept = []
			for conceptIndex in self.associatedContextForWords[word]:
				prospectiveConcept = Utility.union(prospectiveConcept, concepts[conceptIndex])

				=-
			wordConcepts[word] = Utility.unique(prospectiveConcept)
			#print(wordConcepts[word])

		self.concepts = {}
		for (word1, score) in self.contributionOfWords:
			#print('=========================' + word1 + '=============================')
			wordMax = self.blockWords[word1]
			wordMin = 2
			self.concepts[word1] = []
			self.parent[word1] = []
			self.children[word1] = []
			self.siblings[word1] = []
			for word2 in wordConcepts[word1]:
				if word1 == word2:
					continue

				commonWords = Utility.intersect(wordConcepts[word1], wordConcepts[word2])
				totalCommonWords = len(commonWords)
				if self.blockWords[word2] > self.blockWords[word1]:
					self.parent[word1].append(word2)
				elif self.blockWords[word2] == self.blockWords[word1]:
					self.siblings[word1].append(word2)
				else:
					self.children[word1].append(word2)

				if (wordMax >= totalCommonWords) and (totalCommonWords >= wordMin):
					self.concepts[word1].append(word2 + '-' + str(len(commonWords)) + '-' + str(self.blockWords[word2]))
			'''
			if len(self.concepts[word1]):	
				print('=========================' + word1 + '=============================')
				print(self.concepts[word1])
				print('Parent')
				print(self.parent[word1])
				print('Siblings')
				print(self.siblings[word1])
				print('Children')
				print(self.children[word1])
			'''

		return


	def printContribution(self, allowedScore):
		for (word, score) in self.contributionOfWords:
			if score < allowedScore:
				continue
			print(word + ': ' + str(score))

		return

	def nounProcessor(self, afterPartsOfSpeachTagging):
		concepts = {}

		self.positionContribution  = len(afterPartsOfSpeachTagging)
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
				if (item[0].lower() in Utility.getStopWords()):
					continue

				addToConcepts = True 
				if item[1] in ['NNP', 'NNPS']:
					if lastNounProperNoun:
						lastProperNoun = concepts[index][-1]
						addToConcepts = False
					else:
						lastProperNoun = blockWord
					
					lastNounProperNoun = True

					if lastProperNoun not in self.properNouns.keys():
						self.properNouns[lastProperNoun] = []

					if blockWord not in self.properNouns[lastProperNoun]:
						self.properNouns[lastProperNoun].append(blockWord)
						self.properNouns[blockWord] = self.properNouns[lastProperNoun]
				else:
					lastNounProperNoun = False

				if addToConcepts:
					if index not in concepts.keys():
						concepts[index] = []
					concepts[index].append(blockWord)

					if blockWord not in self.orderedWords.keys():
						self.orderedWords[blockWord] = 0

					self.orderedWords[blockWord] += 1

				if blockWord not in self.blockWords.keys():
					self.blockWords[blockWord] = 1 
				else:
					self.blockWords[blockWord] += 1 


				if blockWord not in self.contributionOfWords.keys():
					self.contributionOfWords[blockWord] = 1 + (self.positionContribution * self.positionContributionFactor)
				else:
					self.contributionOfWords[blockWord] += 1 + (self.positionContribution * self.positionContributionFactor)


				self.positionContribution -= 1

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
