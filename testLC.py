import sys
import K3S
import colorama
import scipy
import numpy

text = ("The Eagle and the Jackdaw: "
	"AN EAGLE, flying down from his perch on a lofty rock, seized upon "
	"a lamb and carried him aloft in his talons.  A Jackdaw, who "
	"witnessed the capture of the lamb, was stirred with envy and "
	"determined to emulate the strength and flight of the Eagle. He "
	"flew around with a great whir of his wings and settled upon and "
	"large ram, with the intention of carrying him off, but his claws "
	"became entangled in the ram's fleece and he was not able to "
	"release himself, although he fluttered with his feathers as much "
	"as he could.  The shepherd, seeing what had happened, ran up and"
	"caught him.  He at once clipped the Jackdaw's wings, and taking "
	"him home at night, gave him to his children. On their saying, "
	"\"Father, what kind of bird is it?'  he replied, \"To my certain "
	"knowledge he is a Daw; but he would like you to think an Eagle.\"")

processor = K3S.LocalContext(text)
#print(processor.getRepresentative())
#print(processor.getLocalContexts())

print("===============================================")
text2 = ("The Farmer and His Sons: "
	"A FATHER, being on the point of death, wished to be sure that his "
	"sons would give the same attention to his farm as he himself had "
	"given it.  He called them to his bedside and said, \"My sons, "
	"there is a great treasure hid in one of my vineyards.\"  The sons,"
	"after his death, took their spades and mattocks and carefully dug "
	"over every portion of their land.  They found no treasure, but "
	"the vines repaid their labor by an extraordinary and "
	"superabundant crop.")

processor = K3S.LocalContext(text1)
#print(processor.getRepresentative())
print(processor.getLocalContexts())
sys.exit()