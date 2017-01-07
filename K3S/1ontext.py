from .config import Config
from .mysql import MySql
import sys

class Context():


	def __init__(self, identifier):
		dbConfig = Config.getDbUserConfig()
		dbConfig['name'] = identifier
		self.mysql = MySql(dbConfig)
		self.mysql.connect()
		self.tableName = 'context'
		return


	def save(self, data):
		id = None
		node = self.exists(data)

		if not node:
			id = self.insert(data)
		else:
			id = node[0][0]
			self.update(data, nodeid)

		return id


	def exists(self, data):
		sql = "SELECT contextid FROM " + self.tableName + " WHERE "

		keys = data.keys()
		params = []
		joinRequired = False

		if 'wordids' in keys:
			sql += "wordids LIKE %s "
			params.append('%' + data['wordids'] + '%')
			joinRequired = True

		if 'text_blockids' in keys:
			if joinRequired:
				sql += 'AND '
			sql += "text_blockids = %s "
			params.append('%' + data['text_blockids'] + '%')
			joinRequired = True

		if 'total_association' in keys:
			if joinRequired:
				sql += 'AND '
			sql += "total_association = %s "
			params.append(str(data['total_association']))
		

		return self.mysql.query(sql, params)


	def insert(self, data):
		sql = "INSERT INTO " + self.tableName + " (wordids, text_blockids, total_association) VALUES (%s, %s, %s)"
		
		params = []

		keys = data.keys()
		if 'wordids' in keys:
			params.append(",".join(data['wordids']))

		if 'text_blockids' in keys:
			params.append(",".join(data['text_blockids']))
		
		if 'total_association' in keys:
			params.append(str(data['total_association']))
		
		return self.mysql.insert(sql, params)


	def update(self, data, contextid):
		sql = "UPDATE " + self.tableName + " SET "
		params = []
		joinRequired = False

		keys = data.keys()

		if 'wordids' in keys:
			sql += "wordids = %s "
			params.append(",".join(data['wordids']))
			joinRequired = True

		if 'text_blockids' in keys:
			if joinRequired:
				sql += ', '
			sql += "text_blockids = %s "
			params.append(",".join(data['text_blockids']))
			joinRequired = True
		
		if 'total_association' in keys:
			if joinRequired:
				sql += ', '
			sql += "total_association = %s "
			params.append(str(data['total_association']))

		sql += 'WHERE contextid = ' + str(contextid)

		self.mysql.updateOrDelete(sql, params)
		return


	def deleteByData(self, data):
		id = None
		item = self.exists(data)

		if not item:
			return
		else:
			id = item[0][0]
			self.delete(id)

		return


	def delete(self, contextid):
		sql = "DELETE FROM " + self.tableName + " WHERE contextid = " + str(contextid)
		params = []
		self.mysql.updateOrDelete(sql, params)
		return