from .file import File
from .config import Config
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import matplotlib.cm as cmx
import matplotlib.colors as colors
from nltk import word_tokenize
import sys
import math


class LocalContextHighlighter():


	BLOCK_WIDTH = 1


	BLOCK_HEIGHT = 0.5


	def __init__(self, identifier, totalBlocksPerWidth = 10, totalBlocksPerHeight = 50):
		self.config = Config()
		self.identifier = identifier
		self.path = File.join(self.config.DATA_PATH, self.identifier, 'local-context')
		self.numberOfGroups = 5
		self.setDimension(totalBlocksPerWidth, totalBlocksPerHeight)
		self.totalMax = 0
		self.totalMin = -1
		self.gap = 0
		self.matrix = None
		self.wordVocab = None
		self.axis = None
		self.showText = False
		self.localContexts = []
		self.localContextWords = []
		self.localContextsColorsMap = ['#F2D7D5', '#FDEDEC', '#EBDEF0', '#E8DAEF', '#D4E6F1', '#D6EAF8', 
			'#D1F2EB', '#D0ECE7', '#D4EFDF', '#D5F5E3', '#FCF3CF', '#FDEBD0', '#FAE5D3', '#F6DDCC',
			'#F6DDCC']
		self.localContextsColor = []
		return


	def setDimension(self, totalBlocksPerWidth, totalBlocksPerHeight):
		self.width = totalBlocksPerWidth * self.BLOCK_WIDTH
		self.height = totalBlocksPerHeight * self.BLOCK_HEIGHT
		self.figure = plot.figure(figsize=(self.width, self.height))
		plot.axis((0, self.width, 0, self.height))
		return

	def setLocalContexts(self, localContexts):
		self.localContexts = localContexts

		self.localContextWords = []
		index = 0
		totalColors = len(self.localContextsColorsMap)
		for localContext in localContexts:
			self.localContextWords += localContext
			if index > (totalColors - 1):
				colorIndex = index % totalColors
			else:
				colorIndex = index
			self.localContextsColor.append(self.localContextsColorsMap[colorIndex])
			index += 1

		self.localContextWords = list(set(self.localContextWords))
		return


	def getContextColors(self, blockWord):
		blockWord = blockWord.lower()

		if not self.localContextWords:
			return 'white'

		if blockWord not in self.localContextWords:
			return 'white'

		index = 0
		for localContext in self.localContexts:
			if blockWord in localContext:
				return self.localContextsColor[index]
			index += 1

		return 'white'


	def getColor(self, index):
		colors = ['#d3d3d3','#87ceeb','#1e90ff','#4169e1', '#0000cd','#000080']
		if index > (len(colors) - 1):
			index = len(colors) % index
		return colors[index]


	def renderText(self):
		self.showText = True
		return



	def loadTfIdf(self, matrix, wordVocab):
		totalDocumets = matrix.shape[0]
		totalWords = matrix.shape[1]
		self.matrix = matrix.toarray()
		self.wordVocab = wordVocab
		
		self.totalMax = 0
		self.totalMin = -1

		for row in range(totalDocumets):
			for column in range(totalWords):
				tfIdfValue = self.matrix[row][column]
					
				if tfIdfValue > self.totalMax:
					self.totalMax = tfIdfValue

				if (self.totalMin == -1) or (tfIdfValue < self.totalMin):
					self.totalMin = tfIdfValue

		self.gap = (self.totalMax - self.totalMin) / self.numberOfGroups
		return


	def create(self, documentNumber, fileName, textBlock):
		plot.cla() # Clear the figure
		self.axis = self.figure.add_subplot(111)
		#self.fillGray()

		blockWords = word_tokenize(textBlock)

		x = 0
		y = self.height - self.BLOCK_HEIGHT
		
		wordsInVocab = self.wordVocab.keys()
		for blockWord in blockWords:
			blockWord = blockWord.lower()
			if blockWord in wordsInVocab:
				wordIndex = self.wordVocab[blockWord]
				tfIdfValue = self.matrix[documentNumber][wordIndex]
			else:
				tfIdfValue = 0

			colorGroup = math.ceil(tfIdfValue / self.gap)
			color = self.getColor(colorGroup)

			faceColor = self.getContextColors(blockWord)
			
			block = patches.Rectangle((x,y), self.BLOCK_WIDTH, self.BLOCK_HEIGHT, facecolor=faceColor, edgecolor=color)
			self.axis.add_patch(block)
			if self.showText:
				self.axis.text(x, y, blockWord, fontsize=10)

			x += self.BLOCK_WIDTH
			x = round(x, 1)
			if x >= (self.width):
				x = 0
				y -= self.BLOCK_HEIGHT
				y = round(y, 1)
				if y <= 0:
					y = self.height - self.BLOCK_HEIGHT


		fileNameParts = fileName.split(".")	
	
		self.figure.savefig(File.join(self.path, fileNameParts[0] + '.png'))
		#plot.show()
		return

	def fillGray(self):
		for x in range(int(self.width - self.BLOCK_WIDTH)):
			for y in range(int(self.height - self.BLOCK_HEIGHT)):
				block = patches.Rectangle((x,y), self.BLOCK_WIDTH, self.BLOCK_HEIGHT, facecolor=(1,0,0), edgecolor='None')
				self.axis.add_patch(block)
		return


