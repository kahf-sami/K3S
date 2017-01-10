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
		self.joinFields = []
		self.status = None
		self.limit = 10
		self.offset = 0
		return


	def save(self, data):
		itemid = None
		item = self.exists(data)
		
		if not item:
			itemid = self.insert(data)
			self.status = 'inserted'
		else:
			itemid = item[0][0]
			self.update(data, itemid)
			self.status = 'updated'

		return itemid


	def isInserted(self):
		return (self.status == 'inserted')


	def isUpdated(self):
		return (self.status == 'updated')


	def exists(self, data):
		return self.read(data, False)


	def read(self, data = {}, fetchAllValues = True, asBatch = False):
		if fetchAllValues:
			sql = "SELECT * FROM " + self.tableName + " WHERE "
		else:
			sql = "SELECT " + self.primaryKey  + " FROM " + self.tableName + " WHERE "

		keys = data.keys()
		params = []
		joinRequired = False

		for field in self.fields:
			if (field not in keys) or (field in self.ignoreExists):
				continue

			if joinRequired:
				sql += 'AND '

			if field in self.joinFields:
				sql += field + " LIKE %s "
				params.append('%' + data[field] + '%')
			else:
				sql += field + " = %s "
				params.append(str(data[field]))
			joinRequired = True
		
		if asBatch:
			sql += ' LIMIT ' + str(self.limit) + ' OFFSET ' + str(self.offset)
			self.offset += self.limit

		#print(sql)
		#print(params)
		
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

			if field in self.joinFields:
				params.append(",".join(data[field]))
			else:
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
			if field in self.joinFields:
				params.append(",".join(data[field]))
			else:
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