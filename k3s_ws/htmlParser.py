'''
pip install lxml 
pip install requests
'''

from lxml import html
import requests
import sys

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

		try:
			page = requests.get(self.url, timeout = 10)
			self.tree = html.fromstring(page.content)
			page.raise_for_status()
			#print(page.content)
		except page.exceptions.HTTPError as err:
			print(err)
			return

		return


	def getByXpath(self, xpath):
		if not len(self.tree):
			return None

		return self.tree.xpath(xpath)

