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

class Image():

	BLOCK_WIDTH = 0.1


	BLOCK_HEIGHT = 0.1


	scalerColorMap = None


	def __init__(self, identifier, totalBlocksPerWidth = 10, totalBlocksPerHeight = 80):
		self.config = Config()
		self.identifier = identifier
		self.path = File.join(self.config.DATA_PATH, self.identifier, 'graphs')
		self.numberOfGroups = 5
		self.setDimension(totalBlocksPerWidth, totalBlocksPerHeight)
		self.setGroups(self.numberOfGroups);
		self.labels = []
		self.x = []
		self.y = []
		self.color = []
		self.totalMax = 0
		self.totalMin = -1
		self.gap = 0
		self.matrix = None
		self.wordVocab = None
		return


	def setDimension(self, totalBlocksPerWidth, totalBlocksPerHeight):
		self.width = totalBlocksPerWidth * self.BLOCK_WIDTH
		self.height = totalBlocksPerHeight * self.BLOCK_HEIGHT
		self.figure = plot.figure(figsize=(self.width, self.height))
		return


	def getColor(self, index):
		if (not self.scalerColorMap):
			return None
		return self.scalerColorMap.to_rgba(index)


	def setGroups(self, numberOfGroups):
		self.numberOfGroups = numberOfGroups
		colorNorm  = colors.Normalize(vmin=0, vmax=numberOfGroups)
		self.scalerColorMap = cmx.ScalarMappable(norm=colorNorm, cmap='hsv') 
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
		axis = self.figure.add_subplot(111, aspect="equal")

		x = 0
		y = self.height - self.BLOCK_HEIGHT
		blockWords = word_tokenize(textBlock)
		for blockWord in blockWords:
			wordIndex = self.wordVocab[blockWord]
			tfIdfValue = self.matrix[documentNumber][wordIndex]
			color = self.getColor(math.ceil(tfIdfValue % self.gap))
			block = patches.Rectangle((x,y), self.BLOCK_WIDTH, self.BLOCK_HEIGHT, facecolor=color)
			axis.add_patch(block)

			x += self.BLOCK_WIDTH
			if x > self.width:
				x = 0
			y -= self.BLOCK_HEIGHT
			if y < 0:
				y = self.height - self.BLOCK_HEIGHT


		#figure.savefig(File.join(self.path, fileName))
		plot.show()
		return


