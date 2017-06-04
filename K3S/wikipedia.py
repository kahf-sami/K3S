'''
https://en.wikipedia.org
'''

from .htmlParser import HTMLParser
import re
from .nlp import NLP
from nltk.stem.porter import PorterStemmer


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
		if self.concepts:
			return self.concepts[:10]

		return None


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

		

		