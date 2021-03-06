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

		currentWordDetails = self.getWordDetails(self.word)
		maxAllowed = currentWordDetails[0][1] # max number of time current word appears

		for item in finalAssociated.keys():
			if item == self.word:
				details = currentWordDetails
			else:
				details = self.getWordDetails(item)

			if details[0][1] > maxAllowed:
				# More common word than the current word
				continue


			data = {}
			data['word'] = item
			data['local_distance'] = 100 - math.ceil(finalAssociated[item] / details[0][1] * 100)
			data['global_tfidf'] = details[0][0]
			data['global_nimber_of_blocks'] = details[0][1]
			data['cluster'] = 1
			data['global_distance'] = maxAllowed - details[0][1]
			data['radious'] = math.sqrt(data['local_distance'] * data['local_distance'] + data['global_distance'] * data['global_distance'])

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


	def getAsociatedWords(self, minAllowedPercent = 0):
		representatives = self.getContextRepresentatives()

		if not representatives:
			return None

		self.totalDocs = len(representatives)

		associatedWords = {}
		for representative in representatives:
			#print(representative)
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
		maxAllowed = associatedWords[self.word] + math.ceil(associatedWords[self.word] * minAllowedPercent /100)

		finalAssociated = {}

		for item in associatedWords.keys():
			if (associatedWords[item] >= minAllowed) and (associatedWords[item] <= maxAllowed):
				finalAssociated[item] =  associatedWords[item]

		return finalAssociated



	def getContextRepresentatives(self):
		sql = ("SELECT representatives "
			"FROM text_node "
			"WHERE representatives LIKE \"%\'" + self.word + "\'%\"")
		return self.mysql.query(sql, [])

		

				




