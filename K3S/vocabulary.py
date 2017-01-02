import collections
import six
import pickle
from nltk import word_tokenize
from .file import File
from .config import Config
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
import six

class Vocabulary():


	def __init__(self, identifier, maxLength = 800):
		self.config = Config()
		self.maxLength = maxLength
		self.unknownToken = "<UNKNOWN>"
		self.identifier = identifier
		self.mapping = {self.unknownToken: 0}
		self.reverseMapping = [self.unknownToken]
		self.count = collections.defaultdict(int)
		self.vocabPath = File.join(self.config.DATA_PATH, self.identifier, 'vocab.plk')
		self.tfIdf = None
		self.tfidfCalculation = None
		self.maxCount = 0
		self.minCount = -1
		self.total = 0
		return

	def __len__(self):
		return len(self.mapping)


	def getWordId(self, word):
		if word not in self.mapping:
			self.mapping[word] = len(self.mapping)
			self.reverseMapping.append(word)
			self.count[word] = 0

		return self.mapping[word]


	def getWordById(self, id):
		return self.reverseMapping[id]


	def add(self, word):
		id = self.getWordId(word)
		
		if id <= 0 :
			return

		self.count[word] += 1
		if(self.count[word] > self.maxCount):
			self.maxCount = self.count[word]

		if((self.minCount == -1) or (self.minCount > self.count[word])):
			self.minCount = self.count[word]

		self.total += 1

		return


	def getMax(self):
		return self.maxCount


	def getMin(self):
		return self.minCount


	def getTotal(self):
		return self.total


	def trim(self, minCount = 0, maxCount = None):
		self.count = sorted(sorted(six.iteritems(self.count), key = lambda x: (isinstance(x[0], str), x[0])), key = lambda x: x[1], reverse = True)

		self.mapping = {self.unknownToken: 0}
		self.reverseMapping = [self.unknownToken]

		# index 0 is for unknown
		index = 1
		processedCount = collections.defaultdict(int)
		for word, count in self.count:
			if (maxCount and count > maxCount) or (minCount and count < minCount):
				continue

			self.mapping[word] = index
			self.reverseMapping.append('word')
			processedCount[word] = count
			index += 1


		self.count = processedCount
		return


	def bulidVocabularyFromTextBlock(self, textBlocks):
		for textBlock in textBlocks:
			blockWords = word_tokenize(textBlock)
			for blockWord in blockWords:
				self.add(blockWord)

		return


	def transfromTextBlocksToWordIdsMatrix(self, textBlocks):
		"""Transform documents to wordid matrix.
		Args:
			textBlocks: An iterable which yield either str or unicode.
		Yields:
			x: iterable, [n_samples, max_document_length]. Word-id matrix.
		"""
		for textBlock in textBlocks:
			blockWords = word_tokenize(textBlock)
			
			wordIds = numpy.zeros(self.maxLength, numpy.int64)
			
			for index, blockWord in enumerate(blockWords):
				if index > self.maxLength:
					break
				wordIds[index] = self.getWordId(blockWord)

		yield wordIds


		
	def fitTransform(self, textBlocks):
		self.bulidVocabularyFromTextBlock(textBlocks)
		return self.transfromTextBlocksToWordIdsMatrix(textBlocks)


	def useTfIdf(self, textBlocks):
		self.tfIdf = TfidfVectorizer(tokenizer=word_tokenize, use_idf=True, smooth_idf=True)
		self.tfidfCalculation = self.tfIdf.fit_transform(textBlocks)
		return self.tfidfCalculation


	def getTfIdfVocabulary(self):
		return self.tfIdf.vocabulary_

	def save(self):
		file = File(self.vocabPath)
		file.remove()
		file.write(pickle.dumps(self), 'wb')
		return


	@classmethod
	def restore(cls, identifier):
		config = Config()
		vocabPath = File.join(config.DATA_PATH, identifier, 'vocab.plk')
		file = File(vocabPath)
		if file.exists():
			return pickle.loads(file.read('rb'))
		return Vocabulary(identifier)

