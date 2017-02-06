import sys
import K3S
import colorama
import scipy
import numpy


#processor = K3S.Processor('Bukhari') 
#processor.calculateLDA(500, 10)
#processor.calculateLDA(500, 20)
#processor.calculateLDA(500, 50)

#processor.calculateLDA(300, 10)
#processor.calculateLDA(300, 20)
#processor.calculateLDA(300, 50)

#processor.calculateLDA(100, 10)
#processor.calculateLDA(100, 20)
#processor.calculateLDA(100, 50)

#processor.calculateLDA(50, 10)
#processor.calculateLDA(50, 20)
#processor.calculateLDA(50, 50)


processor = K3S.Processor('tpl') 
processor.calculateLDA(500, 10)
processor.calculateLDA(500, 20)
processor.calculateLDA(500, 50)

#processor.calculateLDA(300, 10)
processor.calculateLDA(300, 20)
processor.calculateLDA(300, 50)

processor.calculateLDA(100, 10)
processor.calculateLDA(100, 20)
processor.calculateLDA(100, 50)

processor.calculateLDA(50, 10)
processor.calculateLDA(50, 20)
processor.calculateLDA(50, 50)

