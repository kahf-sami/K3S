from .dbModel import DbModel

class Edge(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.tableName = 'edge'
		self.primaryKey = 'edgeid'
		self.fields = ['edgeid', 'source_nodeid', 'destination_nodeid', 'total_common_words']
		return

