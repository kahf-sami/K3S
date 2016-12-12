class File():

	
	def __init__(self):
		self.path = None
		self.fileName = None
		self.extension = None

	@staticmethod
	def join(*args):
		print('Length:', len(args))
		finalPath = ''
		for arg in args:
			if(finalPath):
				finalPath.__add__('/')
			finalPath.__add__(arg)
		return finalPath
