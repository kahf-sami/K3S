from .processor import Processor

import os, sys, re, math
path = os.path.abspath(os.path.join('..', 'k3s_utility'))
sys.path.append(path)
import k3s_utility

path = os.path.abspath(os.path.join('..', 'k3s_ws'))
sys.path.append(path)
import k3s_ws


path = os.path.abspath(os.path.join('..', 'k3s_lc'))
sys.path.append(path)
import k3s_lc
