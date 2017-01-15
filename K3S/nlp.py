import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import SnowballStemmer 
from nltk import word_tokenize
import re
import sys

class NLP():


	def __init__(self, textBlock = None):
		self.textBlock = textBlock

		return

	def removePunctuation(self, textBlock = None):
		if not textBlock:
			textBlock = self.textBlock

		if not textBlock:
			return None

		textBlock = re.sub('[' + string.punctuation + ']', '', str(textBlock))
		
		return textBlock


	def lower(self, textBlock = None):
		if not textBlock:
			textBlock = self.textBlock

		if not textBlock:
			return None

		return textBlock.lower()

	def removeNewLine(self, textBlock = None):
		if not textBlock:
			textBlock = self.textBlock

		if not textBlock:
			return None

		return textBlock.replace("\n", "")


	def removeHtmlTags(self, textBlock = None):
		if not textBlock:
			textBlock = self.textBlock

		if not textBlock:
			return None

		# First we remove inline JavaScript/CSS:
		cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", textBlock.strip())

		# Then we remove html comments. This has to be done before removing regular
		# tags since comments can contain '>' characters.
		cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)

		# Next we can remove the remaining tags:
		cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)

		# Finally, we deal with whitespace
		cleaned = re.sub(r"&nbsp;", " ", cleaned)
		cleaned = re.sub(r"  ", " ", cleaned)
		cleaned = re.sub(r"  ", " ", cleaned)

		return cleaned.strip()


	def removeStopWord(self, textBlock = None):
		if not textBlock:
			textBlock = self.textBlock

		if not textBlock:
			return None

		words =  word_tokenize(textBlock)
		filteredWords = [word for word in words if word not in stopwords.words('english')]

		return filteredWords


	def stem(self, filteredWords = None, algorithm = 'Snowball'):
		if not filteredWords:
			filteredWords = self.filteredWords

		if not filteredWords:
			return None

		if algorithm == 'Porter':
			stemmer = PorterStemmer()
		elif algorithm == 'Lancasters':
			stemmer = LancasterStemmer()
		else:
			stemmer = SnowballStemmer('english')

		stemmedWords = [stemmer.stem(word) for word in filteredWords]
	
		return stemmedWords


	def getFiltered(self, textBlock = None):
		if not textBlock:
			textBlock = self.textBlock

		if not textBlock:
			return None

		textBlock = self.removePunctuation(textBlock)
		textBlock = self.lower(textBlock)
		textBlock = self.removeNewLine(textBlock)
		textBlock = self.removeHtmlTags(textBlock)
		filteredWords = self.removeStopWord(textBlock)
		filteredWords = self.stem(filteredWords)
		return " ".join(filteredWords)


