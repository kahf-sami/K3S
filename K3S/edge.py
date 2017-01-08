from .dbModel import DbModel

class Edge(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.tableName = 'edge'
		self.primaryKey = 'edgeid'
		self.fields = ['edgeid', 'source_nodeid', 'destination_nodeid', 'total_common_words']
		self.ignoreExists = ['total_common_words']
		return


	def associated(self, currentNodeId, related):
		data = {}
		data['source_nodeid'] = currentNodeId

		for relatedNodeId in related:
			data['destination_nodeid'] = relatedNodeId
			data['total_common_words'] = related[relatedNodeId]
			self.save(data)
		
		return
