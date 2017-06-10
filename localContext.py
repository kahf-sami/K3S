import sys, os
import k3s_lc
import k3s_utility

path = 'data/Bukhari/processed/Volume_1,_Book_1,_Number_4.txt'
#path = 'data/Bukhari/processed/Volume_1,_Book_1,_Number_6.txt'
os.path.abspath(path)
file = k3s_utility.File(path)
text = str(file.read())

lc = k3s_lc.LC()
lc.setText(text)
lc.process()
print(lc.getProperNouns())
[mostImportantWords , otherProperNouns] = lc.getContributers()
print('------------- MI --------------------')
print(mostImportantWords)
print('-------------- OPN --------------------')
print(otherProperNouns)

#sys.exit()
print('-------------- LO --------------------')
lo = k3s_lc.LO(mostImportantWords)
lo.process()


