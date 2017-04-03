import K3S


identifier = 'bhot'

#fileProcessor = K3S.Processor(identifier)
#fileProcessor.clean()
#fileProcessor.createSourceSetup()
#fileProcessor.copy('/home/ishrat/research/K3S/data/stephen_hawking_a_brief_history_of_time.pdf')
#fileProcessor.extractBlocks()


processor = K3S.TopologyProcessor(identifier)
#processor.topologySetUp()
#processor.saveBlocksInMysql(None, True)
#processor.calculateTfIdf()
#processor.stopWordsUpdate()
#processor.calculateWordZone()
#processor.calculateLocalContextImportance()
#processor.buildCloud(True)

#processor.buildTextCloud(True)
#processor.generateLocalContextImages(1)
#processor.buildGlobalWord()
processor.buildGlobalText()