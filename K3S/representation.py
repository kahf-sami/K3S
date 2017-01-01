from .config import Config
import numpy
import math
import matplotlib.pyplot as plot
import sys
import mpld3

class Representation():


	def __init__(self, identifier):
		self.config = Config()
		self.identifier = identifier
		self.figure = None
		self.labels = []
		self.radius = []
		self.theta = []
		self.color = []
		return

	def loadPolarData(self, matrix, wordVocab, assignedColors = None):
		totalDocumets = matrix.shape[0]
		totalWords = matrix.shape[1]

		totalMax = 0
		totalMin = -1
		for wordColumn in range(totalWords):
			wordScores = matrix.getcol(wordColumn).toarray()
			
			r = 0
			for row in range(wordScores.shape[0]):
				for column in range(wordScores.shape[1]):
					if r < wordScores[row][column]:
						r = wordScores[row][column]
			
			if r > totalMax:
				totalMax = r

			if (totalMin == -1) or (r < totalMin):
				totalMin = r
			self.labels.append(wordVocab[wordColumn])
			self.radius.append(r)
			self.theta.append(numpy.random.uniform(0, 360))


		colorGroups = [(1,0,0), (0,1,0), (0,0,1), (1,1,0), (0,1,1),(1,0,0),(0.5,0,0)]
		gap = (totalMax - totalMin) / 5
		index = 0
		for r in self.radius:
			if assignedColors:
				colorIndex = assignedColors[index]
			else:
				colorIndex = math.ceil(r / gap)
			self.color.append(colorGroups[colorIndex])
			index += 1


	def createPolar(self, matrix, wordVocab):
		self.loadPolarData(matrix, wordVocab)

		self.figure = plot.figure(figsize=(10, 10))
		self.axis = self.figure.add_subplot(111, projection='polar')
		self.axis.grid(color='white', linestyle='solid')
		self.axis.set_title("TF-IDF (with tooltips!)", size=20)
		graph = self.axis.scatter(self.theta, self.radius, c = self.color, cmap = plot.cm.hsv, picker = True)
		graph.set_alpha(0.5)

		#self.annotations = {}
		#for label, xe, ye in zip(self.labels, self.radius, self.theta):
		#	self.annotations[xe,ye] = self.axis.annotate(label, (xe,ye), visible=True) 

		self.figure.canvas.mpl_connect('pick_event', self.onPick)

		tooltip = mpld3.plugins.PointLabelTooltip(graph, labels = self.labels)
		mpld3.plugins.connect(self.figure, tooltip)

		return


	def kmeans(self, matrix, wordVocab, assignments):
		self.loadPolarData(matrix, wordVocab, assignments)
		self.figure = plot.figure(figsize=(10, 10))
		self.axis = self.figure.add_subplot(111, projection='polar')
		self.axis.grid(color='white', linestyle='solid')
		self.axis.set_title("KMeans using TF-IDF (with tooltips!)", size=20)
		graph = self.axis.scatter(self.theta, self.radius, c = self.color, cmap = plot.cm.hsv, picker = True)
		graph.set_alpha(0.5)

		self.figure.canvas.mpl_connect('pick_event', self.onPick)

		tooltip = mpld3.plugins.PointLabelTooltip(graph, labels = self.labels)
		mpld3.plugins.connect(self.figure, tooltip)

		return

	def show(slef):
		plot.show()
		return

	def showInBrowser(self):
		mpld3.show()
		return

	
	def onPick(self, event):
		thisline = event.artist
		data = thisline.get_offsets()
		index = event.ind
		#annotation = self.annotations[self.radius[index], self.theta[index]] 
		#if not annotation.get_visible(): 
		#	annotation.set_visible(True)
		#self.axis.figure.canvas.draw() 

		print('on pick line:', self.labels[index])
		return





