import sys
import K3S
import colorama
import scipy
import numpy

text1 = ("The Prophet said, \"Faith (Belief) consists of more than sixty branches (i.e. parts)."
	"And Haya (This term \"Haya\" covers a large number of concepts which are to be taken together; "
	"amongst them are self respect, modesty, bashfulness, and scruple, etc.) is a part of faith.\"")

text2 = ('Narrated Abu Said Al-Khudri: The Prophet said, "When the people of Paradise will enter Paradise and the people of '
		'Hell will go to Hell, Allah will order those who have had faith equal to the weight of a grain of mustard seed to be '
		'taken out from Hell. So they will be taken out but (by then) they will be blackened (charred).'
		' Then they will be put in the river of Haya (rain) or Hayat (life) (the Narrator is in doubt as to which is the right term), '
		'and they will revive like a grain that grows near the bank of a flood channel. Don\'t you see that it comes out yellow and twisted"')

text3 = ('Narrated Abu Huraira: ' 
'Some people said, "O Allah\'s Apostle! Shall we see our Lord on the Day of Resurrection?" He said, '
'"Do you crowd and squeeze each other on looking at the sun when it is not hidden by clouds?" They '
'replied, "No, Allah\'s Apostle." He said, "Do you crowd and squeeze each other on looking at the moon '
'when it is full and not hidden by clouds?" They replied, No, O Allah\'s Apostle!" He said, "So you will '
'see Him (your Lord) on the Day of Resurrection similarly Allah will gather all the people and say, '
'Whoever used to worship anything should follow that thing. \'So, he who used to worship the sun, '
'will follow it, and he who used to worship the moon will follow it, and he who used to worship false '
'deities will follow them; and then only this nation (i.e., Muslims) will remain, including their hypo-'
'crites. Allah will come to them in a shape other than they know and will say, \'I am your Lord.\' They '
'will say, \'We seek refuge with Allah from you. This is our place; (we will not follow you) till our Lord '
'comes to us, and when our Lord comes to us, we will recognize Him. '
'Then Allah will come to then in a shape they know and will say, "I am your Lord.\' They will say, '
'(No doubt) You are our Lord,\' and they will follow Him. Then a bridge will be laid over the (Hell) '
'Fire." Allah\'s Apostle added, "I will be the first to cross it. And the invocation of the Apostles on that '
'Day, will be \'Allahukka Sallim, Sallim (O Allah, save us, save us!),\' and over that bridge there will be '
'hooks Similar to the thorns of As Sa\'dan (a thorny tree). Didn\'t you see the thorns of As-Sa\'dan?" The '
'companions said, "Yes, O Allah\'s Apostle." He added, "So the hooks over that bridge will be like the '
'thorns of As-Sa-dan except that their greatness in size is only known to Allah. These hooks will '
'snatch the people according to their deeds. Some people will be ruined because of their evil deeds, '
'and some will be cut into pieces and fall down in Hell, but will be saved afterwards, when Allah has '
'finished the judgments among His slaves, and intends to take out of the Fire whoever He wishes to '
'take out from among those who used to testify that none had the right to be worshipped but Allah. '
'We will order the angels to take them out and the angels will know them by the mark of the traces '
'of prostration (on their foreheads) for Allah banned the fire to consume the traces of prostration on '
'the body of Adam\'s son. So they will take them out, and by then they would have burnt (as coal), and '
'then water, called Maul Hayat (water of life) will be poured on them, and they will spring out like a '
'seed springs out on the bank of a rainwater stream, and there will remain one man who will be fa-'
'cing the (Hell) Fire and will say, \'O Lord! It\'s (Hell\'s) vapor has Poisoned and smoked me and its flame '
'has burnt me; please turn my face away from the Fire.\' He will keep on invoking Allah till Allah says, '
'Perhaps, if I give you what you want), you will ask for another thing?\' The man will say, \'No, by Your '
'Power, I will not ask You for anything else.\' '
'Then Allah will turn his face away from the Fire. The man will say after that, \'O Lord, bring me '
'near the gate of Paradise.\' Allah will say (to him), \'Didn\'t you promise not to ask for anything else? '
'Woe to you, O son of Adam ! How treacherous you are!\' The man will keep on invoking Allah till Al-'
'lah will say, \'But if I give you that, you may ask me for something else.\' The man will say, \'No, by '
'Your Power. I will not ask for anything else.\' He will give Allah his covenant and promise not to ask '
'for anything else after that. So Allah will bring him near to the gate of Paradise, and when he sees '
'what is in it, he will remain silent as long as Allah will, and then he will say, \'O Lord! Let me enter '
'Paradise.\' Allah will say, \'Didn\'t you promise that you would not ask Me for anything other than '
'that? Woe to you, O son of Adam ! How treacherous you are!\' On that, the man will say, \'O Lord! Do '
'not make me the most wretched of Your creation,\' and will keep on invoking Allah till Allah will '
'smile and when Allah will smile because of him, then He will allow him to enter Paradise, and when '
'he will enter Paradise, he will be addressed, \'Wish from so-and-so.\' He will wish till all his wishes '
'will be fulfilled, then Allah will say, All this (i.e. what you have wished for) and as much again there-'
'with are for you.\' "' 
'Abu Huraira added: That man will be the last of the people of Paradise to enter (Paradise). '
'Narrated \'Ata (while Abu Huraira was narrating): Abu Said was sitting in the company of Abu '
'Huraira and he did not deny anything of his narration till he reached his saying: "All this and as '
'much again therewith are for you." Then Abu Sa\'id said, "I heard Allah\'s Apostle saying, \'This is for '
'you and ten times as much.\' " Abu Huraira said, "In my memory it is \'as much again therewith.\'')
#processor = K3S.Processor('Bukhari') 
#processor.calculateLDA(500)
lda = K3S.LDA('Bukhari', 500)
lda.display()
lda.getTopics(text3)
sys.exit()

processor = K3S.Processor('Bukhari') 
#processor.topologySetUp()
#processor.saveBlocksInMysql()
#processor.calculateTfIdf()
processor.calculateLDA(1)
sys.exit()
processor.calculateLDA(5)
processor.calculateLDA(10)
processor.calculateLDA(50)
processor.calculateLDA(100)
processor.calculateLDA(500)
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