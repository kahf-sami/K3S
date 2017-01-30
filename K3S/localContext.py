from .nlp import NLP
import sys
import re
from .utility import Utility
import math
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from .dbModel import DbModel

class LocalContext(DbModel):


	def __init__(self, textBlock, identifier = None):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'local_context'
		self.primaryKey = 'local_contextid'
		self.fields = ['local_contextid', 'nodeid', 'words']
		self.textBlock = textBlock
		self.cleanTextBlock = self.setCleanText(textBlock)
		self.nlpProcessor = NLP()
		self.stemmer = PorterStemmer()
		self.contexts = []
		self.representatives = []
		self.buildRepresentatives()
		self.buildLocalContexts()
		return


	def getRepresentative(self):
		return self.representatives


	def getSentenceContexts(self):
		sentenceContexts = re.split('[?.,!;:\n]', self.cleanTextBlock.lower())
		return sentenceContexts


	def getLocalContexts(self):
		return self.contexts

	def getCleanedTextBlock(self):
		return  re.sub('[?.!;:\n]', '', str(self.cleanTextBlock))


	def setCleanText(self, textBlock):
		textBlock = re.sub(r'\s(bin|ibn)\s', r'_\1_', str(self.textBlock))
		textBlock = re.sub(r'([\']s?)|(-\n)|(\")|(Volume.+Book.+:)', '', str(textBlock))
		textBlock = re.sub('(\s+)|(\s\n)|\(.+\)', ' ', str(textBlock.strip()))
		return textBlock

	def buildRepresentatives(self):
		representatives = self.nlpProcessor.getNouns(self.cleanTextBlock)
		representatives = [word for word in representatives if word not in stopwords.words('english')]
		#print(representatives)
		self.representatives = representatives
		return



	def buildLocalContexts(self):
		sentenceContexts = self.getSentenceContexts()

		#print(sentenceContexts)
		localContexts = []
		index = 0
		for sentence in sentenceContexts:
			prospectiveContextItems = self.getProspectiveContextItems(sentence)
			totalProspectiveItems = len(prospectiveContextItems)
			if totalProspectiveItems == 0:
				continue

			if totalProspectiveItems == 1:
				# only one item
				localContexts = self.appendToLocalContext(prospectiveContextItems[0], localContexts)
				continue
					
			intexOfItem = self.getIndexOfProspectiveContentItems(prospectiveContextItems)

			itemIndex = 0
			combinedContext = []
			for item in prospectiveContextItems:
				if itemIndex == (totalProspectiveItems - 1):
					#Last item
					if item not in combinedContext:
						localContexts = self.appendToLocalContext(item, localContexts)
						
					break
						
				contextDistance = abs(intexOfItem[itemIndex] - intexOfItem[itemIndex + 1])
				if contextDistance == 1:
					if item not in combinedContext:
						combinedContext = self.appendItemToLocalContext(item, combinedContext)

					if prospectiveContextItems[itemIndex + 1] not in combinedContext:
						combinedContext = self.appendItemToLocalContext(prospectiveContextItems[itemIndex + 1], combinedContext)
				else:
					localContexts = self.appendToLocalContext(item, localContexts)

				itemIndex += 1


			if len(combinedContext):
				localContexts.append(combinedContext)

			index += 1
		
		return self.loadContexts(localContexts)

	def getIndexOfProspectiveContentItems(self, prospectiveContextItems):
		intexOfItem = []
		for item in prospectiveContextItems:
			intexOfItem.append(self.representatives.index(item))
		return intexOfItem


	def appendToLocalContext(self, item, localContexts):
		stemmedItem = self.stemmer.stem(item)
		if stemmedItem == item:
			itemList = [item]
		else:
			itemList = [item, stemmedItem]

		localContexts.append(itemList)
		return localContexts


	def appendItemToLocalContext(self, item, localContexts):
		stemmedItem = self.stemmer.stem(item)
		if (stemmedItem != item) and (stemmedItem not in localContexts):
			localContexts.append(stemmedItem)

		if item not in localContexts:
			localContexts.append(item)

		return localContexts


	def getProspectiveContextItems(self, sentence):
		words = self.nlpProcessor.getWords(sentence)
		return Utility.intersect(self.representatives, words)


	def loadContexts(self, localContexts):
		self.contexts = []	
		for localContext in localContexts:
			setMain = set(localContext) 
			totalMain = len(localContext)
			subSetOfAnother = False
			for subContext in localContexts:
				totalSub = len(subContext)
				if totalSub <= totalMain:
					continue
				setSub = set(subContext) 
				commonItems = setMain & setSub
				similarity = len(commonItems) / totalMain
				if similarity >= 0.75:
					subSetOfAnother = True
				
			if (not subSetOfAnother) and (localContext not in self.contexts):
				self.contexts.append(localContext)

		return self.contexts


	def saveLocalContexts(self, nodeid):
		if not self.contexts:
			return

		for context in self.contexts:
			context.sort()
			data = {}
			data['nodeid'] = nodeid
			data['words'] = ','.join(context)
			self.save(data)
		
		return


	def deleteLocalContextsByNodeid(self, nodeid):
		sql = "DELETE FROM local_context WHERE nodeid = " + str(nodeid)
		params = []
		self.mysql.updateOrDelete(sql, params)
		return