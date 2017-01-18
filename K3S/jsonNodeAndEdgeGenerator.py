from .word import Word
from .file import File 
import json
from .processor import Processor
import sys
from collections import OrderedDict

class JsonNodeAndEdgeGenerator():


	def __init__(self, identifier, destinationPath):
		self.identifier = identifier
		self.wordProcessor = Word(self.identifier)
		self.destinationPath = destinationPath
		self.fileName = identifier + '.json'
		self.jsonData = {}
		self.jsonData['nodes'] = []
		#self.jsonData['links'] = []
		return

	def setFileName(self, fileName):
		self.fileName = self.identifier + '-' + fileName + '.json'
		return

	def loadJsonData(self, word = None):
		self.jsonData = {}
		self.jsonData['nodes'] = []		
		self.jsonData['links'] = []
		
		#processor = Processor(self.identifier)
		#vocab = processor.reloadVocab()
		#kmeans = processor.reloadKMeans()
		#self.loadNodesClusterByKmeans(vocab.tfidfCalculation, vocab.tfIdf.get_feature_names(), kmeans.getAssignments())
		
		if word:
			self.loadClusterForOnlyOneWord(word)
		else:
			self.loadNodesFromDatabase()
		
		return

	def appendNode(self, id, group):
		node = {}
		node['id'] = str(id)
		node['group'] = str(group)
		self.jsonData['nodes'].append(node)
		return

	def appendLink(self, source, target, similarity):
		link = {}
		link['source'] = source
		link['target'] = target
		link['value'] = similarity
		self.jsonData['links'].append(link)
		return

	def loadNodes(self):
		words = self.wordProcessor.getWordsBySimilarity()
		return

	def write(self):
		filePath = File.join(self.destinationPath, self.fileName)
		file = File(filePath)
		file.remove()
		jsonString = json.dumps(OrderedDict([("nodes", self.jsonData['nodes']), ("links", self.jsonData['links'])]))
		file.write(jsonString)
		return


	def loadNodesClusterByKmeans(self, matrix, wordVocab, group):
		totalDocumets = matrix.shape[0]
		totalWords = matrix.shape[1]

		index = 0
		for wordColumn in range(totalWords):
			word = wordVocab[wordColumn]
			nodeGroup = group[index]
			self.appendNode(word, nodeGroup)
			index += 1
		return


	def loadNodesFromDatabase(self, clusterSize = 5):
		words = self.wordProcessor.getAllWords()

		index = 0
		for word in words:
			name = str(word[0]) + '-' + word[1]
			nodeGroup = round(word[3] % 5)
			self.appendNode(name, nodeGroup)
			edges = self.wordProcessor.getEdges(word[0])
			if edges:
				for edge in edges:
					print(edge)
					otherNodeName = str(edge[0]) + '-' + edge[1]
					self.appendLink(name, otherNodeName, edge[2])

			#if index == 10:
			#	return

			index += 1

		return

	def loadClusterForOnlyOneWord(self, word):
		self.setFileName(word)
		relatedWords = self.wordProcessor.getRelatedWordsForGraph(word)

		self.appendNode(word, 1)
		for item in relatedWords:
			if item[1] == word:
				self.appendNode(item[3], 2)
			else:
				self.appendNode(item[1], 2)

			self.appendLink(item[1], item[3], item[4])
		return


