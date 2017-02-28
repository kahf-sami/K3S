import os
from .config import Config
from .directory import Directory
from .file import File
from .log import Log
from .nlp import NLP
from .utility import Utility
import sys
from .topology import Topology
from .word import Word
from .localContext import LocalContext
from .localContextHighlighter import LocalContextHighlighter
from .textNode import TextNode


class TopologyProcessor():


	def __init__(self, sourceIdentifier):
		self.config = Config()
		self.log = Log()
		self.mainPath = File.join(self.config.DATA_PATH, sourceIdentifier)
		self.processedPath = File.join(self.mainPath, 'processed')
		self.localContextImagesPath = File.join(self.mainPath, 'local-context')
		self.sourceIdentifier = sourceIdentifier
		return


	def topologySetUp(self):
		topologyBuilder = Topology(self.sourceIdentifier)
		topologyBuilder.setUp()
		return

	def saveBlocksInMysql(self, limit = None):
		topologyBuilder = Topology(self.sourceIdentifier)

		sourceDir = Directory(self.processedPath)
		files = sourceDir.scan()

		if not files:
			return

		files.sort()
		index = 0
		for fileName in files:
			if fileName[0] == '.':
				continue
			filePath = File.join(self.processedPath, fileName)
			file = File(filePath)
			data = {}
			data['source_identifier'] = file.getFileName()
			data['text_block'] = file.read()
			data['text_block'].encode("utf-8")
			topologyBuilder.addTextNode(data)

			index += 1
			if (index == limit):
				break;

		
		return

	def calculateTfIdf(self):
		wordProcessor = Word(self.sourceIdentifier)
		wordProcessor.calculateTfIdf()
		return


	def generateLocalContextImages(self, limit = None):
		processedDir = Directory(self.processedPath)

		files = processedDir.scan()

		if not files:
			return

		files.sort()
		localVocab = {}
		index = 0
		nlpProcessor = NLP()
		vocab = Vocabulary.restore(self.sourceIdentifier)
		
		image = LocalContextHighlighter(self.sourceIdentifier)
		image.renderText()
		image.loadTfIdf(vocab.tfidfCalculation, vocab.getTfIdfVocabulary())

		for fileName in files:
			if fileName[0] == '.':
				continue
			
			filePath = File.join(self.processedPath, fileName)
			file = File(filePath)
			fileName = file.getFileName()
			textBlock = file.read()
			
			if textBlock:
				textBlock = nlpProcessor.removeHtmlTags(textBlock)

			lc = LocalContext(textBlock)
			image.setLocalContexts(lc.getLocalContexts())
			print(lc.getRepresentative())
			print(lc.getLocalContexts())
			image.create(index, fileName, lc.getCleanedTextBlock())
			print("--------------------------------------")
			index += 1
			if limit and index == limit:
				break
		#localVocab1 = localVocab.sort()
		#for word in localVocab:
		#	print(word + ': ' + str(localVocab[word]) )

		#print(localVocab1)
		return


