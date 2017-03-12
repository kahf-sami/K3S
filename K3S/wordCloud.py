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
		return


	def savePoints(self):
		limit = 500
		offset = 0

		self.truncate(self.tableName)
		words = self.getWordsByBatch(limit, offset)
		totalWords = len(words)

		while totalWords:
			for word in words:
				self.calculateAndSavePoint(word)

			offset += totalWords
			words = self.getWordsByBatch(limit, offset)
			totalWords = totalWords = len(words)

		return


	def calculateAndSavePoint(self, word):
		wordProcessor = Word(self.identifier)
		localContextImportance = wordProcessor.saveLocalContextImportance(word)

		data = {}
		data['wordid'] = word[0]
		data['label'] = word[1]
		data['y'] = math.ceil(word[4])
		data['x'] = localContextImportance
		print(data)
		self.save(data);


	def getWordsByBatch(self, limit, offset = 0):
		sql = ("SELECT wordid, word, stemmed_word, count, number_of_blocks, tf_idf, local_avg, signature "
			"FROM word "
			"LIMIT " + str(limit) + " OFFSET " + str(offset))
		
		return self.mysql.query(sql, [])



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
		limit = 500
		offset = 0
		words = self.getWordsByBatch(limit, offset)
		totalWords = len(words)

		if filePath:
			file = File(filePath)
		else:
			file = File(self.mainPath)
		file.remove()

		while totalWords:
			for word in words:
				if len(word[1]) < 2:
					continue

				data = {}
				data['word'] = word[1]
				data['local_avg'] = word[6]
				data['global_docs'] = word[4]
				data['global_tf_idf'] = math.ceil(word[5])
				data['global_cluster'] = 1
				data['global_local'] = 2 * float(data['global_tf_idf'])  + 0.1 * float(data['local_avg'])
				data['signature'] = word[7]

				if representatives and (word[1] in representatives):
					data['global_cluster'] = 2

				#print(word)
				#self.getRelatedWords(word[0])
				
				file.write(data)
			
			offset += totalWords
			words = self.getWordsByBatch(limit, offset)
			totalWords = len(words)


	def buildTextNodeCloud(self, nodeid):
		representatives = self.getNodeRepresentative(nodeid)

		if not representatives:
			return

		pointsPath = File.join(self.config.ROOT_PATH, 'Web', self.identifier + '_' + str(nodeid) + '.csv')

		self.generateLCCsv(representatives, pointsPath)
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


	def getPointsByBatch(self, limit, offset = 0):
		sql = ("SELECT label, y as local_avg_weight, x as global_docs, tf_idf "
			"FROM word "
			"JOIN word_point ON word_point.wordid = word.wordid "
			"LIMIT " + str(limit) + " OFFSET " + str(offset))
		return self.mysql.query(sql, [])

		

				




