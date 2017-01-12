from .dbModel import DbModel
import sys

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

		return


	def buildBasic(self):
		self.resetProcessed()
		
		contextCharNumber = 65
		nodeId = self.getNextUnprocessedNodeId()
		while nodeId:
			self.relatedNodeIds = []
			self.words = []
			self.loadRelatedNodes(nodeId)
			data = {}
			data['name'] = char(contextCharNumber)
			data['text_blockids'] = self.relatedNodeIds
			data['total_association'] = len(self.relatedNodeIds)
			date['wordids'] = self.getWords()
			self.save(data)
			nodeId = self.getNextUnprocessedNodeId()
			contextCharNumber += 1
		
		return

	def getWords(self):

		return

	def resetProcessed(self):
		self.mysql.query('UPDATE text_node SET processed = 0')
		return


	def getNextUnprocessedNodeId(self):
		return self.mysql.query('SELECT nodeid FROM text_node WHERE processed = 0 LIMIT 1 ORDER BY nodeid')


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







