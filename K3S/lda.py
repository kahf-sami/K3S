K3from gensim import corpora, models
import gensim
from .config import Config
from .file import File
from .localContext import LocalContext


class LDA():


	def __init__(self, identifier, number = 5, passes = 20):
		self.identifier = identifier
		self.config = Config()
		self.filePath = File.join(self.config.DATA_PATH, identifier, 'lda', 'LDA-' + str(number) + '-' + str(passes))
		self.dictionaryFilePath = File.join(self.filePath + '_dictionary.dict')
		self.model = None
		self.numberOfTopics = number
		self.dictionary = None
		self.corpus = None
		self.passes = passes
		self.loadModel()
		return


	def loadModel(self):
		file = File(self.filePath)
		if file.exists():
			self.model = gensim.models.ldamodel.LdaModel.load(self.filePath)
			self.dictionary = corpora.Dictionary.load(self.dictionaryFilePath)


	def getTopics(self, textBlock):
		
		lc = LocalContext(textBlock, self.identifier)
		representatives = lc.getRepresentative()
		print('---- Representative ------')
		print(representatives)
		bow = self.dictionary.doc2bow(representatives)

		print('----- Bow ---------')
		print(bow)
		for bowItem in bow:
			wordid = bowItem[0]
			print(self.dictionary.get(wordid))
			topics = self.model.get_term_topics(wordid, minimum_probability=0.5)
			for topic in topics:
				topicid = topic[0]
				print(self.model.show_topic(topicid))

			print('-----------------------------------')

		#localContexts = lc.getLocalContexts()
		topics = self.model.get_document_topics(bow)

		for topic in topics:
			topicid = topic[0]
			print(topic)
			print(self.model.show_topic(topicid))
			print('====================================')

		return
		

	def display(self):
		#print(self.model.print_topics(num_topics=3))
		
		return



	def train(self, textBlocks):			
		if self.model:
			newDictionary = Dictionary(textBlocks)
			self.dictionary = self.dictionary.merge_with(newDictionary)
			corpus = [self.dictionary.doc2bow(text) for text in textBlocks]
			merged_corpus = itertools.chain(some_corpus_from_dict1, dict2_to_dict1[some_corpus_from_dict2])

			dictionary.add_documents(textBlocks)
			corpus = [dictionary.doc2bow(text) for text in textBlocks]
			# Not working: https://radimrehurek.com/gensim/corpora/mmcorpus.html need to check corpus merge
			# http://gensim.narkive.com/4feWtfNv/gensim-3229-merging-three-or-more-dictionaries-corpora
			self.model.update(corpus)
		else:
			dictionary = corpora.Dictionary(textBlocks)
			corpus = [dictionary.doc2bow(text) for text in textBlocks]
			self.model = gensim.models.ldamodel.LdaModel(corpus, num_topics=self.numberOfTopics, id2word = dictionary, passes=self.passes, update_every=0)
			self.model.save(self.filePath)
			
		dictionary.save(self.dictionaryFilePath)
		return