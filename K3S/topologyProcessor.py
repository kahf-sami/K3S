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
from .coreWord import CoreWord
from .wordContext import WordContext
from .wordCloud import WordCloud
from .textNodeCloud import TextNodeCloud
import re


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

	def saveBlocksInMysql(self, limit = None, processCore = True):
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
			data['text_block'] = re.sub('\'s', '', str(data['text_block']))
			data['text_block'] = re.sub('(-?)\n', '', str(data['text_block']))
			data['text_block'] = re.sub('\'|"|\(|\)|\{|\}|[|\]|<[a-zA-Z0-9\"\'-_\s"]+>', '', str(data['text_block']))
			data['text_block'] = re.sub('\s+', ' ', str(data['text_block']))
			data['text_block'].encode("utf-8")
			topologyBuilder.addTextNode(data, processCore)

			index += 1
			if (index == limit):
				break;

		
		return

	def calculateTfIdf(self):
		wordProcessor = Word(self.sourceIdentifier)
		wordProcessor.calculateTfIdf()
		return


	def calculateLocalContextImportance(self):
		wordProcessor = Word(self.sourceIdentifier)
		wordProcessor.calculateLocalContextImportance()
		return


	def buildWordContext(self):
		return;


	def buildCloud(self):
		wordCloud = WordCloud(self.sourceIdentifier)
		wordCloud.savePoints()
		wordCloud.generateLCCsv()
		return


	def buildTextCloud(self, savePoints = False):
		cloud = TextNodeCloud(self.sourceIdentifier)
		if(savePoints):
			cloud.savePoints()
		cloud.generateCsv()
		return


	def buildTextNodeCloud(self, nodeid):
		wordCloud = WordCloud(self.sourceIdentifier)
		wordCloud.buildTextNodeCloud(nodeid)
		return


	def stopWordsUpdate(self):
		coreWprdProcessor = CoreWord(self.sourceIdentifier)
		coreWprdProcessor.markStopWords()
		return


	def generateLocalContextImages(self, limit = None):
		textNodeProcessor = TextNode(self.sourceIdentifier)
		cursor = textNodeProcessor.getAllByBatch()

		index = 0
		filterLowerRatedNouns = 0
		for batch in cursor:
			if index == limit:
				break;

			textBlocks = [item for item in cursor.fetchall()]
			
			for textBlock in textBlocks:
				print(textBlock)
				lc = LocalContext(textBlock[2], self.sourceIdentifier, filterLowerRatedNouns)
				lc.reflectRepresentatives(textBlock[1])
				index += 1

		return



