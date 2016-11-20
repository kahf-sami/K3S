import os
import logging
from io import StringIO
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

logging.propagate = False
logging.getLogger().setLevel(logging.ERROR)


def convert(filePath, pages=None):
    file = open(filePath, 'rb')
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
    text_content = []
    
    for pageNumber, page in enumerate(document.get_pages()):
        outputFile = open('data/bukhari/' + str(pageNumber) + '_bukhari.txt', 'w');
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                text = lt_obj.get_text()
                text_content.append(text)
                outputFile.write(text);
        outputFile.close()

    return text_content

#print(os.path.dirname(os.path.abspath(__file__)))
text = convert('data/en_Sahih_Al-Bukhari.pdf', pages=[3])
print('Finished');