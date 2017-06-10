'''
https://en.wikipedia.org
'''

from .htmlParser import HTMLParser
import re, sys
from k3s_utility.nlp import NLP
from k3s_utility.utility import Utility
from nltk.stem.porter import PorterStemmer
import requests, json

class Wikipedia(HTMLParser):


	def __init__(self, url = None):
		self.paragraphs = None
		self.index = 0
		self.categories = None
		self.nlpProcessor = NLP()
		self.stemmer = PorterStemmer()
		self.words = {}
		self.pureWords = {}
		self.positionContribution = None 
		self.positionContributingFactor = 0.5
		self.occuranceContributingFactor = 1
		self.concepts = None

		super(Wikipedia, self).__init__(url)
		return


	def setTree(self):
		self.index = 0
		self.words = {}
		self.pureWords = {}
		self.concepts = None
		super(Wikipedia, self).setTree()

		self.categories = self.getByXpath("//div[@class='mw-normal-catlinks']//a/text()")
		if self.categories:
			self.categories.pop(0) #Removing title category

		self.paragraphs = self.getByXpath("//div[@class='mw-parser-output']//p")
		
		#print(self.categories)
		#print(self.paragraphs)
		return


	def getMostRelevantUrl(self, word):
		items = self.fetchRelatedPages(word)
		if not items:
			return ''
		
		url = ''
		#print(word)
		firstOne = None
		for item in items:
			if not firstOne:
				firstOne = item['fullurl']

			title = self.stemmer.stem(item['title'])
			if(title == word):
				return item['fullurl']

		return firstOne


	def fetchRelatedPages(self, word):
		params = {'action': 'query', 
			'generator': 'search', 
			'prop': 'info',
			'inprop': 'url',
			'format': 'json',
			'formatversion' : 2,
			'gsrsearch': word }
		
		url = 'https://en.wikipedia.org/w/api.php?' + Utility.utlencode(params)	
		#/Utility.debug(url)
		page = requests.get(url)
		response = json.loads(page.content.decode('utf-8'))
		#Utility.debug(response)

		if 'query' not in response.keys():
			return None

		return response['query']['pages']


	def resetIndex(self):
		self.index = 0
		return


	def fetchParagraph(self, index = 0):
		if not self.paragraphs:
			return ''

		return self.paragraphs[index].text_content()


	def fetchNext(self):
		text = self.fetchParagraph(self.index)
		self.index += 1
		return text


	def getImportantConcepts(self):
		if not self.concepts:
			return None

		concepts = []

		for concept in self.concepts[:20]:
			concepts.append(self.pureWords[concept])

		return concepts


	def processLocalContext(self):
		text = self.fetchParagraph() #Fetching first paragraph

		if self.categories:
			for category in self.categories:
				text += ' ' + category + '. '

		text = self.getCleanText(text)

		if not text:
			return

		return self.buildLocalContext(text)


	def buildLocalContext(self, text):
		afterPartsOfSpeachTagging = self.nlpProcessor.getWords(text, True);
		self.positionContribution = len(afterPartsOfSpeachTagging)

		for item in afterPartsOfSpeachTagging:
			if (item[1] not in ['NN', 'NNS']) or (len(item[0]) < 2):
				continue

			word = self.stemmer.stem(item[0].lower())
			self.pureWords[word] = item[0]
			self.increaseScore(word)

		self.concepts =  [k for k in sorted(self.words, key=self.words.get, reverse=True)]
		return self.concepts


	def increaseScore(self, word):
		if word not in self.words:
			self.words[word] = 0

		self.words[word] += self.occuranceContributingFactor + self.positionContribution * self.positionContributingFactor
		self.positionContribution -= 1
		return		


	def getCleanText(self, text):
		#text = re.sub('\(.+\)', ' ', text)
		text = re.sub('[^a-zA-Z0-9\s_\-\?:;.,!]+', ' ', text)
		text = re.sub('\s+', ' ', text)
		text = text.strip()
		return text

	
		