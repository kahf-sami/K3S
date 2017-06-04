import sys
import K3S

searcher = K3S.Search()
searcher.process('Isaac Newton')
getMostRelevantWikiLink = searcher.getMostRelevantLink()
#print(getMostRelevantWikiLink)

print('---------- start -----------------')
if getMostRelevantWikiLink:
	wikipidia = K3S.Wikipedia(getMostRelevantWikiLink)
	wikipidia.processLocalContext()
	print('Url: ' + getMostRelevantWikiLink)
	print('Description: ' + wikipidia.fetchNext())
	print('Concepts')
	print(wikipidia.getImportantConcepts())
else:
	print('No information found')

print('---------- End -----------------')