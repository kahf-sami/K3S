from .dbModel import DbModel
from .utility import Utility
from .config import Config
from .file import File
from .utility import Utility
import sys
import math


class WordCloud(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.config = Config()
		self.identifier = identifier
		self.tableName = 'word_point'
		self.primaryKey = 'word_pointid'
		self.fields = ['word_pointid', 'wordid', 'label', 'x', 'y', 'r', 'theta']
		self.maxX = self.maxNumberOfSimilarBlocks()
		self.mainPath = File.join(self.config.DATA_PATH, self.identifier + '.csv')
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


	def generateLGCsv(self):
		limit = 500
		offset = 0
		words = self.getPointsByBatch(limit, offset)
		totalWords = len(words)

		file = File(self.mainPath)
		file.remove()
		
		while totalWords:
			for word in words:
				data = {}
				data['word'] = word[0]
				data['local_avg_weight'] = word[1]
				data['global_docs'] = word[2]
				data['global_tf_idf'] = math.ceil(word[3])
				data['global_cluster'] = 1
				data['global_local'] = data['global_tf_idf'] + 2 * data['local_avg_weight']
				data['hash'] = Utility.getAsciiValue(word[0])
				#print(word)
				#self.getRelatedWords(word[0])
				
				file.write(data)

			offset += totalWords
			words = self.getPointsByBatch(limit, offset)
			totalWords = len(words)


	def getPointsByBatch(self, limit, offset = 0):
		sql = ("SELECT label, y as local_avg_weight, x as global_docs, tf_idf "
			"FROM word "
			"JOIN word_point ON word_point.wordid = word.wordid "
			"LIMIT " + str(limit) + " OFFSET " + str(offset))
		return self.mysql.query(sql, [])

	'''
	def getRelatedWords(self, word, min = 50):
		print(word)
		sql = ("SELECT lc.word FROM local_context as lc WHERE lc.nodeid IN (( select lc2.nodeid from local_context as lc2 where lc2.word = '" + word + "'))")
		words = self.mysql.query(sql, [])

		if not words:
			return None

		processedWords = {}
		for word in words:
			if word not in  processedWords.keys():
				processedWords[word] = 0

			processedWords[word] += 1

		finalProcessedWords = {}

		for word in processedWords.keys():
			if processedWords[word] > min:
				finalProcessedWords[word] = processedWords[word]


		print(finalProcessedWords)
		sys.exit()
		return finalProcessedWords

	'''

		

				




