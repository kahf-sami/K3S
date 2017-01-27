import sys
import K3S
import colorama
import scipy
import numpy

text = ("The Eagle and the Jackdaw"
	""
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
