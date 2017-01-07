from .config import Config
from .mysql import MySql
import sys

class TextNode():


	def __init__(self, identifier):
		dbConfig = Config.getDbUserConfig()
		dbConfig['name'] = identifier
		self.mysql = MySql(dbConfig)
		self.mysql.connect()
		self.tableName = 'text_node'
		return


	def save(self, data):
		nodeid = None
		node = self.exists(data)

		if not node:
			nodeid = self.insert(data)
		else:
			nodeid = node[0][0]
			self.update(data, nodeid)

		return nodeid


	def exists(self, data):
		sql = "SELECT nodeid FROM " + self.tableName + " WHERE "

		keys = data.keys()
		params = []
		joinRequired = False

		if 'nodeid' in keys:
			sql += "nodeid = %d "
			params.append(data['nodeid'])
			joinRequired = True

		if 'source_identifier' in keys:
			if joinRequired:
				sql += 'AND '
			sql += "source_identifier = %s "
			params.append(data['source_identifier'])
			joinRequired = True

		"""
		if 'text_block' in keys:
			if joinRequired:
				sql += 'AND '
			sql += "text_block = %s "
			params.append(data['text_block'])
		"""

		return self.mysql.query(sql, params)


	def insert(self, data):
		sql = "INSERT INTO " + self.tableName + " (source_identifier, text_block) VALUES (%s, %s)"
		
		params = []

		keys = data.keys()
		if 'source_identifier' in keys:
			params.append(data['source_identifier'])
		
		if 'text_block' in keys:
			params.append(data['text_block'])
		
		return self.mysql.insert(sql, params)


	def update(self, data, nodeid):
		sql = "UPDATE " + self.tableName + " SET "
		params = []
		joinRequired = False

		keys = data.keys()
		if 'source_identifier' in keys:
			sql += "source_identifier = %s "
			params.append(data['source_identifier'])
			joinRequired = True

		if 'text_block' in keys:
			if joinRequired:
				sql += ', '
			sql += "text_block = %s "
			params.append(data['text_block'])

		sql += 'WHERE nodeid = ' + str(nodeid)

		self.mysql.updateOrDelete(sql, params)
		return

	def deleteByData(self, data):
		nodeid = None
		node = self.exists(data)

		if not node:
			return
		else:
			nodeid = node[0][0]
			self.delete(nodeid)

		return

	def delete(self, nodeid):
		sql = "DELETE FROM " + self.tableName + " WHERE nodeid = " + str(nodeid)
		params = []
		self.mysql.updateOrDelete(sql, params)
		return