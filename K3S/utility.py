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

