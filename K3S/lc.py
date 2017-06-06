class LC():

	def __init__(self, text):
		self.text = text
		self.scores = {}
		self.pureWords = {}
		self.properNouns = {}
		self.occuranceContributingFactor = 1
		self.positionContributingFactor = 0.5
		self.currentPosition = None
		self.process()
		return


	def process(self):
		return
		
	


	def increaseScore(self, word):
		if word not in self.scores:
			self.scores[word] = 0

		self.scores[word] += self.occuranceContributingFactor + self.currentPosition * self.positionContributingFactor
		self.currentPosition -= 1
		return		


	def getCleanText(self, text):
		text = re.sub('[^a-zA-Z0-9\s_\-\?:;.,!]+', ' ', text)
		text = re.sub('\s+', ' ', text)
		text = text.strip()
		return text