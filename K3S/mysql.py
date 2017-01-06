from __future__ import print_function
from mysql.connector import connector
from mysql.connector import errorcode

class MySql():


	def __init__(self, config):
		self.config = config
		self.connector = None
		return


	def createDb(self, name):
		database = connector.connect(user = self.config['userName'], password = self.config['password'], host = self.config['host'])
		cursor = database.cursor()
		try:
			cursor.execute('CREATE DATABASE IF NOT EXISTS ' + name)
		except connector.Error as err:
			print("Failed creating database: {}".format(err))
		return

	def connect(self):
		self.connector = connector.connect(user = self.config['userName'], password = self.config['password'], host = self.config['host'], database=self.config['name'])
		return

	def createTables(self, tables):
		return


