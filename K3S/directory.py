from .config import Config
import os

Class Directory():

	def __init__(self, path = None):
		self.config = Config()
		self.dataPath = self.config.DATA_PATH
		self.path = path
		self.name = None

	def setPath(self, path):
		self.path = path

	def exists(self):
		return os.path.exists(self.path)

	def create(self):
		if(self.exists()):
			return
		os.makedirs(self.path)

	def remove(self):
		if(!self.exists()):
			return
		for root, dirs, files in os.walk(self.path, topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		os.rmdir(self.path)

	def scan(self):
		return next(os.walk(path))[2]