from .config import Config
from .mysql import MySql
from .textNode import TextNode
from .word import Word 

class Schema():


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

	def getTables(self):
		tables = {}
		
		tables['text_node'] = (
			"CREATE TABLE IF NOT EXISTS text_node ("
			"nodeid INT(11) NOT NULL AUTO_INCREMENT,"
			"source_identifier VARCHAR (255) NOT NULL DEFAULT '',"
			"text_block LONGTEXT,"
			"representatives LONGTEXT,"
			"PRIMARY KEY (nodeid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")

		tables['core_word'] = (
			"CREATE TABLE IF NOT EXISTS core_word ("
			"core_wordid INT(11) NOT NULL AUTO_INCREMENT,"
			"word VARCHAR(255) NOT NULL,"
			"stemmed_word VARCHAR(255) NOT NULL,"
			"pos_type VARCHAR(255) NOT NULL,"
			"count INT(11) NOT NULL DEFAULT 0,"
			"number_of_blocks INT(11) NOT NULL DEFAULT 0,"
			"stop_word TINYINT(1) NOT NULL DEFAULT 0,"
			"PRIMARY KEY (core_wordid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")

		tables['local_context'] = (
			"CREATE TABLE IF NOT EXISTS local_context ("
			"local_contextid INT(11) NOT NULL AUTO_INCREMENT,"
			"nodeid INT(11) NOT NULL,"
			"word VARCHAR(255) DEFAULT NULL,"
			"weight DOUBLE(11, 2) NOT NULL DEFAULT 0,"
			"PRIMARY KEY (local_contextid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")

		tables['word'] = (
			"CREATE TABLE IF NOT EXISTS word ("
			"wordid INT(11) NOT NULL AUTO_INCREMENT,"
			"word VARCHAR(255) NOT NULL,"
			"stemmed_word VARCHAR(255) NOT NULL,"
			"count INT(11) NOT NULL DEFAULT 0,"
			"number_of_blocks INT(11) NOT NULL DEFAULT 0,"
			"tf_idf DOUBLE(11, 2) DEFAULT 0,"
			"local_avg DECIMAL(20,2) DEFAULT 0.00,"
			"zone TINYINT(1) DEFAULT 0,"
			"PRIMARY KEY (wordid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")
		
		tables['wiki_word_context'] = (
			"CREATE TABLE IF NOT EXISTS wiki_word_context ("
			"wiki_word_contextid INT(11) NOT NULL AUTO_INCREMENT,"
			"wordid INT(11) NOT NULL,"
			"url VARCHAR(255) NOT NULL,"
			"introduction LONGTEXT DEFAULT NULL,"
			"wiki_related_words LONGTEXT,"
			"categories TEXT DEFAULT NULL,"
			"PRIMARY KEY (wiki_word_contextid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")

		tables['word_cloud'] = (
			"CREATE TABLE IF NOT EXISTS word_point ("
			"word_pointid INT(11) NOT NULL AUTO_INCREMENT,"
			"wordid INT(11) NOT NULL,"
			"label VARCHAR (255) NOT NULL DEFAULT '',"
			"x DOUBLE(11, 2) DEFAULT 0,"
			"y DOUBLE(11, 2) DEFAULT 0,"
			"r DOUBLE(11, 2) DEFAULT 0,"
			"theta DOUBLE(11, 2) DEFAULT 0,"
			"PRIMARY KEY (word_pointid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")

		tables['text_cloud'] = (
			"CREATE TABLE IF NOT EXISTS text_point ("
			"text_pointid INT(11) NOT NULL AUTO_INCREMENT,"
			"nodeid INT(11) NOT NULL,"
			"label TEXT NOT NULL,"
			"x DOUBLE(11, 2) DEFAULT 0,"
			"y DOUBLE(11, 2) DEFAULT 0,"
			"r DOUBLE(11, 2) DEFAULT 0,"
			"theta int(11) DEFAULT 0,"
			"PRIMARY KEY (text_pointid)"
			") ENGINE=InnoDB DEFAULT CHARACTER SET=utf8")
		
		return tables


