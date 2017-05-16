import sys
import pickle

import numpy as np
import matIO as io

import connectLib as cLib

def pipeline(data):
    otsuOut = cLib.otsuVox(data)
    clusterList = cLib.clusterThresh(otsuOut, 500, 1000000)
    myCentroids = cLib.getCentroidList(clusterList)
    maximaList = cLib.nonMaximaSuppression(clusterList, data, thresh=47)
    annotations = cLib.generateAnnotations(clusterList, data)

    return annotations, myCentroids

if __name__ == '__main__':
    if len(sys.argv) !=1:
        print 'Usage:\n\tpython runPipeline.py <PSD95.mat>'
    data = np.array(io.loadMat(sys.argv[1]))
    annotation, centroidList = pipeline(data)
    pickle.dump(output, open('annotations.pickle', 'w'))
    pickle.dump(centroidList, open('centroids.pickle', 'w'))
