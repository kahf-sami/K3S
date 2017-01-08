from .dbModel import DbModel
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
		data['word'] = 'said'
		item = self.read(data)

		if not item:
			itemid = self.insert(data)
		else:
			itemid = item[0][0]
			data['count'] += item[0][3]
			self.update(data, itemid)
				
		return itemid