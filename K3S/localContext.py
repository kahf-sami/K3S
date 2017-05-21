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

class LocalContext(DbModel):


	def __init__(self, textBlock, identifier = None, filterLowerRatedNouns = 0.2):
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
		self.positionContributionFactor = 0.8
		self.globalContributionFactor = 10
		self.properNounFactor = 5
		self.pureWords = {}
		self.orderedWords = []
		self.max = 0
		self.min = None
		self.circleSizeMultiplier = 0.5
		self.zoneColors = ['crimson', 'fuchsia', 'pink', 'plum', 
			'violet', 'darkorchid', 'royalblue', 
			'dodgerblue', 'lightskyblue', 'aqua', 'aquamarine', 'green', 
			'yellowgreen', 'yellow', 'lightyellow', 'lightsalmon', 
			'coral', 'tomato', 'brown', 'maroon', 'gray']

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
		textBlock = re.sub(r'([\']s?)|(-\n)|(\")|(Volume.+Book.+:)|(\n)', ' ', str(textBlock))
		textBlock = re.sub('(\s+)|(\s\n)', ' ', str(textBlock.strip()))
		textBlock = re.sub('-', '_', str(textBlock))
		return textBlock


	def buildDetails(self):
		sentenceContexts = self.getSentenceContexts()

		if not len(sentenceContexts):
			return

		#limit = 10
		#count = 0
		for sentence in sentenceContexts:
			words = self.processSentenceWords(sentence)
			#count += 1
			#if limit == count:
			#	sys.exit()
			#if len(words):
			#	self.addToCombinedContext(words)


		#print(self.blockWords)
		#print(self.combinedContexts)
		#print(self.relatedContexts)
		return


	def buildRepresentatives(self, filterLowerRatedNouns = 0.2):
		print(len(self.blockWords))
		print('----------------')
		minValue = self.max * filterLowerRatedNouns
		print(minValue)
		allWords = self.blockWords.keys()
		
		for word in self.orderedWords:
			if filterLowerRatedNouns and self.blockWords[word] < minValue:
				continue
			
			self.representatives.append(word)
		print(len(self.representatives))
		return


	def reflectRepresentatives(self, fileName, filterLowerRatedNouns = 0.2):
		#print(filterLowerRatedNouns)
		#print(len(self.blockWords))
		#print(len(self.representatives))
		#sys.exit()
		if not len(self.representatives):
			return

		minValue = self.max * filterLowerRatedNouns
		nodes = {}
		nodeIndex = 0
		totalWords = len(self.representatives)

		thetaGap = 360 / (totalWords)
		theta = 0
		x = []
		y = []
		colors = []
		sizes = []
		colTest = lambda: random.randint(0,255)
		maxRadius = None

		wordProcessor = Word(self.identifier)
		'''
		node = {}
		node['index'] = nodeIndex
		node['label'] = '0'
		node['color'] = 'black'
		node['r'] = 0
		node['theta'] = 0
		node['x'] = 0
		node['y'] = 0

		nodes['0'] = node

		nodeIndex += 1
		'''

		radiusGroups = {}
		processedNodes = {}

		currentColors = {}
		
		for word in  self.representatives:
			mainWord = self.pureWords[word]
			#word =  self.stemmer.stem(word)

			#if word not in self.representatives:
			#	continue

			if self.blockWords[word] < minValue:
				theta += thetaGap
				continue

			if word not in nodes.keys():
				getGlobalContributionDetails = wordProcessor.getGlobalContributionDetails(word)
				if getGlobalContributionDetails:
					zone = getGlobalContributionDetails[1]
					number_of_blocks = getGlobalContributionDetails[0]
				else:
					zone = 19
					number_of_blocks = 0


				node = {}
				node['index'] = nodeIndex
				node['label'] = mainWord #+ '-' + str(zone)
				#+ '-' + str(self.blockWords[word]) + '-' + str(getGlobalContribution)
				if not zone:
					node['color'] = 'black'
				else:
					node['color'] = self.zoneColors[zone]
				node['r'] = (self.max) - (self.blockWords[word]) #+ ( (self.max) - (self.blockWords[word])) * 2
				node['theta'] = theta
				node['zone'] = zone
				node['x'] = node['r'] * numpy.cos(numpy.deg2rad(theta))
				node['y'] = node['r'] * numpy.sin(numpy.deg2rad(theta))

				nodes[word] = node 
				nodeIndex += 1
				theta += thetaGap
				x.append(node['x'])
				y.append(node['y'])
				colors.append(node['color'])

				size = number_of_blocks * self.circleSizeMultiplier
				if not size:
					size = 2
				sizes.append(size)
				#print(mainWord + '(' + str(node['theta']) + ')' + str(node['r']))

				currentColors[zone] = self.zoneColors[zone]

				if not maxRadius or maxRadius < node['r']:
					maxRadius = node['r']
				'''	
				if zone <= 18:
					r = math.ceil(node['r'] / 10)
					if not r in radiusGroups.keys():
						radiusGroups[r] = []
					
					processedNodes[word] = node
					radiusGroups[r].append(word)
				'''	

		distance = maxRadius * 0.3

		#print(currentColors)
		#sys.exit()
		polygons = None
		
		#polygons = self.getPolygons(nodes, distance)

		'''
		results = self.addCurrentColorLegend(nodes, nodeIndex, maxRadius, currentColors, x, y, colors, sizes)
		nodes = results[0]
		x = results[1]
		y = results[2]
		colors = results[3]
		sizes = results[4]
		'''
		lcr = LocalContextReflector(self.identifier)
		lcr.create(x, y, colors, nodes, sizes, fileName, polygons)
		
		return


	def addCurrentColorLegend(self, nodes, nodeIndex, maxRadius, currentColors, x, y, colors, sizes):
		Y = 800

		if len(currentColors):
			for zone in range(1, 20):
				if zone not in currentColors.keys():
					continue
				node = {}
				node['index'] = nodeIndex
				node['label'] = 'zone - ' + str(zone)
				node['color'] = currentColors[zone]
				node['r'] = 0
				node['theta'] = 0
				node['zone'] = zone
				node['x'] = maxRadius - 120
				node['y'] = Y

				nodes[zone] = node 

				x.append(node['x'])
				y.append(node['y'])
				colors.append(node['color'])
				sizes.append(10)
				Y -= 50
				nodeIndex += 1

		return [nodes, x, y, colors, sizes]



	def getPolygons(self, nodes, distance):
		if not nodes:
			return None


		edges = {}	

		for node1 in nodes:
			node1 = nodes[node1]
			
			for node2 in nodes:
				node2 = nodes[node2]

				if node1['index'] == node2['index']:
					continue

				xDistance = node2['x'] - node1['x']
				yDistance = node2['y'] - node1['y']
				distanceBetweenNodes = abs(math.sqrt(xDistance * xDistance + yDistance * yDistance))

				if distanceBetweenNodes > distance:
					continue

				identifier = str(node2['index']) + '-' + str(node1['index'])
				if identifier in edges.keys():
					continue

				edges[identifier] = {'start-x' : node1['x'], 'start-y' : node1['y'], 'start-w' : node1['label'], 'end-x' : node2['x'], 'end-y' : node2['y'], 'end-w' : node2['label']}
				#print(node1)
				#print(node2)
				#print(distanceBetweenNodes)
				#print(edges[identifier])
				


		#print(edges)
		print(len(edges))
		#print(len(nodes))
		#print(distance)
		return edges


		
	'''
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
	'''
	'''
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
	'''

	def processSentenceWords(self, sentence):
		afterPartsOfSpeachTagging = self.nlpProcessor.getWords(sentence, True)
		print(afterPartsOfSpeachTagging)
		print('----------------')

		if not len(afterPartsOfSpeachTagging):
			self.positionContribution -= 1
			return []

		lastType = None
		words = []
		index = 0
			
		for item in afterPartsOfSpeachTagging:
			word =  self.stemmer.stem(item[0].lower())
			self.pureWords[word] = item[0].lower()
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
				self.orderedWords.append(blockWord)
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

		allWords = self.blockWords.keys()

		self.deleteLocalContextsByNodeid(nodeid)

		for representative in allWords:
			if representative not in self.representatives:
				continue

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