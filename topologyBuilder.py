import sys
import K3S
import colorama
import scipy
import numpy

processor = K3S.Processor('Bukhari')
#processor.topologySetUp()
#processor.topologyBuilder()
processor.contextExtraction()