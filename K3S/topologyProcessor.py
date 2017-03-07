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
		textNodeProcessor = TextNode(self.sourceIdentifier)
		textBlocks = textNodeProcessor.getAllByBatch(limit, 1)

		index = 0
		filterLowerRatedNouns = 0
		while len(textBlocks):

			if index == limit:
				break;

			for textBlock in textBlocks:
				print(textBlock)
				lc = LocalContext(textBlock[2], self.sourceIdentifier, filterLowerRatedNouns)
				lc.reflectRepresentatives(textBlock[1])
				index += 1

		return


