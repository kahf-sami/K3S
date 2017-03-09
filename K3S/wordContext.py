from .dbModel import DbModel
from .utility import Utility
from .config import Config
from .file import File
from .utility import Utility
import sys
import math
import ast
import re


class WordContext(DbModel):


	def __init__(self, identifier, word):
		DbModel.__init__(self, identifier)
		self.config = Config()
		self.identifier = identifier
		self.word = word
		self.mainPath = File.join(self.config.ROOT_PATH, 'Web', self.identifier + '_' + word +  '.csv')
		self.minOcc = None
		self.maxOcc = None
		self.totalDocs = None
		return


	def generateLGCsv(self):
		file = File(self.mainPath)
		file.remove()
		
		finalAssociated = self.getAsociatedWords()

		if not finalAssociated:
			return

		for item in finalAssociated.keys():
			details = self.getWordDetails(item)
			data = {}
			data['word'] = item
			data['distance'] = finalAssociated[item]
			data['global_tfidf'] = details[0][0]
			data['cluster'] = 1
			data['number_of_docs'] = details[0][1]

			file.write(data)

		return



	def getWordDetails(self, word):
		sql = ("SELECT tf_idf, number_of_blocks "
			"FROM word "
			"WHERE word = %s")
		result = self.mysql.query(sql, [word])

		if not result:
			return 0

		return result


	def getAsociatedWords(self, minAllowedPercent = 10):
		representatives = self.getContextRepresentatives()

		if not representatives:
			return None

		self.totalDocs = len(representatives)
		associatedWords = {}
		for representative in representatives:
			representativeList = ast.literal_eval(re.sub('\'', '"', str(representative[0])))

			for item in representativeList:
				if item not in associatedWords.keys():
					associatedWords[item] = 0;

				associatedWords[item] += 1

				if not self.minOcc or (self.minOcc > associatedWords[item]):
					self.minOcc  = associatedWords[item]

				if not self.maxOcc or (self.maxOcc < associatedWords[item]):
					self.maxOcc  = associatedWords[item]


		minAllowed = self.totalDocs * minAllowedPercent / 100
		finalAssociated = {}

		for item in associatedWords.keys():
			if associatedWords[item] >= minAllowed:
				finalAssociated[item] =  associatedWords[item]

		return finalAssociated



	def getContextRepresentatives(self):
		sql = ("SELECT representatives "
			"FROM text_node "
			"WHERE representatives LIKE '%" + self.word + "%'")
		return self.mysql.query(sql, [])

		

				




