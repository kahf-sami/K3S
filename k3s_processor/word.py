from .dbModel import DbModel
from k3s_utility.utility import Utility
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize, pos_tag
import ast

class Word(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.tableName = 'word'
		self.primaryKey = 'wordid'
		self.fields = ['wordid', 'contextid', 'word', 'count', 'number_of_blocks', 'tf_idf', 'stemmed_word', 'signature','local_avg', 'zone']
		self.ignoreExists = ['count', 'number_of_blocks', 'tf_idf', 'word', 'zone']
		self.stemmer = PorterStemmer()
		self.maxZone = 6
		return


	def save(self, data):
		itemid = None
		item = self.read(data)
		#totalTextBlocks = self.getTotalTextBlocks()

		if not item:
			# new text node
			#totalTextBlocks += 1
			data['number_of_blocks'] = 1
			itemid = self.insert(data)
			#data['zone'] = self.getZone(data['number_of_blocks'], totalTextBlocks)
		else:
			itemid = item[0][0]
			data['word'] = item[0][1]
			data['number_of_blocks'] = int(item[0][4]) + 1
			#data['zone'] = self.getZone(data['number_of_blocks'], totalTextBlocks)
			
			if 'count' in data.keys():
				data['count'] += int(item[0][3])
			
			self.update(data, itemid)
				
		return itemid


	def saveWords(self, words = None):
		totals = {}
		for word in words:
			stemmedWord = self.stemmer.stem(word)
			if stemmedWord in totals.keys():
				totals[stemmedWord] += 1
			else:
				totals[stemmedWord] = 1
		
		if len(totals):
			for word in words:
				data = {}
				data['word'] = word
				data['stemmed_word'] = self.stemmer.stem(word)
				keys = totals.keys()
				if data['stemmed_word'] in keys:
					data['count'] = totals[data['stemmed_word']]
				elif word in keys:
					data['count'] = totals[word]
				else:
					parts =  data['word'].split('_')
					if parts[0] in keys:
						data['count'] = totals[parts[0]]
					else:	
						data['count'] = 1
				
				self.save(data)

		return words


	def calculateTfIdf(self):
		totalWords = self.getTotalWords()

		totalTextBlocks = self.getTotalTextBlocks()

		cursor = self.getWordsByBatch()

		for word in cursor:
			tf = int(word[2]) / int(totalWords[0][0])
			idf = math.log(int(totalTextBlocks) / (1 + int(word[3])))
			data = {}
			data['wordid'] = word[0]
			data['tf_idf'] = "{0:.2f}".format(tf * idf * 10)
			self.update(data, int(word[0]))
			
		return


	def calculateZone(self):
		totalWords = self.getTotalWords()
		totalTextBlocks = self.getTotalTextBlocks()
		cursor = self.getWordsByBatch()

		for word in cursor:
			data = {}
			data['wordid'] = word[0]
			data['zone'] = self.getZone(word[3], totalTextBlocks)
			
			self.update(data, int(word[0]))

		return


	def getZone(self, numberOfBlocks, totalTextBlocks):
		if not numberOfBlocks or not totalTextBlocks:
			return 0

		percentageOfNumberOfBlocks = (int(numberOfBlocks) * 100) / totalTextBlocks

		if percentageOfNumberOfBlocks >= 40:
			return 1

		if percentageOfNumberOfBlocks <= 0.10: 
			return 19

		if percentageOfNumberOfBlocks <= 0.20: 
			return 18

		if percentageOfNumberOfBlocks <= 0.30: 
			return 17

		if percentageOfNumberOfBlocks <= 0.40: 
			return 16

		if percentageOfNumberOfBlocks <= 0.50: 
			return 15

		if percentageOfNumberOfBlocks <= 0.60: 
			return 14

		if percentageOfNumberOfBlocks <= 0.70: 
			return 13

		if percentageOfNumberOfBlocks <= 0.80: 
			return 12

		if percentageOfNumberOfBlocks <= 0.90: 
			return 11

		if percentageOfNumberOfBlocks <= 1: 
			return 10

		if percentageOfNumberOfBlocks <= 2: 
			return 9

		if percentageOfNumberOfBlocks <= 3: 
			return 8

		if percentageOfNumberOfBlocks <= 4: 
			return 7
		
		if percentageOfNumberOfBlocks <= 5: 
			return 6
		
		if percentageOfNumberOfBlocks <= 10: 
			return 5
		
		if percentageOfNumberOfBlocks <= 15: 
			return 4
		
		if percentageOfNumberOfBlocks <= 20: 
			return 3
			
		return 2


	def calculateLocalContextImportance(self):
		totalWords = self.getTotalWords()
		totalTextBlocks = self.getTotalTextBlocks()

		cursor = self.getWordsByBatch()

		for word in cursor:
			data = {}
			data['wordid'] = word[0]
			data['local_avg'] = "{0:.2f}".format(self.localContextImportance(word[4]))
			#print(data)
			self.update(data, word[0])

		return


	def saveLocalContextImportance(self, word):
		data = {}
		data['word'] = word
		data['local_avg'] = "{0:.2f}".format(self.localContextImportance(word))
		self.save(data)
		return


	def localContextImportance(self, word):
		sql = ("SELECT weight, representatives "
			"FROM local_context "
			"JOIN text_node ON text_node.nodeid = local_context.nodeid "
			"WHERE local_context.word = %s")

		results = self.mysql.query(sql, [word])

		weight = 0

		if not results:
			return weight

		for row in results:
			representativeList = ast.literal_eval(re.sub('\'', '"', str(row[1])))
			itemWeight = row[0] / len(representativeList) * 100
			weight += itemWeight

		return weight


	def getAsciiSum(self, words):
		words = Utility.unique(words)
		wordsString = ''.join(words)
		
		asciiSum = 0
		for char in wordsString:
			asciiSum += ord(char)

		return asciiSum


	def getWordsDetails(self, words):
		sql = "SELECT word.word, word.number_of_blocks, word.count FROM word WHERE number_of_blocks > 1 AND word.word IN (";
		params = []

		joinRequired = False
		for word in words:
			if joinRequired:
				sql += ','
			sql += '%s'
			params.append(word)
			joinRequired = True

		sql += ") ORDER BY word.number_of_blocks"
		results = self.mysql.query(sql, params)
		return results
		

	def getNouns(self, textBlock):
		return self.getWordsByType(textBlock, 'NN')



	def getWordsByType(self, textBlock, type = None):
		afterPartsOfSpeachTagging = self.getWords(textBlock, True)
		
		if not type:
			return afterPartsOfSpeachTagging

		words = []
		for item in afterPartsOfSpeachTagging:
			word = item[0]
			wordType = item[1]

			if wordType == type:
				words.append(word)

		return words


	def getWords(self, textBlock, tagPartsOfSpeach = False):
		words = word_tokenize(textBlock)
		if not tagPartsOfSpeach:
			return words
		return pos_tag(words)


	def getWordsByBatch(self):
		sql = "SELECT wordid, word.word,count,number_of_blocks,stemmed_word FROM word "
		return self.mysql.query(sql, [], True)


	def getGlobalContributionDetails(self, word):
		sql = "SELECT number_of_blocks, zone, tf_idf FROM word WHERE word.stemmed_word = %s"

		params = []
		params.append(word)
		result = self.mysql.query(sql, params)

		if not result:
			return None
			
		return result[0]

			
	def getWordId(self, word):
		sql = "SELECT wordid FROM word WHERE word.word = %s"

		params = []
		params.append(word)
		result = self.mysql.query(sql, params)

		if not result:
			return 0

		return result[0][0]


	def getTotalWords(self):
		sql = "SELECT count(*) FROM word"

		params = []
		return self.mysql.query(sql, params)


	def getTextNodesHavingWord(self, word):
		sql = "SELECT text_block FROM text_node WHERE text_block LIKe %s ORDER BY nodeid"

		params = []
		params.append('%' + word + '%')
		return self.mysql.query(sql, params)


	def getAllWords(self):
		sql = ("SELECT wordid, word, count, number_of_blocks "
			"FROM word "
			"ORDER BY number_of_blocks DESC, count ASC")

		return self.mysql.query(sql, [])


