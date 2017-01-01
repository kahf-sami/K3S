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


	def buildVocabulary(self, limit = None):
		filteredDir = Directory(self.filteredPath)
		fileNames = filteredDir.scan()
		
		if not fileNames:
			return

		if limit == None:
			limit = len(fileNames)

		vocab = Vocabulary.restore(self.sourceIdentifier)

		i = 0
		docs = []
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


	def calculateKMeans(self):
		vocab = self.buildVocabulary(10)

		#print(TFKMeansCluster(vocab.tfidfCalculation, 5))
		#sys.exit()
		#kmeansProcessor = TFKMeansCluster(vocab.tfidfCalculation, 5)
		numberOfClusters = 5
		iteration = 1
		kmeansProcessor = KMeans(self.sourceIdentifier, numberOfClusters, iteration)
		kmeansProcessor.setVectors(vocab.tfidfCalculation)
		print(kmeansProcessor.computeCluster())
		#data_centroids, samples = kmeansProcessor.createSamples()
		#print(data_centroids)
		#print(samples)
		
		#kmeansProcessor.computeCluster()
		print('----------------------FINISHING---------------------------')






