from .search import Search
from .wikipedia import Wikipedia

import os, sys
path = os.path.abspath(os.path.join('..', 'k3s_utility'))
sys.path.append(path)
import k3s_utility
