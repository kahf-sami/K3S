from .textToMatrix import TextToMatrix
from .processor import Processor


import os, sys
path = os.path.abspath(os.path.join('..', 'k3s_utility'))
sys.path.append(path)
import k3s_utility


import os, sys
path = os.path.abspath(os.path.join('..', 'k3s_lc'))
sys.path.append(path)
import k3s_lc