import K3S


identifier = 'Bukhari'
processor = K3S.TopologyProcessor(identifier)
processor.topologySetUp()
processor.saveBlocksInMysql(None)
processor.calculateTfIdf()
processor.stopWordsUpdate()
processor.calculateLocalContextImportance()
processor.calculateWordZone()
processor.buildCloud()
processor.buildTextCloud()
