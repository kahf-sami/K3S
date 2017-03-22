from .config import Config
from .file import File
from .timer import Timer
from .directory import Directory
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
import sys
import re
import pandas
from .nlp import NLP

class ToText():


	def __init__(self, sourcePath, destinationPath):
		self.config = Config()
		self.sourcePath = sourcePath
		self.destinationPath = destinationPath
		self.tempPath = File.join(self.config.DATA_PATH, 'temp')

		return


	def convertFromPdf(self):
		file = open(self.sourcePath, 'rb')
		parser = PDFParser(file)
		document = PDFDocument()
		parser.set_document(document)
		document.set_parser(parser)
		document.initialize('')
		manager = PDFResourceManager()
		laparams = LAParams()
		device = PDFPageAggregator(manager, laparams=laparams)
		interpreter = PDFPageInterpreter(manager, device)

		i = 1
		item = 0
		generalFilePath = File.join(self.destinationPath, 'general.txt')
		generalFile = File(generalFilePath)
		generalText = ''

		currentHeader = []
		for pageNumber, page in enumerate(document.get_pages()):
			if i < 3:
				i = i + 1
				continue

			interpreter.process_page(page)
			layout = device.get_result()

			for lt_obj in layout:
				if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
					text = lt_obj.get_text()
					if self.ignoreText(text):
						continue;
					if ((len(text) < 100) and self.isPossibeHeader(text)):
						text = text.strip()
						text = text.replace(" ", "_")
						text = text.replace("/", "")
						text = text.replace("\n", "")
						text = text.replace(":", "")
						currentHeader.append(text)
						item = item + 1
					else:
						lastCurrentHeaderIndex = len(currentHeader) - 1
						if lastCurrentHeaderIndex >= 0 :
							#element = []
							#element.append(text)
							#textContent.append(element)
							#textContentHeader.append(lastCurrentHeaderIndex)
							if len(text) > 15:
								fileName = currentHeader[lastCurrentHeaderIndex]
								filePath = File.join(self.destinationPath, fileName) + '.txt'
								file = File(filePath)
								file.write(text)
						else:
							generalFile.write(text)

			""" Code used for debug 
			i = i + 1
			if i == 10:
				print('--- out --')
				print(len(generalText))
				print(len(currentHeader))
				print(len(textContent))
				print(textContentHeader)
				index = 0;
				for currentHeaderIndex in textContentHeader:
					print(currentHeaderIndex)
					print(currentHeader[currentHeaderIndex])
					print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
					print(textContent[index])
					print('---------------------------------------------------------------')
					index = index + 1
				sys.exit()
			"""
		if currentHeader:
			for fileName in currentHeader:
				text = fileName.replace('_', " ")
				fileName = fileName+ '.txt'
				filePath = File.join(self.destinationPath, fileName)
				file = File(filePath)
				if not file.exists():
					generalFile.write(text)

		return

	def isPossibeHeader(self, text):
		return re.search('BOOK|VOLUME|CHAPTER|SECTION', text, re.IGNORECASE)


	def ignoreText(self, text):
		if re.search('Volume[0-9-\/\s]+1700', text, re.IGNORECASE):
			return True
		elif re.search('VOLUME[0-9-\/\s]+ > BOOK', text, re.IGNORECASE):
			return True

		elif re.search('^CHAPTER.[0-9a-zA-Z\-_\\n\s]+$', text, re.IGNORECASE):
			return True
		return False
	

	def convertFromCsv(self):
		csvFile = File(self.sourcePath)
		rows = csvFile.read()
		
		if not rows.any():
			return

		print('processing .....')
		nlpProcessor = NLP()

		for row in rows:
			fileName = str(row[0]) + '.txt'
			text = ''
			if row[1]:
				text += str(row[1])
			if row[2]:
				text += str(row[2])
			if row[3]:
				text += str(row[3])
			


			filePath = File.join(self.destinationPath, fileName)
			file = File(filePath)
			if file.exists():
				file.remove
			file.write(text)

		return 