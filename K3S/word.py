from .dbModel import DbModel
from nltk import word_tokenize
from nltk import pos_tag
import sys


class Word(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.tableName = 'word'
		self.primaryKey = 'wordid'
		self.fields = ['wordid', 'contextid', 'word', 'count', 'number_of_blocks', 'tf_idf']
		self.ignoreExists = ['count', 'number_of_blocks', 'tf_idf']
		return


	def save(self, data):
		itemid = None
		item = self.read(data)

		if not item:
			data['number_of_blocks'] = 1
			itemid = self.insert(data)
		else:
			itemid = item[0][0]
			data['number_of_blocks'] = item[0][4] + 1
			data['count'] += item[0][3]
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
	def saveWords(self, textBlock, onlyNoun = True):
		if onlyNoun:
			words = self.getNouns(textBlock)
		else:
			words = getWords(self, textBlock)

		keys = []
		totals = {}
		for item in words:
			keys.append(word)
			
			if word in keys:
				totals[word] += 1
			else:
				totals[word] = 1
			
		if len(totals):
			for word in totals:
				data = {}
				data['word'] = word
				data['count'] = totals[word]
				self.save(data)

		return words


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
		return pos_tag(words)