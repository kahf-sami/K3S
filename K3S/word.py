from .dbModel import DbModel
from nltk import word_tokenize
import sys


class Word(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.tableName = 'word'
		self.primaryKey = 'wordid'
		self.fields = ['wordid', 'contextid', 'word', 'count', 'tf_idf']
		self.ignoreExists = ['count', 'tf_idf']
		return


	def save(self, data):
		itemid = None
		item = self.read(data)

		if not item:
			itemid = self.insert(data)
		else:
			itemid = item[0][0]
			data['count'] += item[0][3]
			self.update(data, itemid)
				
		return itemid


	def saveWords(self, textBlock):
		words = word_tokenize(textBlock)
		totals = {}
		for word in words:
			totalKeys = totals.keys()
			if word in totalKeys:
				totals[word] += 1
			else:
				totals[word] = 1
			
		for word in totals:
			data = {}
			data['word'] = word
			data['count'] = totals[word]
			self.save(data)

		return words

	def getWords(self, textBlock):
		return word_tokenize(textBlock)