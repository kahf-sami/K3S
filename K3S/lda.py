from gensim import corpora, models
import gensim
from .config import Config
from .file import File

class LDA():


	def __init__(self, identifier, number = 5):
		self.identifier = identifier
		self.config = Config()
		self.filePath = File.join(self.config.DATA_PATH, identifier, 'LDA-' + str(number))
		self.model = None
		self.loadModel()
		self.numberOfTopics = number
		return


	def loadModel(self):
		file = File(self.filePath)
		if file.exists():
			self.model = gensim.models.ldamodel.LdaModel.load(self.filePath)
		




	def train(self, textBlocks):			
		if self.model:
			dictionary = corpora.Dictionary.load(self.filePath + '_dictionary')
			dictionary.add_documents(textBlocks)
			corpus = [dictionary.doc2bow(text) for text in textBlocks]
			# Not working: https://radimrehurek.com/gensim/corpora/mmcorpus.html need to check corpus merge
			self.model.update(corpus)
		else:
			dictionary = corpora.Dictionary(textBlocks)
			corpus = [dictionary.doc2bow(text) for text in textBlocks]
			self.model = gensim.models.ldamodel.LdaModel(corpus, num_topics=self.numberOfTopics, id2word = dictionary, passes=10, update_every=0)
			self.model.save(self.filePath)
			
		dictionary.save(self.filePath + '_dictionary.dict')
		return