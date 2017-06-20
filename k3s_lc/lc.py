import re, sys
from nltk import word_tokenize, pos_tag
from nltk.stem.porter import PorterStemmer
from k3s_utility.utility import Utility

class LC():

	def __init__(self):
		self.stemmer = PorterStemmer()
		self.stopWords = Utility.getStopWords()
		self.text = None
		self.scores = {}
		self.count = {}
		self.pureWords = {}
		self.properNouns = []
		self.occuranceContributingFactor = 1
		self.positionContributingFactor = 0.5
		self.currentPosition = None
		self.contributingWords = None
		return

	def setPositionContributingFactor(self, contributingFactor):
		self.positionContributingFactor = contributingFactor
		return


	def setOccuranceContributingFactor(self, contributingFactor):
		self.occuranceContributingFactor = contributingFactor
		return


	def setText(self, text):
		self.text = self.getCleanText(text)
		return

	def getScores(self):
		return self.scores


	def getPureWords(self):
		return self.pureWords


	def process(self):
		afterPartsOfSpeachTagging = self.getWords(self.text, True);

		self.processWords(afterPartsOfSpeachTagging)

		self.contributingWords = [(k, self.scores[k]) for k in sorted(self.scores, key=self.scores.get, reverse=True)]
		return


	def getProperNouns(self):
		return self.properNouns


	def getTotalContributer(self):
		return len(self.contributingWords)


	def getContributers(self, limit = 15):
		if not self.contributingWords:
			return

		properNounElements = self.getProperNounElements()

		mostImportantWords = []
		usedProperNouns = []

		for word, score in self.contributingWords[:limit]:
			mostImportantWord = word
			if word in properNounElements.keys():
				mostImportantWord = properNounElements[word]
				usedProperNouns.append(mostImportantWord)

			if mostImportantWord not in mostImportantWords:
				mostImportantWords.append(mostImportantWord)

		otherProperNouns = Utility.diff(self.properNouns, usedProperNouns)

		return [mostImportantWords , otherProperNouns]



	def processWords(self, words):
		self.currentPosition  = len(words)
		lastNounProperNoun = False
		for item in words:
			wordType = item[1]
			mainWord = item[0].lower()

			if (wordType not in ['NNP', 'NNPS', 'NN', 'NNS']) or (len(item[1]) == 1) or (len(item[0]) <= 2) or  (mainWord in self.stopWords):
				if item[0] in ['bin', 'ibn']:
					wordType = 'NNP'
				else:
					# Puntuation or other type of word
					lastNounProperNoun = False
					continue

			if item[0] in ['bin', 'ibn']:
					wordType = 'NNP'

						
			if wordType in ['NNP', 'NNPS']:
				self.addToProperNoun(lastNounProperNoun, mainWord)
				lastNounProperNoun = True

			word =  self.stemmer.stem(mainWord)	
			self.pureWords[word] = item[0]
			self.increaseOccurance(word)
			self.increaseScore(word)
				
			self.currentPosition -= 1

		return


	def addToProperNoun(self, lastNounProperNoun, mainWord):
		if lastNounProperNoun:
			lastIndex = len(self.properNouns) - 1
			self.properNouns[lastIndex] = self.properNouns[lastIndex] + ' ' + mainWord
		elif mainWord not in  self.properNouns:
			self.properNouns.append(mainWord)
		
		return
		
	
	def increaseOccurance(self, word):
		if word not in self.count.keys():
			self.count[word] = 0

		self.count[word] += 1 
		return


	def increaseScore(self, word):
		if word not in self.scores.keys():
			self.scores[word] = 0

		self.scores[word] += 1 * self.occuranceContributingFactor + self.currentPosition * self.positionContributingFactor
		return		


	def getCleanText(self, text):
		text = re.sub('[\']{1}', '', text)
		text = re.sub('[^a-zA-Z0-9\s_\-\?:;.,!\"]+', ' ', text)
		text = re.sub('\s+', ' ', text)
		return text


	def getWords(self, text, tagPartsOfSpeach = False):
		words = word_tokenize(text)

		if tagPartsOfSpeach:
			return pos_tag(words)

		return words

	def getProperNounElements(self):
		properNounElements = {}

		if self.properNouns:
			for properNoun in self.properNouns:
				parts = properNoun.split(' ')
				for part in parts:
					stemmedWord =  self.stemmer.stem(part)
					properNounElements[stemmedWord] = properNoun

		return properNounElements

	