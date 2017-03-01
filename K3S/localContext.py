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

class LocalContext(DbModel):


	def __init__(self, textBlock, identifier = None, filterLowerRatedNouns = 0.1):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'local_context'
		self.primaryKey = 'local_contextid'
		self.fields = ['local_contextid', 'nodeid', 'word', 'weight']
		self.nlpProcessor = NLP()
		self.textBlock = textBlock
		self.cleanTextBlock = self.setCleanText(textBlock)
		self.stemmer = PorterStemmer()
		self.contexts = []
		self.representatives = []
		self.sentenceContexts = []
		self.blockWords = {}
		self.associatedContextForWords = {}
		self.combinedContexts = {}
		self.relatedContexts = {}
		self.positionContribution = 0
		self.positionContributionFactor = 0.5
		self.properNounFactor = 5
		self.max = None
		self.min = None

		self.buildDetails()
		self.buildRepresentatives(filterLowerRatedNouns)
		#self.buildLocalContexts()
		return


	def getRepresentative(self):
		return self.representatives


	def getSentenceContexts(self):
		if len(self.sentenceContexts):
			return self.sentenceContexts

		self.sentenceContexts = re.split('[?.,!;:\n\(\)]', self.cleanTextBlock)
		self.positionContribution = len(self.sentenceContexts)
		return self.sentenceContexts


	'''
	def getLocalContexts(self):
		return self.combinedContexts
	'''

	def getCleanedTextBlock(self):
		return  re.sub('[?.!;:\n]', '', str(self.cleanTextBlock))


	def getCleanText(self):
		return self.cleanTextBlock

	def setCleanText(self, textBlock):
		textBlock = re.sub(r'\s(bin|ibn)\s', r'_\1_', str(self.textBlock), flags=re.IGNORECASE)
		textBlock = re.sub(r'([\']s?)|(-\n)|(\")|(Volume.+Book.+:)', '', str(textBlock))
		textBlock = re.sub('(\s+)|(\s\n)', ' ', str(textBlock.strip()))
		textBlock = re.sub('-', '_', str(textBlock))
		return textBlock


	def buildDetails(self):
		sentenceContexts = self.getSentenceContexts()

		if not len(sentenceContexts):
			return

		for sentence in sentenceContexts:
			words = self.processSentenceWords(sentence)

			#if len(words):
			#	self.addToCombinedContext(words)


		#print(self.blockWords)
		#print(self.combinedContexts)
		#print(self.relatedContexts)
		return


	def buildRepresentatives(self, filterLowerRatedNouns = 0.1):
		minValue = self.max * filterLowerRatedNouns

		allWords = self.blockWords.keys()

		
		for word in  allWords:
			if self.blockWords[word] < minValue:
				continue
			else:
				self.representatives.append(word)

		return


	def reflectRepresentatives(self, fileName, filterLowerRatedNouns = 0.1):
		if not len(self.representatives):
			return

		minValue = self.max * filterLowerRatedNouns
		nodes = {}
		nodeIndex = 0
		totalWords = len(self.blockWords)
		thetaGap = 360 / totalWords
		theta = 0
		x = []
		y = []
		colors = []
		colTest = lambda: random.randint(0,255)
		
		for word in  self.representatives:
			if self.blockWords[word] < minValue:
				continue

			itemColor = '#%02X%02X%02X' % (colTest(),colTest(),colTest())

			if word in nodes.keys():
				node = nodes[word]
			else:
				node = {}
				node['index'] = nodeIndex
				node['label'] = word + '-' + str(self.blockWords[word])
				node['color'] = itemColor
				node['r'] =  self.blockWords[word]
				node['theta'] = theta
				node['x'] = node['r'] * numpy.cos(numpy.deg2rad(theta))
				node['y'] = node['r'] * numpy.sin(numpy.deg2rad(theta))
				
				nodes[word] = node 
				nodeIndex += 1
				theta += thetaGap
				x.append(node['x'])
				y.append(node['y'])
				colors.append(itemColor)
			



		lcr = LocalContextReflector(self.identifier)
		lcr.create(x, y, colors, nodes, None, None, fileName)
		
		return
		

	def reflect(self, fileName, filterLowerRatedNouns = 0):
		lcr = LocalContextReflector(self.identifier)

		processedContexts = []

		edges = []
		nodes = {}
		#contextPolygons = []
		#contextColors = []
		nodeIndex = 0
		totalWords = len(self.blockWords)
		thetaGap = 360 / totalWords
		theta = 0
		minValue = self.max * filterLowerRatedNouns

		x = []
		y = []
		colors = []

		colTest = lambda: random.randint(0,255)
		#print(self.max)
		#print(self.min)

		contextIndex = 0
		for context in self.combinedContexts:
			itemColor = '#%02X%02X%02X' % (colTest(),colTest(),colTest())
			#polygon = []
			contextMin = None
			for word in  self.combinedContexts[context]:
				if self.blockWords[word] < minValue:
					continue

				if word in nodes.keys():
					node = nodes[word]
				else:
					node = {}
					node['index'] = nodeIndex
					node['label'] = word + '-' + str(self.blockWords[word])
					node['color'] = itemColor
					node['r'] =  self.blockWords[word]
					node['theta'] = theta
					node['x'] = node['r'] * numpy.cos(numpy.deg2rad(theta))
					node['y'] = node['r'] * numpy.sin(numpy.deg2rad(theta))
					nodes[word] = node 
					nodeIndex += 1
					theta += thetaGap
					x.append(node['x'])
					y.append(node['y'])
					colors.append(itemColor)


				#point = (node['x'], node['y'])
				#polygon.append(point)

			#contextPolygons.append(polygon)
			#contextColors.append(itemColor)

		lcr.create(x, y, colors, nodes, None, None, fileName)
		#pyplot.plot([point[0], point2[0]], [point[1], point2[1]])

		return

	def addToCombinedContext(self, words):
		uniqueWords = Utility.unique(words)
		contextIndex = len(self.combinedContexts)		

		alreadyProcessedWords = self.associatedContextForWords.keys()
		alreadyProcessedWordsSentenceWords = Utility.intersect(alreadyProcessedWords, uniqueWords)
		notProcessedWords = list(set(uniqueWords) - set(alreadyProcessedWordsSentenceWords))

		totalWords = len(words)
		totalProcessedWords = len(alreadyProcessedWordsSentenceWords)
		totalNotProcessedWords = len(notProcessedWords)

		self.combinedContexts[contextIndex] = uniqueWords
		for uniqueWord in notProcessedWords:
			self.associatedContextForWords[uniqueWord] = contextIndex
						
		if not totalProcessedWords:
			return

		matchedContexts = []
		for processedContextItem in alreadyProcessedWordsSentenceWords:
			cIndex = self.associatedContextForWords[processedContextItem]
			if cIndex not in matchedContexts:
				matchedContexts.append(cIndex)

				if cIndex not in self.relatedContexts.keys():
					self.relatedContexts[cIndex] = []

				self.relatedContexts[cIndex].append(contextIndex)
									
				if contextIndex not in self.relatedContexts.keys():
					self.relatedContexts[contextIndex] = []
				
				self.relatedContexts[contextIndex].append(cIndex)

		return

	def processSentenceWords(self, sentence):
		afterPartsOfSpeachTagging = self.nlpProcessor.getWords(sentence, True)
		#print(afterPartsOfSpeachTagging)
		
		if not len(afterPartsOfSpeachTagging):
			self.positionContribution -= 1
			return []

		lastType = None
		words = []
		index = 0
			
		for item in afterPartsOfSpeachTagging:
			word =  self.stemmer.stem(item[0].lower())
			currentType = item[1]
			bloclWord = None

			if (item[1] not in ['NNP', 'NNPS', 'NN', 'NNS']) or (len(word) < 2):
				continue

			words.append(word)

			index += 1
			lastType = currentType
			blockWord = word

			if blockWord not in self.blockWords.keys():
				self.blockWords[blockWord] = (1 + (self.positionContribution * self.positionContributionFactor))
			else:
				self.blockWords[blockWord] += (1 + (self.positionContribution * self.positionContributionFactor))

			if item[1] == 'NNP':
				self.blockWords[blockWord] += self.properNounFactor

			if not self.max or self.max < self.blockWords[blockWord]:
				self.max = self.blockWords[blockWord]

			if not self.min or self.min > self.blockWords[blockWord]:
				self.min = self.blockWords[blockWord]

		
		self.positionContribution -= 1

		return words

	'''

	def buildRepresentatives(self):
		representatives = self.nlpProcessor.getNouns(self.textBlock)
		representatives = [word for word in representatives if word not in stopwords.words('english')]
		#print(representatives)
		self.representatives = representatives
		return
	'''

	'''
	def buildLocalContexts(self):
		sentenceContexts = self.getSentenceContexts()

		#print(sentenceContexts)
		localContexts = []
		index = 0
		for sentence in sentenceContexts:
			prospectiveContextItems = self.getProspectiveContextItems(sentence)
			#print('--------------')
			#print(sentence)
			
			totalProspectiveItems = len(prospectiveContextItems)
			if totalProspectiveItems == 0:
				continue
			#print(prospectiveContextItems)
			if totalProspectiveItems == 1:
				# only one item
				localContexts = self.appendToLocalContext(prospectiveContextItems[0], localContexts)
				continue
					
			intexOfItem = self.getIndexOfProspectiveContentItems(prospectiveContextItems)

			itemIndex = 0
			combinedContext = []
			for item in prospectiveContextItems:
				if itemIndex == (totalProspectiveItems - 1):
					#Last item
					if item not in combinedContext:
						localContexts = self.appendToLocalContext(item, localContexts)
						
					break
						
				contextDistance = abs(intexOfItem[itemIndex] - intexOfItem[itemIndex + 1])
				if contextDistance <= 5:
					if item not in combinedContext:
						combinedContext = self.appendItemToLocalContext(item, combinedContext)

					if prospectiveContextItems[itemIndex + 1] not in combinedContext:
						combinedContext = self.appendItemToLocalContext(prospectiveContextItems[itemIndex + 1], combinedContext)
				else:
					localContexts = self.appendToLocalContext(item, localContexts)

				itemIndex += 1


			if len(combinedContext):
				localContexts.append(combinedContext)

			index += 1
		#print(localContexts)
		#sys.exit()
		
		return self.loadContexts(localContexts)

	'''

	'''
	def getIndexOfProspectiveContentItems(self, prospectiveContextItems):
		intexOfItem = []
		for item in prospectiveContextItems:
			intexOfItem.append(self.representatives.index(item))
		return intexOfItem
	'''


	''''

	def appendToLocalContext(self, item, localContexts):
		#stemmedItem = self.stemmer.stem(item)
		#if stemmedItem == item:
		#	itemList = [item]
		#else:
		#	itemList = [item, stemmedItem]
		itemList = [item]
		if itemList not in localContexts:
			localContexts.append(itemList)

		return localContexts
	'''
	'''
	def appendItemToLocalContext(self, item, localContexts):
		#stemmedItem = self.stemmer.stem(item)
		#if (stemmedItem != item) and (stemmedItem not in localContexts):
		#	localContexts.append(stemmedItem)

		if item not in localContexts:
			localContexts.append(item)

		return localContexts
	'''

	'''

	def getProspectiveContextItems(self, sentence):
		words = self.nlpProcessor.getWords(sentence)
		return Utility.intersect(self.representatives, words)
	'''

	'''
	def loadContexts(self, localContexts):
		self.contexts = []	
		for localContext in localContexts:
			setMain = set(localContext) 
			totalMain = len(localContext)
			subSetOfAnother = False
			for subContext in localContexts:
				totalSub = len(subContext)
				if totalSub <= totalMain:
					continue
				setSub = set(subContext) 
				commonItems = setMain & setSub
				similarity = len(commonItems) / totalMain
				if similarity >= 0.75:
					subSetOfAnother = True
				
			if (not subSetOfAnother) and (localContext not in self.contexts):
				self.contexts.append(localContext)

		return self.contexts

	'''


	def saveLocalContexts(self, nodeid):
		if not self.representatives:
			return

		self.deleteLocalContextsByNodeid(nodeid)

		for representative in self.representatives:
			data = {}
			data['nodeid'] = nodeid
			data['word'] = representative
			data['weight'] = self.blockWords[representative]
			self.save(data)
		
		return


	def deleteLocalContextsByNodeid(self, nodeid):
		sql = "DELETE FROM local_context WHERE nodeid = " + str(nodeid)
		params = []
		self.mysql.updateOrDelete(sql, params)
		return