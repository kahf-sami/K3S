import os
from .config import Config
from .directory import Directory
from .file import File
from .log import Log
from .toText import ToText
from .vocabulary import Vocabulary
from .nlp import NLP
from .utility import Utility
import sys
import re
from .kMeans import KMeans
from .image import Image
from .topology import Topology
from .word import Word
#from .TFKMeansCluster import TFKMeansCluster


class Processor():


	def __init__(self, sourceIdentifier):
		self.config = Config()
		self.log = Log()
		self.mainPath = File.join(self.config.DATA_PATH, sourceIdentifier)
		self.rawPath = File.join(self.mainPath, 'raw')
		self.processedPath = File.join(self.mainPath, 'processed')
		self.filteredPath = File.join(self.mainPath, 'after-filtered')
		self.graphsPath = File.join(self.mainPath, 'graphs')
		self.sourceIdentifier = sourceIdentifier
		
		return


	def clean(self):
		directory = Directory(self.mainPath)
		directory.remove()
		
		return


	def createSourceSetup(self):
		directory = Directory(self.rawPath)
		directory.create()

		processedDir = Directory(self.processedPath)
		processedDir.create()

		graphDir = Directory(self.graphsPath)
		processedDir.create()

		filteredDir = Directory(self.filteredPath)
		filteredDir.create()

		return


	def copy(self, sourcePath, destinationPath = None):
		sourcefile = File(sourcePath)
		if not destinationPath:
			destinationPath = File.join(self.rawPath, sourcefile.getFileName())
		File.copy(sourcePath, destinationPath)
		return


	def extractBlocks(self, path = None):
		if not path:
			path = self.rawPath

		hasExtracted = False
		
		for root, dirs, files in os.walk(self.rawPath, topdown=False):
			if files:
				for name in files:
					filePath = File.join(root, name)
					file = File(filePath)
					if file.isZipFile():
						file.unzip()
						file.remove()
					elif file.isTarFile():
						file.untar()
						file.remove()
					elif file.isPdfFile():
						pdfToText = ToText(filePath, self.processedPath)
						pdfToText.convertFromPdf()
						hasExtracted = True
					elif file.isCsvFile:
						csvToText = ToText(filePath, self.processedPath)
						csvToText.convertFromCsv()
						hasExtracted = True
					else:
						self.copy(filePath, self.processedPath)
						hasExtracted = True
			if dirs:
				for name in dirs:
					dirPath = File.join(root, name)
					if self.extractBlocks(dirPath):
						hasExtracted = True

		return hasExtracted


	def nlpPreProcessBlocks(self):
		processedDir = Directory(self.processedPath)

		files = processedDir.scan()

		if not files:
			return

		nlpProcessor = NLP()
		for fileName in files:
			filePath = File.join(self.processedPath, fileName)
			file = File(filePath)
			fileName = file.getFileName()
			destinationFilePath = File.join(self.filteredPath, fileName)
			destinationFile = File(destinationFilePath)
			
			textBlock = file.read()
			textBlock = nlpProcessor.getFiltered(textBlock)

			if textBlock:
				destinationFile.write(textBlock)

		return

	def reloadVocab(self):
		vocab = Vocabulary.restore(self.sourceIdentifier)
		return vocab

	def buildVocabulary(self, limit = None, onlyNoun = True):
		fileNames = self.getFilteredFiles()
		
		if not fileNames:
			return

		if limit == None:
			limit = len(fileNames)

		vocab = Vocabulary.restore(self.sourceIdentifier)

		i = 0
		docs = []
		wordProcessor = Word(self.sourceIdentifier)
		#fileNames = ['Volume_1,_Book_12,_Number_790.txt', 'Volume_1,_Book_12,_Number_791.txt', 'Volume_1,_Book_12,_Number_792.txt']
		for fileName in fileNames:
			filePath = File.join(self.filteredPath, fileName)
			file = File(filePath)
			textBlock = file.read()
			del file
			if textBlock:
				textBlock = textBlock.replace("'", ' ')
				textBlock = str(textBlock.encode('utf-8', 'replace'))
				textBlock = re.sub("b'",'', textBlock)
				textBlock = re.sub("'",'', textBlock)
				if onlyNoun:
					nouns = wordProcessor.getNouns(textBlock)
					if nouns:
						textBlock = " ".join(nouns)
					else:
						textBlock = None
				if textBlock:
					docs.append(textBlock)
			i += 1
			if i == limit:
				break

			#print(fileName)
			#print(i)
		
		vocab.bulidVocabularyFromTextBlock(docs)
		vocab.transfromTextBlocksToWordIdsMatrix(docs)
		vocab.useTfIdf(docs)
		vocab.save()

		return vocab


	def produceImages(self, limit = None, withText = False):
		vocab = Vocabulary.restore(self.sourceIdentifier)
		
		image = Image(self.sourceIdentifier)
		if withText:
			image.renderText()
		image.loadTfIdf(vocab.tfidfCalculation, vocab.getTfIdfVocabulary())

		fileNames = self.getFilteredFiles()
		
		if not fileNames:
			return

		if limit == None:
			limit = len(fileNames)
		
		documentNumber = 0
		for fileName in fileNames:
			filePath = File.join(self.filteredPath, fileName)
			file = File(filePath)
			textBlock = file.read()
			del file
			if textBlock:
				image.create(documentNumber, fileName, textBlock)
			documentNumber += 1
			if documentNumber == limit:
				break

		return


	def reloadKMeans(self):
		kmeans = KMeans.restore(self.sourceIdentifier)
		return kmeans


	def calculateKMeans(self, vocab, numberOfClusters = 5, iteration = 100):
		kmeansProcessor = KMeans(self.sourceIdentifier, numberOfClusters, iteration)
		kmeansProcessor.setVectors(vocab.tfidfCalculation)
		kmeansProcessor.computeCluster()
		kmeansProcessor.save()
		return kmeansProcessor


	def topologySetUp(self):
		topologyBuilder = Topology(self.sourceIdentifier)
		topologyBuilder.setUp()
		return

	def saveBlocksInMysql(self, limit = None):
		topologyBuilder = Topology(self.sourceIdentifier)

		files = self.getFilteredFiles()

		if not files:
			return

		index = 0
		for fileName in files:
			filePath = File.join(self.filteredPath, fileName)
			file = File(filePath)
			textBlock = file.read()
			data = {}
			data['source_identifier'] = file.getFileName()
			data['text_block'] = file.read()
			data['text_block'].encode("utf-8")
			topologyBuilder.addTextNode(data)
			index += 1
			if (index == limit):
				break;
		return


	def contextExtraction(self):
		topologyBuilder = Topology(self.sourceIdentifier)
		topologyBuilder.extractContext()


	def getFilteredFiles(self):
		sourceDir = Directory(self.filteredPath)

		files = sourceDir.scan()

		if not files:
			if self.filteredPath != self.processedPath:
				self.filteredPath = self.processedPath
				sourceDir = Directory(self.processedPath)
			else:
				return None

		return sourceDir.scan()



