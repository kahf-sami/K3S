import K3S


identifier = 'tpl'

processor = K3S.TopologyProcessor(identifier)

#processor.topologySetUp()
#processor.saveBlocksInMysql(None)
'''
processor.calculateTfIdf()
processor.stopWordsUpdate()
processor.calculateLocalContextImportance()
processor.calculateWordZone()

processor.buildCloud(True)
processor.buildTextCloud(True)
'''
#processor.buildGlobalWord()

processor.buildGlobalText()



#identifier = 'Bukhari'
#processor = K3S.TopologyProcessor(identifier)
#processor.topologySetUp()
#processor.saveBlocksInMysql(None)
#processor.calculateTfIdf()
#processor.stopWordsUpdate()
#processor.calculateLocalContextImportance()
#processor.calculateWordZone()
#processor.buildCloud(True)
#processor.buildTextCloud(True)
#processor.buildGlobalWord()
#processor.buildGlobalText()
