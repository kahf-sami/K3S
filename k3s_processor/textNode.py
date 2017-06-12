from .dbModel import DbModel
from .word import Word
from k3s_utility.nlp import NLP
from k3s_utility.utility import Utility 
from .wikipediaProcessor import WikipediaProcessor 
from .localContext import LocalContext
from .coreWord import CoreWord
import sys

class TextNode(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'text_node'
		self.primaryKey = 'nodeid'
		self.fields = ['nodeid', 'source_identifier', 'text_block', 'representatives']
		self.ignoreExists = ['text_block', 'representatives']
		self.wordProcessor = Word(identifier)
		self.coreWordProcessor = CoreWord(identifier)
		self.nlpProcessor = NLP()
		self.nodeid = None
		self.wikipedia = WikipediaProcessor(self.identifier)
		return


	def save(self, data, processCore):
		keys = data.keys()
		words = None
		
		if 'text_block' in keys:
			if not data['text_block']:
				return

			if processCore:
				self.coreWordProcessor.saveWords(data['text_block'])

			lc = LocalContext(data['text_block'], self.identifier)
			data['representatives'] = lc.getRepresentative()
			pureRepresentatives = lc.getPureRepresentative()

			words = self.wordProcessor.saveWords(pureRepresentatives)
			
			
			if data['representatives']:
				lc.saveLocalContexts(self.nodeid)
				self.wikipedia.saveWords(data['representatives'], pureRepresentatives)

			self.nodeid = DbModel.save(self, data)

		return self.nodeid



	def getAllByBatch(self):
		sql = "SELECT *  FROM text_node ORDER BY nodeid"
		return self.mysql.query(sql, [], True)


	def getTotalTextBlocks(self):
		sql = "SELECT count(*) FROM text_node"

		result = self.mysql.query(sql, [])
		return result[0][0]

