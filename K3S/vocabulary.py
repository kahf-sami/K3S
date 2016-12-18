import collections
import six
import pickle
from nltk import word_tokenize
from .file import File
from .config import Config
import numpy

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
		return


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
			
			wordIds = numpy.zeros(self.maxLength, numby.int64)
			
			for index, blockWord in enumerate(blockWords):
				if index > self.maxLength:
					break
				wordIds[index] = self.getWordId(blockWord)
			
		yield wordIds


		
	def fitTransform(self, textBlocks):
		self.bulidVocabularyFromTextBlock(textBlocks)
		return self.transfromTextBlocksToWordIdsMatrix(textBlocks)


	def save(self):
		file - File(self.vocabPath)
		file.write(pickle.dumps(self))
		return


	@classmethod
	def restore(cls, identifier):
		config = Config()
		vocabPath = File.join(config.DATA_PATH, identifier, 'vocab.plk')
		file - File(vocabPath)
		return pickle.loads(file.read('rb'))




  def reverse(self, documents):
    """Reverses output of vocabulary mapping to words.

    Args:
      documents: iterable, list of class ids.

    Yields:
      Iterator over mapped in words documents.
    """
    for item in documents:
      output = []
      for class_id in item:
        output.append(self.vocabulary_.reverse(class_id))
      yield ' '.join(output)

  def save(self, filename):
    """Saves vocabulary processor into given file.

    Args:
      filename: Path to output file.
    """
    with gfile.Open(filename, 'wb') as f:
      f.write(pickle.dumps(self))

  @classmethod
  def restore(cls, filename):

    """Restores vocabulary processor from given file.

    Args:
      filename: Path to file to load from.

    Returns:
      VocabularyProcessor object.
    """
    with gfile.Open(filename, 'rb') as f:
      return pickle.loads(f.read())


