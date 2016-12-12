from .config import Config
import logging

class Log():

	self.config = None
	self.logPath = None
	self.fileName = 'general.log'
	self.logFilePath = None
	self.logger = None

	def __init__(self):
		self.config = K3S.Config()
		self.logPath = config.LOG_LOCATION
		self.logFilePath = os.path.join(self.logPath, self.fileName)
		self.setLogger()

	def setName(name):
		self.fileName = name;

	def setPath(path):
		self.logFilePath = path

	def setLogger():
		self.logger = logging.basicConfig(self.logFilePath, level=logging.DEBUG, 
			format='%(levelname)s:%(asctime)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

	def getLogger():
		return self.logger

	def add(message, type = 'info'):
		if type == 'debug':
			self.logger.debug(message)
		else if type == 'warn':
			self.logger.warning(message)
		else if type == 'error':
			self.logger.error(message)
		else if  type == 'critical':
			self.logger.critical(message)
		else
			self.logger.info(message)

	def debug(message):
		self.add(message, 'debug')

	def error(message):
		self.add(message, 'error')

	def critical(message):
		self.add(message, 'critical')

	def warn(message):
		self.add(message, 'warn')