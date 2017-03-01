import K3S


identifier = 'Bukhari'
processor = K3S.TopologyProcessor(identifier)
#processor.topologySetUp()
#processor.saveBlocksInMysql()
#processor.calculateTfIdf()
processor.generateLocalContextImages(1)






