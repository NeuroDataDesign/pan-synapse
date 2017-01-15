import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
import sys
sys.path.insert(0,'../code/functions/')
import connectLib as cLib
import plosLib as pLib
import mouseVis

def completePipeline(combinedIm, neighborhood = 1):
    #finding the clusters after plosPipeline - realistically lists the centers of the clusters
    plosOut = pLib.pipeline(combinedIm, neighborhood = neighborhood)
    bianOut = cLib.otsuVox(plosOut)
    connectList = cLib.connectedComponents(bianOut)

    upperThreshClusterList = cLib.thresholdByVolumePercentile(connectList)

    #finding the clusters without plosPipeline - lists the entire clusters
    bianRawOut = cLib.otsuVox(combinedIm)
    connectRawList = cLib.connectedComponents(bianRawOut)

    completeClusterMemberList = cLib.clusterCoregister(connectList, connectRawList)

    return completeClusterMemberList
