from .dbModel import DbModel
from .context import Context 
from .edge import Edge
from .word import Word
from nltk import word_tokenize
import sys

class TextNode(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'text_node'
		self.primaryKey = 'nodeid'
		self.fields = ['nodeid', 'source_identifier', 'text_block']
		self.ignoreExists = ['text_block']
		self.context = Context(identifier)
		self.edge = Edge(identifier)
		self.word = Word(identifier)
		return


	def save(self, data):
		wordProcessor = Word(self.identifier)
		keys = data.keys()

		if 'text_block' in keys:
			words = word_tokenize(data['text_block'])
			totals = {}
			for word in words:
				totalKeys = totals.keys()
				if word in totalKeys:
					totals[word] += 1
				else:
					totals[word] = 1
			print(totals)
			for word in totals:
				data = {}
				data['word'] = word
				data['count'] = totals[word]
				wordProcessor.save(data)
				sys.exit()
			
		
		return DbModel.__init__(self, data)