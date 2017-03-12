from .dbModel import DbModel
from .edge import Edge
from .word import Word
from .context import Context
from .nlp import NLP
import sys
import re
from .utility import Utility
import math
from .localContext import LocalContext
from .coreWord import CoreWord
import ast
from .config import Config
from .file import File

class TextNodeCloud(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.config = Config()
		self.identifier = identifier
		self.tableName = 'text_point'
		self.primaryKey = 'text_pointid'
		self.fields = ['text_pointid', 'nodeid', 'label', 'x', 'y', 'r', 'theta']
		self.ignoreExists = ['theta', 'r', 'x', 'y', 'label']
		self.wordProcessor = Word(identifier)
		self.mainPath = File.join(self.config.ROOT_PATH, 'Web', self.identifier + '_text_node.csv')
		return



	def getRepresentativesByBatch(self, limit, offset = 0):
		sql = "SELECT nodeid, representatives FROM text_node ORDER BY nodeid LIMIT " + str(limit) + " OFFSET " + str(offset)
		return self.mysql.query(sql, [])


	def savePoints(self):
		limit = 500
		offset = 0

		self.mysql.truncate(self.tableName)
		representatives = self.getRepresentativesByBatch(limit, offset)
		total = len(representatives)

		while total:
			for representative in representatives:
				representativeList = ast.literal_eval(re.sub('\'', '"', str(representative[1])))

				self.calculateAndSavePoint(representativeList, representative[0])

			offset += total
			representstives = self.getRepresentativesByBatch(limit, offset)
			total = len(representatives)

		return


	def calculateAndSavePoint(self, representativeList, nodeid):
		if not representativeList:
			return None

		numberOfWords = 0
		sumX = 0
		sumY = 0
		label = ''
		divider = ''
		for word in representativeList:
			details = self.getWordDetails(word)
			sumX += details[0][1]
			sumY += details[0][0]
			numberOfWords += 1
			label += divider + word
			divider = ', '

		data = {}
		data['nodeid'] = nodeid
		data['label'] = label
		data['y'] = sumY / numberOfWords
		data['x'] = sumX / numberOfWords
		data['r'] = math.sqrt(float(data['x']) * float(data['x']) + float(data['y']) * float(data['y']))
		
		#print(data)
		
		self.save(data);
		return


	def generateLCCsv(self, representatives = None, filePath = None):
		limit = 500
		offset = 0
		points = self.getPointsByBatch(limit, offset)
		totalPoints = len(points)

		if filePath:
			file = File(filePath)
		else:
			file = File(self.mainPath)
		file.remove()

		while totalPoints:
			for point in totalPoints:
				if len(word[1]) < 2:
					continue

				data = {}
				data['nodeid'] = word[0]
				data['labe;'] = word[0]
				data['x'] = word[0]
				data['y'] = word[0]
				data['r'] = word[0]
				
				file.write(data)
			
			offset += totalWords
			points = self.getPointsByBatch(limit, offset)
			totalPoints = len(points)


	def getPointsByBatch(self, limit, offset = 0):
		sql = ("SELECT nodeid, label, x, y, r "
			"FROM text_point "
			"LIMIT " + str(limit) + " OFFSET " + str(offset))
		return self.mysql.query(sql, [])


	def getWordDetails(self, word):
		sql = ("SELECT number_of_blocks, local_avg "
			"FROM word "
			"WHERE word.word = %s")
		
		return self.mysql.query(sql, [word])
