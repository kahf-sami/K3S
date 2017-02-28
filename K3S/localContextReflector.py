from .file import File
from .config import Config
import numpy as np
import matplotlib.pyplot as plot
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.cm as cmx
import matplotlib.colors as colors
from nltk import word_tokenize
import sys
import math


class LocalContextReflector():


	def __init__(self, identifier):
		self.config = Config()
		self.identifier = identifier
		self.path = File.join(self.config.DATA_PATH, self.identifier, 'local-context-reflector')
		return


	def create(self, x, y, colors, nodes, contextPolygons = None, contextColors = None, fileName = None):
		plot.cla() # Clear the figure

		self.figure = plot.figure(figsize=(200, 200))
		self.axis = self.figure.add_subplot(111)
		self.axis.grid(color='white', linestyle='solid')
		graph = self.axis.scatter(x, y, c = colors, marker='o', s=50)
		
		for node in nodes:
			if nodes[node]['x'] < 0:
				horizontalalignment = 'right'
			else:
				horizontalalignment = 'left'
			if nodes[node]['y'] < 0:
				verticalalignment = 'down'
			else:
				verticalalignment = 'top'
			
			self.axis.annotate(nodes[node]['label'], (nodes[node]['x'], nodes[node]['y']), color='black', horizontalalignment=horizontalalignment, verticalalignment=verticalalignment)

		'''
		index = 0
		for polygon in contextPolygons:
			totalPoints = len(polygon)
			firstPoint = True
			codes = []
			
			if totalPoints == 1:
				continue

			for point in polygon:
				if firstPoint:
					codes.append(Path.MOVETO)
					firstPoint = False
				elif polygon == totalPoints - 1:
					#lastPoint
					codes.append(Path.CLOSEPOLY)
					firstPoint = True
				else:
					codes.append(Path.LINETO)

			#path = Path(polygon, codes)
			#patch = patches.PathPatch(path, color=contextColors[index], alpha=0.2)
			#self.axis.add_patch(patch)
			index += 1
			'''


		#plot.show()

		#self.figure.savefig(File.join(self.path, fileName + '.png'))
		plot.show()
		return



