import K3S


identifier = 'Bukhari'
#processor = K3S.TopologyProcessor(identifier)
#processor.topologySetUp()
#processor.saveBlocksInMysql()
#processor.calculateTfIdf()
#processor.generateLocalContextImages(1)


#wordCloud = K3S.WordCloud(identifier)
#wordCloud.savePoints()
#wordCloud.generateLGCsv()


wC = K3S.WordContext(identifier, 'day')
wC.generateLGCsv()


