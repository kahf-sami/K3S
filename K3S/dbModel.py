from .config import Config
from .mysql import MySql


class DbModel():


	def __init__(self, identifier):
		dbConfig = Config.getDbUserConfig()
		dbConfig['name'] = identifier
		self.mysql = MySql(dbConfig)
		self.mysql.connect()
		self.tableName = None
		self.primaryKey = None
		self.fields = []
		self.ignoreExists = []
		return


	def save(self, data):
		itemid = None
		item = self.exists(data)

		if not item:
			itemid = self.insert(data)
		else:
			itemid = item[0][0]
			self.update(data, itemid)

		return itemid


	def exists(self, data):
		sql = "SELECT " + self.primaryKey  + " FROM " + self.tableName + " WHERE "

		keys = data.keys()
		params = []
		joinRequired = False

		for field in self.fields:
			if (field not in keys) or (field in self.ignoreExists):
				continue

			if joinRequired:
				sql += 'AND '
			
			sql += field + " = %s "
			params.append(str(data[field]))
			joinRequired = True

		return self.mysql.query(sql, params)


	def insert(self, data):
		fieldList = ''
		placeholder = ''
		params = []
		joinRequired = False
		keys = data.keys()

		for field in self.fields:
			if field not in keys:
				continue

			params.append(str(data[field]))
			if joinRequired:
				fieldList += ','
				placeholder += ','

			fieldList += field
			placeholder += '%s'
			joinRequired = True
		
		sql = "INSERT INTO " + self.tableName + " (" + fieldList + ") VALUES (" + placeholder + ")"
		
		return self.mysql.insert(sql, params)


	def update(self, data, itemid):
		sql = "UPDATE " + self.tableName + " SET "
		params = []
		joinRequired = False

		keys = data.keys()

		for field in self.fields:
			if field not in keys:
				continue

			if joinRequired:
				sql += ', '
			
			sql += field + " = %s "
			params.append(str(data[field]))
			joinRequired = True

		sql += 'WHERE ' + self.primaryKey + ' = ' + str(itemid)

		self.mysql.updateOrDelete(sql, params)
		return


	def deleteByData(self, data):
		itemid = None
		item = self.exists(data)

		if not item:
			return
		else:
			itemid = item[0][0]
			self.delete(itemid)

		return


	def delete(self, itemid):
		sql = "DELETE FROM " + self.tableName + " WHERE " + self.primaryKey + " = " + str(itemid)
		params = []
		self.mysql.updateOrDelete(sql, params)
		return