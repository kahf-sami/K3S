from .word import Word
from .file import File 
import json
from .processor import Processor

class JsonNodeAndEdgeGenerator():


	def __init__(self, identifier, destinationPath):
		self.wordProcessor = Word(identifier)
		self.destinationPath = destinationPath
		self.fileName = identifier + '.json'
		self.jsonData = {}
		self.jsonData['nodes'] = []
		self.jsonData['links'] = []
		return

	def loadJsonData(self):
		self.jsonData = {}
		self.jsonData['nodes'] = []		
		self.jsonData['links'] = []
		
		processor = Processor(identifier)
		vocab = processor.reloadVocab()
		kmeans = processor.reloadKMeans()
		self.loadNodesClusterByKmeans(vocab.tfidfCalculation, vocab.tfIdf.get_feature_names(), kmeans.getAssignments())
		return

	def appendNode(self, id, group):
		node = {}
		node['id'] = id
		node['group'] = group
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
		jsonString = json.dumps(self.jsonData)
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


	def loadLinkClusterByWordMatrix(self, matrix, wordVocab):
		return


