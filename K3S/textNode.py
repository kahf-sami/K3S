from .dbModel import DbModel
from .edge import Edge
from .word import Word

import sys

class TextNode(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'text_node'
		self.primaryKey = 'nodeid'
		self.fields = ['nodeid', 'source_identifier', 'text_block']
		self.ignoreExists = ['text_block']
		self.contextProcessor = Context(identifier)
		self.edgeProcessor = Edge(identifier)
		self.wordProcessor = Word(identifier)
		self.nodeid = None
		return


	def save(self, data):
		keys = data.keys()
		words = None

		if 'text_block' in keys:
			# Save the node
			self.nodeid = DbModel.save(self, data)

			# Save the words
			if self.isInserted():
				words = self.wordProcessor.saveWords(data['text_block'])
			else:
				words = self.wordProcessor.getWords(data['text_block'])

			# Save related content
			self.relate(words, self.nodeid)

		return self.nodeid


	def relate(self, words, currentNodeId):
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