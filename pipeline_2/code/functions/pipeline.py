import sys
import pickle

import numpy as np
import tiffIO as io

from neuroGraphLib import neuroGraph, generateNeuroGraphStack, getSynapseROIs

def pipeline(data):

    neuroGraphStack = generateNeuroGraphStack(data)
    synapseROIList = [getSynapseROIs(neuroGraphStack[idx], data[idx]) for idx in range(data.shape[0])]
    synapseStack = resolveROIList(synapseROIList, data)
    return synapseStack
    
if __name__ == '__main__':
    data = np.array(io.loadTiff(sys.argv[1]))
    output = pipeline(data)
    pickle.dump(output, open('out.dat', 'w'))
