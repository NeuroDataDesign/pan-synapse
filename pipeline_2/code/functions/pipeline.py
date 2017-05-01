import sys
import pickle

import numpy as np
import tiffIO as io

from neuroGraphLib import neuroGraph, generateNeuroGraphStack

def pipeline(data):

    neuroGraphStack = generateNeuroGraphStack(data)
    return

if __name__ == '__main__':
    data = io.loadTiff(sys.argv[1])
    output = pipeline(data[15:17])
