from .config import Config
from .mysql import MySql

class Topology():


	def __init__(self, identifier):
		self.identifier = identifier
		self.dbConfig = Config.getDbUserConfig()
		self.dbConfig['name'] = identifier
		self.mysql = MySql(self.dbConfig)
		return


	def setUp(self):
		mysql.createDb(self.identifier)
		mysql.createTables(self.getTables())
		return


	def getTables(self):
		tables = {}
		
		tables['node'] = (
			"CREATE TABLE text_node ("
			"nodeid INT(11) NOT NULL AUTO_INCREMENT,"
			"source_identifier VARCHAR (255) NOT NULL DEFAULT ''"
			"text_block LONGTEXT NOT NULL DEFAULT '',"
			"PRIMARY KEY (nodeid)"
			") ENGINE=InnoDB")

		tables['edge'] = (
			"CREATE TABLE edge ("
			"edgeid INT(11) NOT NULL AUTO_INCREMENT,"
			"source_nodeid INT(11) NOT NULL,"
			"destination_nodeid INT(11) NOT NULL,"
			"PRIMARY KEY (edgeid)"
			") ENGINE=InnoDB")

		tables['context'] = (
			"CREATE TABLE context ("
			"contextid INT(11) NOT NULL AUTO_INCREMENT,"
			"wordids LONGTEXT NOT NULL,"
			"text_blockids LONGTEXT NOT NULL,"
			"total_association INT(11) NOT NULL DEFAULT 0,"
			"PRIMARY KEY (contextid)"
			") ENGINE=InnoDB")

		tables['word'] = (
			"CREATE TABLE word ("
			"wordid INT(11) NOT NULL AUTO_INCREMENT,"
			"contextid INT(11) NOT NULL,"
			"word VARCHAR(255) NOT NULL,"
			"count INT(11) NOT NULL,"
			"tf_idf DECIMAL DECIMAL(5,10),"
			"PRIMARY KEY (wordid)"
			") ENGINE=InnoDB")

		return tables


