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
	def saveWords(self, textBlock):
		words = word_tokenize(textBlock)
		afterPartsOfSpeachTagging = pos_tag(words)

		totals = {}
		for item in afterPartsOfSpeachTagging:
			word = item[0]
			wordType = item[1]

			if wordType != 'NN':
				continue;

			totalKeys = totals.keys()
			if word in totalKeys:
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
		

	def getWords(self, textBlock):
		return word_tokenize(textBlock)