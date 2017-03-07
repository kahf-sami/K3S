from .dbModel import DbModel
from .utility import Utility
import sys
import math


class WordCloud(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'word_point'
		self.primaryKey = 'word_pointid'
		self.fields = ['word_pointid', 'wordid', 'label', 'x', 'y', 'r', 'theta']
		self.maxX = self.maxNumberOfSimilarBlocks()
		return


	def savePoints(self):
		limit = 500
		offset = 0
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
		data = {}
		data['wordid'] = word[0]
		data['label'] = word[1]
		data['x'] = self.maxX - math.ceil(word[4])
		data['y'] = math.ceil(self.localContextImportance(word[1]))
		print(data)
		self.save(data);
		return

	def localContextImportance(self, word):
		sql = ("SELECT AVG(weight) FROM local_context WHERE word = %s")
		params = []
		params.append(word);
		weight = self.mysql.query(sql, params)
		return weight[0][0]


	def getWordsByBatch(self, limit, offset = 0):
		sql = ("SELECT wordid, word, stemmed_word, count, number_of_blocks, tf_idf "
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




