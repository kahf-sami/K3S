'''
pip install lxml 
pip install requests
'''

from lxml import html
import requests

class HTMLParser():

	def __init__(self, url = None):
		if url:
			self.url = url
			self.setTree()
		return


	def setUrl(self, url):
		self.url = url
		return

	def setTree(self):
		#print(self.url)
		page = requests.get(self.url)
		self.tree = html.fromstring(page.content)
		return


	def getByXpath(self, xpath):
		#print(xpath)
		return self.tree.xpath(xpath)

