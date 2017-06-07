import sys, os
import k3s_lc
import k3s_utility

path = 'data/Bukhari/processed/Volume_1,_Book_1,_Number_4.txt'
os.path.abspath(path)
file = k3s_utility.File(path)
text = str(file.read())

lc = k3s_lc.LC()
lc.setText(text)
lc.process()
print(lc.getProperNouns())
print(lc.getContributers())
