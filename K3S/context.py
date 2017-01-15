from .dbModel import DbModel
from .word import Word
from .utility import Utility
import sys
import re

class Context(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'context'
		self.primaryKey = 'contextid'
		self.fields = ['contextid', 'parent_contextid', 'ancestor_contextid', 'name', 'wordids', 'text_blockids', 'total_association']
		self.ignoreExists = ['total_association', 'wordids', 'text_blockids']
		self.joinFields = ['wordids', 'text_blockids']
		self.relatedNodeIds = []
		self.words = []
		self.wordProcessor = Word(identifier)
		self.context = {}
		return


	def buildBasic(self):
		self.resetProcessed()
		node = self.getNextUnprocessedNode()
		
		contextCharNumber = 65
		self.context = {}
		totalContexts = 0
		while node:
			nodeId = node[0][0]
			textBlock = node[0][1]
			words = self.wordProcessor.getNouns(textBlock)
			if not totalContexts:
				self.loadInitContext(words)
				#contextName = chr(contextCharNumber)
				#wordDetails = self.wordProcessor.getWordsDetails(words)
				#for word in words:
				#	otherMatchingWords = self.otherMatchingWords(word[0])
				#	print(word)
			#else:
			#	for contextName

			print()
			sys.exit()
			self.words = []
			self.loadRelatedNodes(nodeId)
			#data = {}
			#data['name'] = char(contextCharNumber)
			#data['text_blockids'] = self.relatedNodeIds
			#data['total_association'] = len(self.relatedNodeIds)
			#date['wordids'] = self.getWords()
			#self.save(data)
			nodeId = self.getNextUnprocessedNodeId()
			contextCharNumber += 1
		
		
		return


	def loadInitContext(self, words):
		words = Utility.unique(words)

		print(self.getOtherRelatedContents(words))
		sys.exit()
		return

	def getOtherRelatedContents(self, words, minGroupLength = 3):
		where = ''
		similarity = "CONCAT_WS(',',"
		similarityScore = "("
		params1 = []
		params2 = []

		joinRequired = False
		for word in words:
			if joinRequired:
				where += ' OR '
				similarity += ','
				similarityScore += "+"
			
			similarity += "IF(text_block like %s, %s, '')"
			similarityScore += "IF(text_block like %s, 1, 0)"
			where += 'text_block like %s'
			
			params1.append('%' + word + '%')
			params1.append(word)
			params2.append('%' + word + '%')
			joinRequired = True

		
		similarity += ') as similarity'
		similarityScore += ") as similarity_score"
		sql = "SELECT nodeid, " + similarity + "," + similarityScore + " FROM text_node WHERE (" + where + ") ORDER By similarity_score"
		
		results = self.mysql.query(sql, params1 + params2 + params2)
		
		totalNumberOfRelatedContent = len(results)
		minSimilarity = None
		maxSimilarity = None
		index = 0
		self.context = []
		for result in results:
			#similarity_score = result[2]
			#if similarity_score < minRelatedContent:
			#	continue
			matchedWords = re.sub(r",+", ",", result[1])
			if matchedWords[0] == ',':
				matchedWords = matchedWords[1:]
			if matchedWords[len(matchedWords) - 1] == ',':
				matchedWords = matchedWords[:-1]
			
			matchedWords = matchedWords.split(',')
			matchedWords.sort()
			self.context.append(set(matchedWords))

			#if not self.context:
			#	self.context.append(set(matchedWords))
			#else:
			#	currentSet = set(matchedWords)
			#	for singleContext in self.context:
			#		if len(currentSet) == 0:
			#			break
			#		currentSet = set(currentSet) - set(singleContext)

			#	if len(currentSet):
			#		self.context.append(set(currentSet))
			
			
			
			#index +=1
			#if index == 1000:
			#	break


		print(set.intersection(*self.context))
		modifiedContext = []
		for refContext in self.context:
			

			for otherContext in self.context:
				if refContext == otherContext:
					continue
				common = refContext & otherContext
				if len(common)  >= minGroupLength: 
					modifiedContext.append(common)
					
		for context in modifiedContext:
			print(context)
			print('-----------------------------------')
		sys.exit()
		return results


	def otherMatchingWords(self, word):
		sql = 'SELECT nodeid, text_block FROM text_node WHERE text_block LIKE %s';
		params = []
		params.append('%' + word + '%')

		results = self.mysql.query(sql, params)
		
		sys.exit()
		return

	def getExistingContexts(self):
		return self.context



	def getAll(self):
		return self.mysql.query('SELECT contextid, name, wordids  FROM context ORDER BY contextid')
	

	def resetProcessed(self):
		self.mysql.updateOrDelete('UPDATE text_node SET processed = 0', [])
		return


	def getNextUnprocessedNode(self):
		return self.mysql.query('SELECT nodeid, text_block FROM text_node WHERE processed = 0 ORDER BY nodeid LIMIT 1')


	def loadRelatedNodes(self, nodeId):
		nodeIds = self.getAssociatedNodeIds()
                 
		self.relatedNodeIds.append(nodeId)

		if not nodeIds:
			self.markAsProcessed(nodeId)
			return

		for nodeId in nodeIds:
			if nodeId not in self.relatedNodeIds:
				self.loadRelatedNodes(nodeId)

		self.markAsProcessed(nodeId)
		return


	def getAssociatedNodeIds(self, nodeId):
		fetchSql = "SELECT destination_nodeid FROM edge WHERE source_nodeid = %s ORDER BY total_common_words"
	
		params = []
		params.append(str(nodeId))
		nodeIds = self.mysql.query(fetchSql, params)

		return nodeIds


	def markAsProcessed(self, nodeId):
		updateSql = "UPDATE text_node SET processed = 1 WHERE nodeid = %s"

		params = []
		params.append(str(nodeId))

		self.mysql.query(updateSql, params)
		return







