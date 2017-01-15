import sys
import K3S
import colorama
import scipy
import numpy

processor = K3S.Processor('tpl') 
#processor.topologySetUp()
#processor.topologyBuilder()
#processor.contextExtraction()
processor.addEdges()
