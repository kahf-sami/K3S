from .dbModel import DbModel

class Context(DbModel):


	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.tableName = 'context'
		self.primaryKey = 'contextid'
		self.fields = ['contextid', 'wordids', 'text_blockids', 'total_association']
		return


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

