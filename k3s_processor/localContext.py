from .dbModel import DbModel
from k3s_lc.lc import LC
from k3s_utility.utility import Utility 
from nltk.stem.porter import PorterStemmer
import sys

class LocalContext(DbModel):


	def __init__(self, textBlock, identifier = None):
		DbModel.__init__(self, identifier)
		self.identifier = identifier
		self.tableName = 'local_context'
		self.primaryKey = 'local_contextid'
		self.fields = ['local_contextid', 'nodeid', 'word', 'weight']
		self.representatives = None
		self.textBlock = textBlock
		self.localContext = LC()
		self.localContext.setText(self.textBlock)
		self.stemmer = PorterStemmer()
		self.scores = None
		self.pureRepresentatives = None

		self.process(self.textBlock)
		return


	def process(self, textBlock):
		self.localContext.setText(self.textBlock)
		self.localContext.process()
		[mostImportantWords , otherProperNouns] = self.localContext.getContributers()
		self.representatives = Utility.union(mostImportantWords, otherProperNouns)

		self.scores = self.localContext.getScores()

		self.pureRepresentatives = {}
		pureWords = self.localContext.getPureWords()
		for word in self.representatives:
			if word in pureWords.keys():
				self.pureRepresentatives[word] = pureWords[word]
			else:
				self.pureRepresentatives[word] = word
		return 



	def getRepresentative(self):
		return self.representatives


	def getPureRepresentative(self):
		return self.pureRepresentatives



	def saveLocalContexts(self, nodeid):
		if not self.representatives or not nodeid:
			return

		self.deleteLocalContextsByNodeid(nodeid)

		for representative in self.representatives:
			data = {}
			data['nodeid'] = nodeid
			data['word'] = self.stemmer.stem(representative)
			if representative in self.scores.keys():
				data['weight'] = self.scores[representative]
			else:
				parts = representative.split(' ')
				data['weight'] = self.scores[self.stemmer.stem(parts[0])]

			self.save(data)
		
		return


	def deleteLocalContextsByNodeid(self, nodeid):
		sql = "DELETE FROM local_context WHERE nodeid = " + str(nodeid)
		params = []
		self.mysql.updateOrDelete(sql, params)
		return