#import glob
import os
#import sys
#import pandas
#import numpy
#import math
#import tensorflow as tf
#import matplotlib.pyplot as plt


class Config:


	def __init__(self):
		self.ROOT_PATH = os.path.abspath(__file__ + "/../../")
		self.LIBRARY_PATH = os.path.join(self.ROOT_PATH, 'K3S')
		self.DATA_PATH = os.path.join(self.ROOT_PATH, 'data')
		self.DATA_PROCESSED_PATH = os.path.join(self.DATA_PATH, 'processed')
		self.LOG_LOCATION = os.path.join(self.ROOT_PATH, 'temp', 'logs')
		self.RUN_LOCATION = os.path.join(self.ROOT_PATH, 'temp', 'runs')


	@staticmethod
	def getDbUserConfig():
		return {'userName': 'k3s_user', 'host':'localhost', 'password': 'b15m1llah'}
