import sys

import numpy as np
import matplotlib.pyplot as plt

from skimage.measure import label
from cluster import Cluster

def getPercentDetected(annotations):
    if len(annotations.shape)==3:
        return np.count_nonzero(annotations)/float(annotations.shape[0] * annotations.shape[1] * annotations.shape[2])
    elif len(annotations.shape)==2:
        return "Percent Detected: " + str(np.count_nonzero(annotations)/float(annotations.shape[0] * annotations.shape[1]))

def getAverageVolume(annotations):
    numClusters = np.max(label(annotations))
    return "Average Volume: " + str(np.count_nonzero(annotations)/float(numClusters))

def getVolumeHistogram(clusterList, title=None):
    fig = plt.figure()
    if not title is None:
        plt.title(title)
    volList = [elem.getVolume for elem in clusterList]
    plt.hist(volList)
    plt.show()
    return

def getNumClusters(clusterList):
    return "Number of Clusters: " + str(len(clusterList))
