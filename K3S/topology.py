from .config import Config
from .mysql import MySql
from .textNode import TextNode
from .context import Context 

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


	def addTextNode(self, data):
		textNode = TextNode(self.identifier)
		return textNode.save(data)


	def extractContext(self):
		context = Context(self.identifier)
		context.buildBasic()
		return


	def getTables(self):
		tables = {}
		
		tables['node'] = (
			"CREATE TABLE IF NOT EXISTS text_node ("
			"nodeid INT(11) NOT NULL AUTO_INCREMENT,"
			"source_identifier VARCHAR (255) NOT NULL DEFAULT '',"
			"text_block LONGTEXT,"
			"ascii_sum int(11) DEFAULT 0,"
			"processed TINYINT(1) DEFAULT 0,"
			"PRIMARY KEY (nodeid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")
		
		tables['edge'] = (
			"CREATE TABLE IF NOT EXISTS edge ("
			"edgeid INT(11) NOT NULL AUTO_INCREMENT,"
			"source_nodeid INT(11) NOT NULL,"
			"destination_nodeid INT(11) NOT NULL,"
			"total_common_words INT(11) NOT NULL DEFAULT 0,"
			"PRIMARY KEY (edgeid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")

		tables['context'] = (
			"CREATE TABLE IF NOT EXISTS context ("
			"contextid INT(11) NOT NULL AUTO_INCREMENT,"
			"parent_contextid INT(11) DEFAULT NULL,"
			"ancestor_contextid INT(11) DEFAULT NULL,"
			"name VARCHAR(255) NOT NULL,"
			"wordids LONGTEXT NOT NULL,"
			"text_blockids LONGTEXT NOT NULL,"
			"total_association INT(11) NOT NULL DEFAULT 0,"
			"PRIMARY KEY (contextid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")

		tables['word'] = (
			"CREATE TABLE IF NOT EXISTS word ("
			"wordid INT(11) NOT NULL AUTO_INCREMENT,"
			"contextid INT(11) DEFAULT NULL,"
			"word VARCHAR(255) NOT NULL,"
			"count INT(11) NOT NULL DEFAULT 0,"
			"number_of_blocks INT(11) NOT NULL DEFAULT 0,"
			"tf_idf DECIMAL(10,10) DEFAULT 0,"
			"PRIMARY KEY (wordid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")

		tables['word_edge'] = (
			"CREATE TABLE IF NOT EXISTS word_edge ("
			"word_edgeid INT(11) NOT NULL AUTO_INCREMENT,"
			"source_wordid INT(11) NOT NULL,"
			"destination_wordid INT(11) NOT NULL,"
			"similaruty_score INT(11) NOT NULL DEFAULT 0,"
			"PRIMARY KEY (word_edgeid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")
		
		return tables


