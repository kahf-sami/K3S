#import K3S

identifier = 'Bukhari'
#processor = K3S.TopologyProcessor(identifier)
#processor.topologySetUp()
#processor.saveBlocksInMysql(None)
#processor.calculateTfIdf()
#processor.stopWordsUpdate()
#processor.calculateLocalContextImportance()
#processor.calculateWordZone()
#processor.buildCloud()
#processor.buildTextCloud()


#processor.buildTextNodeCloud(1)

#processor.generateLocalContextImages(1)


#wordCloud = K3S.WordCloud(identifier)
#wordCloud.savePoints()
#wordCloud.generateLGCsv()
'''
wC = K3S.WordContext(identifier, 'allah')
wC.generateLGCsv()

wC = K3S.WordContext(identifier, 'muhammad')
wC.generateLGCsv()

wC = K3S.WordContext(identifier, 'apostl')
wC.generateLGCsv()

wC = K3S.WordContext(identifier, 'prophet')
wC.generateLGCsv()

wC = K3S.WordContext(identifier, 'prayer')
wC.generateLGCsv()

wC = K3S.WordContext(identifier, 'aisha')
wC.generateLGCsv()

wC = K3S.WordContext(identifier, 'abu')
wC.generateLGCsv()

wC = K3S.WordContext(identifier, 'huraira')
wC.generateLGCsv()

wC = K3S.WordContext(identifier, 'peopl')
wC.generateLGCsv()
'''

import k3s_processor

processor = k3s_processor.Processor(identifier)
processor.setUpDb()
processor.saveBlocksInMysql()
print('end')



