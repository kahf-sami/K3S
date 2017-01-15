from .config import Config

class Utility():


	def __init__(self):
		self.config = Config()
		return

	@staticmethod
	def printMatrix(matrixGenerator, rowNumber = None, columnNumber = None):
		if not matrixGenerator:
			return

		rowCount = 0
		
		stringToPrint = ''

		for row in matrixGenerator:
			if (rowNumber and rowNumber != rowCount):
				rowCount += 1
				continue

			columnCount = 0
			for column in row:
				if (columnNumber and (columnNumber == columnCount)) or (columnNumber == None):
					stringToPrint += str(column) + ' '
					columnCount += 1

			stringToPrint += "\n"

		print(stringToPrint)


	@staticmethod
	def getRowColumnOfScipySparseCsrCsrMatrix(matrix, rowNumber):
		print(matrix[rowNumber, :])


	""" return the list with duplicate elements removed """
	@staticmethod
	def unique(a):
		return list(set(a))


	""" return the intersection of two lists """
	@staticmethod
	def intersect(a, b):
		return list(set(a) & set(b))


	""" return the union of two lists """
	@staticmethod
	def union(a, b):
		return list(set(a) | set(b))


