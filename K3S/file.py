from .directory import Directory
import os
import zipfile

class File():

	
	def __init__(self, path):
		parts = path.split('/')
		self.path = path
		self.fileName = parts[len(parts) - 1]

		parts = path.split('.')
		self.extension = parts[len(parts) - 1]

		self.file = None
		self.lines = None
		self.lineNumber = 0


	def exists(self):
		return os.path.exists(self.path)

	def open(self, mode = "w"):
		self.file = open(self.path, mode)

	def close(self):
		self.file.close()

	def delete(self):
		os.remove(self.path)

	def load(self):
		self.open("r")
		self.lines = self.file.readlines()
		self.close()

	def write(content):
		self.open()
		self.file.write(content)
		self.close()

	def read():
		if(!self.lines):
			self.load()
		return self.lines[]

	def readLine():
		if(!self.lines):
			self.load()
		line = self.lines[self.lineNumber]
		self.lineNumber = self.lineNumber + 1
		return line

	def zip(filePaths):
		self.file = zipfile.ZipFile(self.path, "w")
		if hasattr(filePaths, "__len__"):
			for filePath in filePaths:
				self.file.write(filePath)
		else:
			self.file.write(filePaths)
		self.file.close()

	def isZipFile(self):
		return zipfile.is_zipfile(self.path)

	def unzip(self):
		self.file = zipfile.ZipFile(self.path)
		for fileName in self.file.namelist():
			self.file.read(fileName)
		self.file.close()


	@staticmethod
	def join(*args):
		return os.path.join(args)


