import sys
import k3s_cnn

text1 = ('Narrated Abu Said Al-Khudri: The Prophet said, "When the people of Paradise will enter Paradise and the people of '
		'Hell will go to Hell, Allah will order those who have had faith equal to the weight of a grain of mustard seed to be '
		'taken out from Hell. So they will be taken out but (by then) they will be blackened (charred).'
		' Then they will be put in the river of Haya (rain) or Hayat (life) (the Narrator is in doubt as to which is the right term), '
		'and they will revive like a grain that grows near the bank of a flood channel. Don\'t you see that it comes out yellow and twisted"')

textToMatrix = k3s_cnn.TextToMatrix()


textToMatrix.setText(text1)
print_r(textToMatrix.getMatrix())


