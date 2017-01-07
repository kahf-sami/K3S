from .dbModel import DbModel
from .context import Context 
from .edge import Edge
from .word import Word

class TextNode(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.tableName = 'text_node'
		self.primaryKey = 'nodeid'
		self.fields = ['nodeid', 'source_identifier', 'text_block']
		self.ignoreExists = ['text_block']
		self.context = Context(identifier)
		self.edge = Edge(identifier)
		self.word = Word(identifier)
		return


