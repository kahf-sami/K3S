from .dbModel import DbModel
from .utility import Utility
from .config import Config
from .file import File
from .utility import Utility
import sys
import math
from .word import Word
import ast
import re
import numpy


class WordCloud(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.config = Config()
		self.identifier = identifier
		self.tableName = 'word_point'
		self.primaryKey = 'word_pointid'
		self.fields = ['word_pointid', 'wordid', 'label', 'x', 'y', 'r', 'theta']
		self.maxX = self.maxNumberOfSimilarBlocks()
		self.mainPath = File.join(self.config.ROOT_PATH, 'Web', self.identifier + '_all.csv')
		self.radius = self.calculateRadius()
		self.thetaIncrementPerZone = {}		
		self.radiusIncrementFactor = 10
		self.thetaIncrementFactorPerZone = {}
		self.loadThetaIncrementFactor()
		print(self.mainPath)
		return


	def calculateRadius(self):
		totalTextNodes = self.getTotalTextNodes();
		if not totalTextNodes:
			return 0

		# The radius of a circle is number of nodes
		radius = math.ceil(totalTextNodes * 7 / 44)
		return radius


	def savePoints(self):
		self.mysql.truncate(self.tableName)
		cursor = self.getWordsByBatch()

		for word in cursor:
			self.calculateAndSavePoint(word)

		return


	def calculateAndSavePoint(self, word):
		wordProcessor = Word(self.identifier)
		#localContextImportance = wordProcessor.localContextImportance(word[1])

		zone =  word[8]
		if not zone in self.thetaIncrementPerZone.keys():
			self.thetaIncrementPerZone[zone] = 0
		else:
			self.thetaIncrementPerZone[zone] += self.thetaIncrementFactorPerZone[zone]

		data = {}
		data['wordid'] = word[0]
		data['label'] = word[1]
		data['r'] = self.radiusIncrementFactor * zone
		data['theta'] = self.thetaIncrementPerZone[zone]
		data['x'] = data['r'] * numpy.cos(numpy.deg2rad(data['theta']))
		data['y'] = data['r'] * numpy.sin(numpy.deg2rad(data['theta']))

		self.save(data);


	def getWordsByBatch(self):
		sql = ("SELECT wordid, word, stemmed_word, count, number_of_blocks, tf_idf, local_avg, signature, zone "
			"FROM word ORDER BY zone, wordid")
		
		return self.mysql.query(sql, [], True)



	def getPoint(self, word):
		sql = "SELECT word_pointid FROM word_point WHERE label = %s"

		params = []
		params.append(word);
		return self.mysql.query(sql, params)


	def maxNumberOfSimilarBlocks(self):
		sql = ("SELECT MAX(number_of_blocks) FROM word ")
		result = self.mysql.query(sql, [])
		return result[0][0]


	def generateLCCsv(self, representatives = None, filePath = None):
		cursor = self.getPointsByBatch()

		if filePath:
			file = File(filePath)
		else:
			file = File(self.mainPath)
		file.remove()

		for batch in cursor:
			words = [item for item in cursor.fetchall()]
			for word in words:
				if len(word[1]) < 2 or word[4] == 1:
					continue

				data = {}
				data['word'] = word[1]
				data['local_avg'] = word[6]
				data['global_docs'] = word[4]
				data['global_tf_idf'] = math.ceil(word[5])
				data['global_cluster'] = 'zone' + str(word[8])
				data['global_local'] = 2 * float(data['global_tf_idf'])  + 0.1 * float(data['local_avg'])
				data['signature'] = word[7]
				data['x'] = word[9]
				data['y'] = word[10]
				data['r'] = word[11]
				data['theta'] = word[12]

				if representatives and (word[1] in representatives):
					data['global_cluster'] = 2

				#print(word)
				#self.getRelatedWords(word[0])
				
				file.write(data)
			


	def buildTextNodeCloud(self, nodeid):
		representatives = self.getNodeRepresentative(nodeid)

		if not representatives:
			return

		pointsPath = File.join(self.config.ROOT_PATH, 'Web', self.identifier + '_' + str(nodeid) + '.csv')

		self.generateLCCsv(representatives, pointsPath)
		return

	
	def loadThetaIncrementFactor(self):
		self.thetaIncrementFactorPerZone = {}

		zones = self.getZones()

		if not zones:
			return

		for zone in zones:
			if zone[0] == 0:
				self.thetaIncrementFactorPerZone[zone[1]] = 0
			else:
				self.thetaIncrementFactorPerZone[zone[1]] = 360 / zone[0]
		return


	def getWordDetails(self, word):
		sql = ("SELECT wordid, word, stemmed_word, count, number_of_blocks, tf_idf, local_avg, signature "
			"FROM word "
			"WHERE word.word = %s")
		
		return self.mysql.query(sql, [word])



	def getNodeRepresentative(self, nodeid):
		sql = ("SELECT representatives "
			"FROM text_node "
			"WHERE nodeid = %s")
		result = self.mysql.query(sql, [nodeid])

		if result[0][0]:
			return ast.literal_eval(re.sub('\'', '"', str(result[0][0])))

		return None


	def getPointsByBatch(self):
		sql = ("SELECT word.wordid, word.word, stemmed_word, count, number_of_blocks, tf_idf, local_avg, signature, zone, x, y, r, theta "
			"FROM word "
			"JOIN word_point ON word.wordid=word_point.wordid "
			"ORDER BY zone, wordid")
		
		return self.mysql.query(sql, [], True)

		sql = ("SELECT label, y as local_avg_weight, x as global_docs, tf_idf "
			"FROM word "
			"JOIN word_point ON word_point.wordid = word.wordid ")
		return self.mysql.query(sql, [], True)


	def getTotalTextNodes(self):
		sql = ("SELECT count(*) "
			"FROM text_node ")
		result = self.mysql.query(sql, [])
		return result[0][0]


	def getZones(self):
		sql = ("SELECT count(wordid), zone "
			"FROM word "
			"GROUP BY zone")
		result = self.mysql.query(sql, [])
		
		return result

				




