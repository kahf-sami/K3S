from k3s_ws.search import Search
from k3s_ws.wikipedia import Wikipedia
from k3s_utility import Utility

'''
LC = Local context
LO = Local ontology
'''
class LO():

	def __init__(self, words):
		self.words = words
		self.wikiConcepts = {}
		self.terms = []
		return

	def process(self):
		if not self.words:
			return

		for word in self.words:
			Utility.debug(word)
			self.wikiConcepts[word] = self.getWikiContext(word)
			Utility.debug(self.wikiConcepts[word])

		return


	def getWikiContext(self, word):
		url = self.getMostImportantWikiLink(word)

		if not url:
			return None

		#Utility.debug(url)

		wikipidia = Wikipedia(url)
		wikipidia.processLocalContext()
		return wikipidia.getImportantConcepts()


		return


	def getMostImportantWikiLink(self, word):
		#searcher = Search()
		#searcher.process(word)
		#return searcher.getMostRelevantLink()

		wikipidia = Wikipedia()
		return wikipidia.getMostRelevantUrl(word)
			
