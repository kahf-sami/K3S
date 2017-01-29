from .dbModel import DbModel
from .edge import Edge
from .word import Word
from .context import Context
from .nlp import NLP
import sys
import re
from .utility import Utility
import math
from nltk.stem.porter import PorterStemmer

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
		stemmer = PorterStemmer()
		
		sentenceContexts = re.split('[?.,!;:\n]', textBlock.lower())

		localContexts = []
		
		index = 0
		for sentenceContext in sentenceContexts:
			words = self.nlpProcessor.getWords(sentenceContext)
			prospectiveContextItems = Utility.intersect(representatives, words)
			totalProspectiveItems = len(prospectiveContextItems)
			if totalProspectiveItems == 0:
				continue

			if totalProspectiveItems == 1:
				# only one item
				stemedItem = stemmer.stem(prospectiveContextItems[0])
				if stemedItem == prospectiveContextItems[0]:
					itemList = [prospectiveContextItems[0]]
				else:
					itemList = [prospectiveContextItems[0], stemedItem]

				localContexts.append(itemList)
				continue
					
			intexOfItem = []
					
			for item in prospectiveContextItems:
				intexOfItem.append(representatives.index(item))

			itemIndex = 0
			combinedContext = []
			for item in prospectiveContextItems:
				stemedItem = stemmer.stem(item)
				if stemedItem == item:
					itemList = [item]
				else:
					itemList = [item, stemedItem]
				
				if itemIndex == (totalProspectiveItems -1):
					#Last item
					if stemedItem not in combinedContext:
						localContexts.append(itemList)
					break
						
				contextDistance = abs(intexOfItem[itemIndex] - intexOfItem[itemIndex + 1])
				if contextDistance == 1:
					if stemedItem not in combinedContext:
						combinedContext.append(item)
						if stemedItem != item:
							combinedContext.append(stemedItem)

					stemmedNextItem = stemmer.stem(prospectiveContextItems[itemIndex + 1])

					if stemmedNextItem not in combinedContext:
						combinedContext.append(prospectiveContextItems[itemIndex + 1])
						if stemmedNextItem != prospectiveContextItems[itemIndex + 1]:
							combinedContext.append(stemmedNextItem)
				else:
					localContexts.append(itemList)

				itemIndex += 1


			if len(combinedContext):
				localContexts.append(combinedContext)

			#print(words)
			#print(prospectiveContextItems)
			#print(localContexts)
			#print('-------------------------------')
			index += 1

		finalLocalContexts = []	
		for localContext in localContexts:
			setMain = set(localContext) 
			totalMain = len(localContext)
			subSetOfAnother = False
			for subContext in localContexts:
				totalSub = len(subContext)
				if totalSub <= totalMain:
					continue
				setSub = set(subContext) 
				commonItems = setMain & setSub
				similarity = len(commonItems) / totalMain
				if similarity >= 0.75:
					subSetOfAnother = True
				
			if not subSetOfAnother and localContext not in finalLocalContexts:
				finalLocalContexts.append(localContext)

		#print(sentenceContexts)
		#print('-------------------------------')
		#print(representatives)
		#print('-------------------------------')
		#print(localContexts)
		print('-------------------------------')
		print(finalLocalContexts)
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