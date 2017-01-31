import sys
import K3S
import colorama
import scipy
import numpy


processor = K3S.Processor('Bukhari') 
processor.topologySetUp()
processor.saveBlocksInMysql()
sys.exit()
#processor.contextExtraction()
#processor.addEdges()

processor = K3S.Processor('Bukhari')
processor.displayResults()

sys.exit()

nlp = K3S.NLP()
text1 = ("The Prophet said, \"Faith (Belief) consists of more than sixty branches (i.e. parts)."
	"And Haya (This term \"Haya\" covers a large number of concepts which are to be taken together; "
	"amongst them are self respect, modesty, bashfulness, and scruple, etc.) is a part of faith.\"")

text2 = ("The Prophet said, \"A Muslim is the one who avoids harming Muslims with his tongue and hands. "
	"And a Muhajir (emigrant) is the one who gives up (abandons) all what Allah has forbidden.")

text3 = ("Some people asked Allah's Apostle, \"Whose Islam is the best? i.e. (Who is a very good Muslim)?\" "
		"He replied, \"One who avoids harming the Muslims with his tongue and hands.\"")


print(text1)
text1 = nlp.removePunctuation(text1)
print('-----------------------------------------------------------------------------------------')
nouns1 = nlp.getNouns(text1)
print(nouns1)
print('-----------------------------------------------------------------------------------------')

print(text2)
text2 = nlp.removePunctuation(text2)
print('-----------------------------------------------------------------------------------------')
nouns2 = nlp.getNouns(text2)
print(nouns2)
print('-----------------------------------------------------------------------------------------')


print(text3)
text3 = nlp.removePunctuation(text3)
print('-----------------------------------------------------------------------------------------')
nouns3 = nlp.getNouns(text3)
print(nouns3)
print('-----------------------------------------------------------------------------------------')
#capitals = nlp.getCapitals()