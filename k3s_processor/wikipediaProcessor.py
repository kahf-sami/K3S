from .dbModel import DbModel
from k3s_ws import Wikipedia
from nltk.stem.porter import PorterStemmer
import sys

class WikipediaProcessor(DbModel):
	

	def __init__(self, identifier):
		DbModel.__init__(self, identifier)
		self.tableName = 'wiki_word_context'
		self.primaryKey = 'wiki_word_contextid'
		self.fields = ['wiki_word_contextid', 'wordid', 'wiki_related_words','url', 'introduction', 'categories']
		self.ignoreExists = ['wiki_related_words', 'url', 'introduction', 'categories']
		self.stemmer = PorterStemmer()
		return


	def saveWords(self, words, pureWords):
		if not words:
			return

		for word in words:
			word = self.stemmer.stem(word)
			data = {}
			data['wordid'] = self.getWordId(word)

			if self.exists(data):
				return

			wikiSearchWord = word
			if word in pureWords.keys():
				wikiSearchWord = pureWords[word]
			data['url'] = self.getMostImportantWikiLink(wikiSearchWord)

			if not data['url']:
				continue

			result = self.getWikiContext(data['url'])
			data['wiki_related_words'] = result[0]

			if (not data['wiki_related_words']) or ('Disambiguation' in data['wiki_related_words']):
				continue

			data['introduction'] = result[1]
			data['categories'] = result[2]
			self.save(data)
		return



	def getWordId(self, word):
		sql = "SELECT wordid FROM word WHERE word.stemmed_word = %s"

		params = []
		params.append(word)
		result = self.mysql.query(sql, params)

		if not result:
			return 0

		return result[0][0]


	def getWikiContext(self, url):
		if not url:
			return None
		
		wikipidia = Wikipedia(url)
		wikipidia.processLocalContext()

		return [wikipidia.getImportantConcepts(), wikipidia.getIntroduction(), wikipidia.getCategories()]


	def getMostImportantWikiLink(self, word):
		wikipidia = Wikipedia()
		return wikipidia.getMostRelevantUrl(word)