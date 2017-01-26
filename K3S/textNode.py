from .dbModel import DbModel
from .edge import Edge
from .word import Word
from .context import Context
from .nlp import NLP
import sys
import re
from .utility import Utility

class TextNode(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'text_node'
		self.primaryKey = 'nodeid'
		self.fields = ['nodeid', 'source_identifier', 'text_block', 'ascii_sum', 'processed']
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
			textBlock = re.sub('([\']s?)|(-\n)|(\")', '', str(data['text_block']))
			textBlock = re.sub('(\s+)|(\s\n)|\(.+\)', ' ', str(textBlock))
			#textBlock = self.nlpProcessor.removePunctuation(textBlock)
			data['representatives'] = self.nlpProcessor.getNouns(textBlock)
			localContexts = self.getLocalContexts(textBlock, data['representatives'] )
			# Save the node
			words = self.wordProcessor.saveWords(data['text_block'])
			data['ascii_sum'] = self.wordProcessor.getAsciiSum(words)
			self.nodeid = DbModel.save(self, data)

		return self.nodeid


	def getLocalContexts(self, textBlock, representatives):
		sentenceContexts = re.split('[?.,:\n]', textBlock.lower())

		localContexts = []
		
		index = 0
		for sentenceContext in sentenceContexts:
			words = self.nlpProcessor.getWords(sentenceContext)
			localContextItem = Utility.intersect(representatives, words)

			print(localContextItem)
			index += 1
		
		print(representatives)
		sys.exit()
		
		return localContexts


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