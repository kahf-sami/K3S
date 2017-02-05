from .dbModel import DbModel
from nltk import word_tokenize
from nltk import pos_tag
from .utility import Utility
import sys
from nltk.stem.porter import PorterStemmer
from .nlp import NLP
import math



class Word(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.tableName = 'word'
		self.primaryKey = 'wordid'
		self.fields = ['wordid', 'contextid', 'word', 'count', 'number_of_blocks', 'tf_idf', 'stemmed_word']
		self.ignoreExists = ['count', 'number_of_blocks', 'tf_idf']
		self.stemmer = PorterStemmer()
		self.nlpProcessor = NLP()
		return


	def save(self, data):
		itemid = None
		item = self.read(data)

		if not item:
			data['number_of_blocks'] = 1
			itemid = self.insert(data)
		else:
			itemid = item[0][0]
			data['number_of_blocks'] = int(item[0][4]) + 1
			data['count'] += int(item[0][3])
			self.update(data, itemid)
				
		return itemid


	"""
	ADJ	adjective
	ADP	adposition
	ADV	adverb
	CONJ conjunction
	DET	determiner
	NOUN noun
	NUM	numeral	
	PRT	particle
	PRON pronoun
	VERB verb
	"""
	def saveWords(self, textBlock, words = None, onlyNoun = True):
		actualWords = self.getWords(textBlock, False)

		if not words:
			if onlyNoun: 
				words = self.getNouns(textBlock)
			else:
				words = actualWords

		totals = {}
		for word in actualWords:
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
		limit = 10
		offset = 0
		words = self.getWordsByBatch(limit, offset)
		totalWords = self.getTotalWords()
		totalTextBlocks = self.getTotalTextBlocks()

		while len(words):
			for word in words:
				tf = int(word[2]) / int(totalWords[0][0])
				idf = math.log(int(totalTextBlocks[0][0]) / (1 + int(word[3])))
				data = {}
				data['wordid'] = word[0]
				data['tf_idf'] = tf * idf
				self.update(data, int(word[0]))

			offset += limit 
			words = self.getWordsByBatch(limit, offset)
		return


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


	def addEdges(self, truncate = True):
		if truncate:
			self.mysql.truncate('word_edge')
			
		limit = 1000
		offset = 0
		words = self.getWordsByBatch(limit, offset)

		while len(words):
			for word in words:
				relatedWords = self.getRelatedWords(word[1])
				if relatedWords:
					for relatedWord in relatedWords:
						data = {}
						data['source_wordid'] = word[0]
						data['destination_wordid'] = relatedWord['wordid']
						data['similaruty_score'] = relatedWord['similarity_score']
						self.saveEdge(data)

			offset += limit 
			words = self.getWordsByBatch(limit, offset)

		return


	def saveEdge(self, data):
		wordEdgeId = self.hasEdge(data)

		if not wordEdgeId:
			sql = 'INSERT INTO word_edge (source_wordid, destination_wordid, similaruty_score) VALUES (%s, %s, %s)'
			params = []
			params.append(data['source_wordid'])
			params.append(data['destination_wordid'])
			params.append(data['similaruty_score'])
			wordEdgeId = self.mysql.insert(sql, params)
			
		return wordEdgeId


	def hasEdge(self, data):
		params = []
		sql = "SELECT word_edgeid FROM word_edge WHERE "

		where1 = ''
		where2 = ''
		joinRequired = False
		keys = data.keys()
		if 'source_wordid' in keys:
			where1 += 'source_wordid = %s'
			where2 += 'destination_wordid = %s'
			params.append(data['source_wordid'])
			joinRequired = True

		if 'destination_wordid' in keys:
			if joinRequired:
				where1 += ' AND '
				where2 += ' AND '

			where1 += 'destination_wordid = %s'
			where2 += 'source_wordid = %s'
			params.append(data['destination_wordid'])

		sql += '(' + where1 + ') OR (' + where2 + ')'

		return self.mysql.query(sql, params + params)


	def getWordsByBatch(self, limit, offset = 0):
		sql = "SELECT wordid, word.word,count,number_of_blocks  FROM word ORDER BY wordid LIMIT " + str(limit) + " OFFSET " + str(offset)
		return self.mysql.query(sql, [])


	def getRelatedWords(self, word, minAllowedSimilarityPercent = 50):
		textBlocks = self.getTextNodesHavingWord(word)

		if not textBlocks:
			return None

		mostSimilarWord = ''
		keys = []
		otherWords = {}
		totalNumberOfDocsWordAppear = len(textBlocks)
		maxSimilarity = 0
		for textBlock in textBlocks:
			thisBlockWords = Utility.unique(self.getNouns(textBlock[0]))
			if thisBlockWords:
				for otherWord in thisBlockWords:
					if word == otherWord:
						continue
					if otherWord in keys:
						otherWords[otherWord] += 1
						if otherWords[otherWord] > maxSimilarity:
							maxSimilarity = otherWords[otherWord]
							mostSimilarWord = otherWord
					else:
						keys.append(otherWord)
						otherWords[otherWord] = 1

		if not otherWords:
			return None

		maxSimilarityPercent = (maxSimilarity / totalNumberOfDocsWordAppear * 100)

		if maxSimilarityPercent < minAllowedSimilarityPercent:
			return None
		
		relatetedWords = []

		for otherWord in otherWords:
			similarityPercent = (otherWords[otherWord] / totalNumberOfDocsWordAppear * 100)
			if similarityPercent < minAllowedSimilarityPercent:
				continue;
			data = {}
			data['word'] = otherWord
			data['wordid'] = self.getWordId(otherWord)
			data['similarity_score'] = similarityPercent
			relatetedWords.append(data)
		
		return relatetedWords

			
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


	def getTotalTextBlocks(self):
		sql = "SELECT count(*) FROM text_node"

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


	def getEdges(self, wordId):
		sql = ("SELECT word.wordid, word.word, similaruty_score "
			"FROM word_edge "
			"JOIN word ON destination_wordid = word.wordid "
			"WHERE source_wordid = %s "
			"ORDER BY similaruty_score")

		params = []
		params.append(wordId)
		return self.mysql.query(sql, params)


	def getRelatedWordsForGraph(self, word):
		sql = ("SELECT source_wordid, source_word.word, destination_wordid, destination_word.word, similaruty_score "
			"FROM word_edge "
			"JOIN word AS source_word ON source_word.wordid = source_wordid "
			"JOIN word AS destination_word ON destination_word.wordid = destination_wordid "
			"WHERE (source_word.word = %s or destination_word.word = %s) "
			"ORDER BY similaruty_score");

		params = []
		params.append(word)
		params.append(word)

		return self.mysql.query(sql, params)

