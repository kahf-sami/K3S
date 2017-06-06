import sys
import k3s_ws

searcher = k3s_ws.Search()
searcher.process('Isaac Newton')
getMostRelevantWikiLink = searcher.getMostRelevantLink()
#print(getMostRelevantWikiLink)

print('---------- start -----------------')
if getMostRelevantWikiLink:
	wikipidia = k3s_ws.Wikipedia(getMostRelevantWikiLink)
	wikipidia.processLocalContext()
	print('Url: ' + getMostRelevantWikiLink)
	print('Description: ' + wikipidia.fetchNext())
	print('Concepts')
	print(wikipidia.getImportantConcepts())
else:
	print('No information found')

print('---------- End -----------------')