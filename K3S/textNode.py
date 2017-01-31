from .dbModel import DbModel
from .edge import Edge
from .word import Word
from .context import Context
from .nlp import NLP
import sys
import re
from .utility import Utility
import math
from .localContext import LocalContext

class TextNode(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'text_node'
		self.primaryKey = 'nodeid'
		self.fields = ['nodeid', 'source_identifier', 'text_block', 'ascii_sum', 'processed', 'local_context', 'representatives']
		self.ignoreExists = ['text_block', 'representatives', 'ascii_sum', 'processed']
		self.contextProcessor = Context(identifier)
		self.edgeProcessor = Edge(identifier)
		self.wordProcessor = Word(identifier)
		self.nlpProcessor = NLP()
		self.nodeid = None
		return


	def save(self, data):
		keys = data.keys()
		words = None
		
		if 'text_block' in keys:
			lc = LocalContext(data['text_block'], self.identifier)
			data['representatives'] = lc.getRepresentative()
			localContexts = lc.getLocalContexts()
			words = self.wordProcessor.saveWords(lc.getCleanText(), data['representatives'])
			data['ascii_sum'] = self.wordProcessor.getAsciiSum(data['representatives'])
			self.nodeid = DbModel.save(self, data)
			if localContexts:
				lc.saveLocalContexts(self.nodeid)

		return self.nodeid





	def relate(self, textBlock, currentNodeId):
		words = self.wordProcessor.getWords(textBlock)

		related = {}
		sql = "SELECT nodeid FROM " + self.tableName + " WHERE text_block LIKE %s AND nodeid != %s"

		processedNodes = []

		#print(words)

		for word in words:
			params = []
			params.append('%' + word + '%')
			params.append(str(currentNodeId))

			nodes = self.mysql.query(sql, params)
			
			if len(nodes) > 0:
				for node in nodes:
					relatedNodeId = node[0]
					
					if relatedNodeId in processedNodes:
						related[relatedNodeId] += 1
					else:
						related[relatedNodeId] = 1

					processedNodes.append(relatedNodeId)

				#print(word)
		#print('-------------------')


		self.edgeProcessor.associate(currentNodeId, related)
		return