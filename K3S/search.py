'''
http://python-guide-pt-br.readthedocs.io/en/latest/scenarios/scrape/
https://stackoverflow.com/questions/15852238/how-to-construct-complex-google-web-search-query
'''

import re
from .utility import Utility
from nltk import word_tokenize
from .htmlParser import HTMLParser

class Search(HTMLParser):

	def __init__(self, site = None):
		if site:
			self.site = site
		else:
			# Search from wikipidia
			self.site = 'en.wikipedia.org'

		self.baseUrl = 'http://www.google.com/search?q='

		self.term = None
		self.tree = None
		self.links = None
		return


	def setTerms(self, terms):
		self.terms = re.sub('[^a-zA-Z0-9]+', ' ', terms)
		self.terms = re.sub('\s+', ' ', self.terms)
		self.terms = word_tokenize(self.terms)
		self.url = self.baseUrl + Utility.implode(self.terms, '+')
		if self.site:
			self.url += '+site:' + self.site
		return

	def process(self, terms):
		self.setTerms(terms)
		self.setTree()

		self.links = []
		links = self.getByXpath('//h3[@class="r"]//a/@href')
		if not links:
			return

		for link in links:
			link = re.sub('&sa=.+$', '', link)
			self.links.append(link[7:])


	def getLinks(self):
		return self.links


	def getMostRelevantLink(self):
		if not self.links:
			return None

		return self.links[0] 



