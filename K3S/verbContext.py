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

		self.buildDetails()
		#self.buildRepresentatives(filterLowerRatedNouns)
		#self.buildLocalContexts()
		return


	def setCleanText(self, textBlock):
		textBlock = re.sub(r'\s(bin|ibn)\s', r'_\1_', str(self.textBlock), flags=re.IGNORECASE)
		textBlock = re.sub(r'([\']s?)|(-\n)|(\")|(Volume.+Book.+:)|(\n)|(\|)', ' ', str(textBlock))
		textBlock = re.sub('(\s+)|(\s\n)', ' ', str(textBlock.strip()))
		textBlock = re.sub('-', '_', str(textBlock))
		textBlock = re.sub('(^a-zA-Z0-9\.\?\!\-\_\;\s)+', '_', str(textBlock))
		return textBlock


	def buildDetails(self):
		sentenceContexts = self.getSentenceContexts()

		if not len(sentenceContexts):
			return

		self.contexts  = {}
		for sentence in sentenceContexts:
			self.countOccurance(sentence)

		
		for sentence in sentenceContexts:	
			words = self.processSentenceWords(sentence)
		
		#print(self.verbContexts)
		#print(len(self.verbContexts))

		#print(self.nVContexts)
		#print(len(self.nVContexts))
		
		'''
		filteredVerbs = {}
		total = len(self.blockVerbWords)
		min = total * 5 /100
		max = total * 30 / 100

		for blockWord in self.blockVerbWords.keys():
			if (self.blockVerbWords[blockWord] > min) and (self.blockVerbWords[blockWord] < max):
				filteredVerbs[blockWord] = self.blockVerbWords[blockWord]
		print(filteredVerbs)
		'''

		return

	def renderContext(self, word):
		print(self.nVContexts['sun'])
		print(self.nVContexts['earth'])
		print(self.nVContexts['moon'])
		sys.exit()

		word = self.stemmer.stem(word)

		associatedWords = {}

		self.max = None
		self.min = None

		if word in self.nVContexts.keys():
			mainVerbs = self.nVContexts[word]
			mainNouns = []
			for verb in self.nVContexts[word]:
				if verb in self.verbContexts.keys():
					#print(self.verbContexts[verb])
					for noun in self.verbContexts[verb]:
						if noun not in associatedWords.keys():
							associatedWords[noun] = 0
							associatedVerbs[noun] = 0

						associatedWords[noun] += 1
						
						if not self.max or (self.max < associatedWords[noun]):
							self.max = associatedWords[noun]

						if not self.min or (self.min > associatedWords[noun]):
							self.min = associatedWords[noun]

		#for verb in self.blockVerbWords.keys():
		#	if self.blockVerbWords[verb] > 1:
		#		print(verb + ' : ' + str(self.blockVerbWords[verb]))
		#self.reflectWordRepresentatives(associatedWords)

		print(associatedWords)

		#print(len(self.sentenceContexts))


		return

	def countOccurance(self, sentence):
		afterPartsOfSpeachTagging = self.nlpProcessor.getWords(sentence, True)
		
		#print(afterPartsOfSpeachTagging)
		#print('--------------------------------------------------------------')

		index = 0

		for item in afterPartsOfSpeachTagging:
			if (item[1] not in ['NNP', 'NNPS', 'NN', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']) or (len(item[0]) < 2):
				continue

			blockWord =  self.stemmer.stem(item[0].lower())
			self.pureWords[blockWord] = item[0].lower()
			if (item[1] in ['NNP', 'NNPS', 'NN', 'NNS']):
				if blockWord not in self.blockWords.keys():
					self.blockWords[blockWord] = 1
				else:
					self.blockWords[blockWord] += 1
			else:
				if blockWord not in self.blockVerbWords.keys():
					self.blockVerbWords[blockWord] = 1
				else:
					self.blockVerbWords[blockWord] += 1

		return


	def processSentenceWords(self, sentence):
		afterPartsOfSpeachTagging = self.nlpProcessor.getWords(sentence, True)
		
		#print('--------------------------------------------------------------')
		#print(afterPartsOfSpeachTagging)
		

		index = 0
		nounsBeforeVerb = 0
		verbsAfterNoun = 0
		nounsAfterVerb = 0
		contexts = {}
		lastVerb = None

			
		for item in afterPartsOfSpeachTagging:
			if (item[1] not in ['NNP', 'NNPS', 'NN', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']) or (len(item[0]) < 2):
				continue

			blockWord =  self.stemmer.stem(item[0].lower())

			if (item[1] in ['NNP', 'NNPS', 'NN', 'NNS']):
				if verbsAfterNoun:
					nounsAfterVerb += 1
				else:
					nounsBeforeVerb += 1

				if index not in contexts.keys():
					contexts[index] = []

				if blockWord not in contexts[index]:
					contexts[index].append(blockWord)

				if lastVerb:
					if lastVerb not in self.verbContexts.keys():
						self.verbContexts[lastVerb] = []

					if blockWord not in self.verbContexts[lastVerb]:
						self.verbContexts[lastVerb].append(blockWord)

					if blockWord not in self.nVContexts.keys():
						self.nVContexts[blockWord] = []

					if lastVerb not in self.nVContexts[blockWord]:
						self.nVContexts[blockWord].append(lastVerb)

					#lastVerb = None

			elif (item[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']):
				lastVerb = blockWord
				if nounsBeforeVerb:
					if verbsAfterNoun in contexts.keys():
						verbsAfterNoun += 1
						index += 1

					
		index = len(self.contexts)			
		if len(contexts):
			for i in contexts.keys():
				mainWord = None
				for word in contexts[i]:
					if not mainWord:
						mainWord = word
					elif (self.blockWords[word] == self.blockWords[mainWord]) and (mainWord != word):
						mainWord += ' ' + word
						self.blockWords[mainWord] = self.blockWords[word]
					elif self.blockWords[word] > self.blockWords[mainWord]:
						mainWord = word


				if index not in self.contexts.keys():
					self.contexts [index] = []

				self.contexts[index].append(mainWord)


		return 


	def getSentenceContexts(self):
		if len(self.sentenceContexts):
			return self.sentenceContexts

		self.sentenceContexts = re.split('[?.,!;:\n\(\)]', self.cleanTextBlock)
		self.positionContribution = len(self.sentenceContexts)
		return self.sentenceContexts

	'''
	def getRepresentative(self):
		return self.representatives


	def getCleanedTextBlock(self):
		return  re.sub('[?.!;:\n]', '', str(self.cleanTextBlock))


	def getCleanText(self):
		return self.cleanTextBlock

	
	def buildRepresentatives(self, filterLowerRatedNouns = 0.2):
		minValue = self.max * filterLowerRatedNouns
		
		allWords = self.blockWords.keys()
		
		for word in self.orderedWords:
			if filterLowerRatedNouns and self.blockWords[word] < minValue:
				continue
			
			self.representatives.append(word)
		
		print(len(self.representatives))
		return

	'''
	def reflectWordRepresentatives(self, associatedWords, filterLowerRatedNouns = 0, fileName = 'test'):
		if not associatedWords:
			return

		minValue = self.max * filterLowerRatedNouns
		nodes = {}
		nodeIndex = 0 
		totalWords = len(associatedWords)

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
		
		for word in  associatedWords:
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
				node['r'] = ((self.max) - (self.blockWords[word])) * 2 #+ ( (self.max) - (self.blockWords[word])) * 2
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
	27.	VB	Verb, base form
	28.	VBD	Verb, past tense
	29.	VBG	Verb, gerund or present participle
	30.	VBN	Verb, past participle
	31.	VBP	Verb, non-3rd person singular present
	32.	VBZ	Verb, 3rd person singular present
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