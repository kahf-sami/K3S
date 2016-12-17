import os
from .config import Config
from .directory import Directory
from .file import File
from .log import Log
from .toText import ToText


class Processor():


	def __init__(self, sourceIdentifier):
		self.config = Config()
		self.log = Log()
		self.mainPath = File.join(self.config.DATA_PATH, sourceIdentifier)
		self.rawPath = File.join(self.mainPath, 'raw')
		self.processedPath = File.join(self.mainPath, 'processed')
		self.graphsPath = File.join(self.mainPath, 'graphs')
		self.sourceIdentifier = sourceIdentifier
		


	def clean(self):
		directory = Directory(self.mainPath)
		directory.remove()


	def createSourceSetup(self):
		directory = Directory(self.rawPath)
		directory.create()

		processedDir = Directory(self.processedPath)
		processedDir.create()

		graphDir = Directory(self.graphsPath)
		processedDir.create()


	def copy(self, sourcePath, destinationPath = None):
		sourcefile = File(sourcePath)
		if not destinationPath:
			destinationPath = File.join(self.rawPath, sourcefile.getFileName())
		File.copy(sourcePath, destinationPath)


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




