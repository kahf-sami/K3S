import os, sys,re
from .config import Config
from k3s_utility.directory import Directory
from k3s_utility.file import File
from k3s_utility.log import Log
from k3s_utility.nlp import NLP
from k3s_utility.utility import Utility
from .schema import Schema
from .textNode import TextNode
from .word import Word


class Processor():


	def __init__(self, sourceIdentifier):
		self.config = Config()
		self.mainPath = File.join(self.config.DATA_PATH, sourceIdentifier)
		self.processedPath = File.join(self.mainPath, 'processed')
		#self.localContextImagesPath = File.join(self.mainPath, 'local-context')
		self.sourceIdentifier = sourceIdentifier
		return


	def setUpDb(self):
		schemaBuilder = Schema(self.sourceIdentifier)
		schemaBuilder.setUp()
		return

	
	def saveBlocksInMysql(self, limit = None, processCore = True):
		textNode = TextNode(self.sourceIdentifier)

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
			data['text_block'] = re.sub('(-?)\n', ' ', str(data['text_block']))
			data['text_block'] = re.sub('/|\|,|:', ' ', str(data['text_block']))
			data['text_block'] = re.sub('\'|"|\(|\)|\{|\}|[|\]|<[a-zA-Z0-9\"\'-_\s"]+>', '', str(data['text_block']))
			data['text_block'] = re.sub('\s+', ' ', str(data['text_block']))
			data['text_block'].encode("utf-8")
			textNode.save(data, processCore)

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

