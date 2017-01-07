from .config import Config
from .mysql import MySql
from .textNode import TextNode

class Topology():


	def __init__(self, identifier):
		self.identifier = identifier
		self.dbConfig = Config.getDbUserConfig()
		self.dbConfig['name'] = identifier
		self.mysql = MySql(self.dbConfig)
		return


	def setUp(self):
		self.mysql.createDb(self.identifier)
		self.mysql.createTables(self.getTables())
		return


	def addTextNode(self, sourceIdentifier, textBlock):
		textNode = TextNode(self.identifier)
		data = {}
		data['source_identifier'] = sourceIdentifier
		data['text_block'] = textBlock
		data['nodeid'] = textNode.save(data)


	def getTables(self):
		tables = {}
		
		tables['node'] = (
			"CREATE TABLE IF NOT EXISTS text_node ("
			"nodeid INT(11) NOT NULL AUTO_INCREMENT,"
			"source_identifier VARCHAR (255) NOT NULL DEFAULT '',"
			"text_block LONGTEXT,"
			"PRIMARY KEY (nodeid)"
			") ENGINE=InnoDB")
		
		tables['edge'] = (
			"CREATE TABLE IF NOT EXISTS edge ("
			"edgeid INT(11) NOT NULL AUTO_INCREMENT,"
			"source_nodeid INT(11) NOT NULL,"
			"destination_nodeid INT(11) NOT NULL,"
			"total_common_words INT(11) NOT NULL DEFAULT 0,"
			"PRIMARY KEY (edgeid)"
			") ENGINE=InnoDB")

		tables['context'] = (
			"CREATE TABLE IF NOT EXISTS context ("
			"contextid INT(11) NOT NULL AUTO_INCREMENT,"
			"wordids LONGTEXT NOT NULL,"
			"text_blockids LONGTEXT NOT NULL,"
			"total_association INT(11) NOT NULL DEFAULT 0,"
			"PRIMARY KEY (contextid)"
			") ENGINE=InnoDB")

		tables['word'] = (
			"CREATE TABLE IF NOT EXISTS word ("
			"wordid INT(11) NOT NULL AUTO_INCREMENT,"
			"contextid INT(11) NOT NULL,"
			"word VARCHAR(255) NOT NULL,"
			"count INT(11) NOT NULL,"
			"tf_idf DECIMAL(10,10) DEFAULT 0,"
			"PRIMARY KEY (wordid)"
			") ENGINE=InnoDB")
		
		return tables


