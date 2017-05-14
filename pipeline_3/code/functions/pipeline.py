import sys
import pickle

import numpy as np
import matIO as io

import connectLib as cLib

def pipeline(data):
    otsuOut = cLib.otsuVox(data)
    clusterList = cLib.clusterThresh(otsuOut, 500, 1000000)
    maximaList = cLib.nonMaximaSuppression(clusterList, data, thresh=47)
    annotations = cLib.generateAnnotations(clusterList, data)
    return annotations

if __name__ == '__main__':
    if len(sys.argv) !=1:
        print 'Usage:\n\tpython runPipeline.py <PSD95.mat>'
    data = np.array(io.loadMat(sys.argv[1]))
    output = pipeline(data)
    pickle.dump(output, open('out.dat', 'w'))
