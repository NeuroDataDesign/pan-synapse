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

    #putting the plosPipeline clusters volumes in a list
    plosClusterVolList =[]
    for cluster in (range(len(connectList))):
        plosClusterVolList.append(connectList[cluster].getVolume())

    #finding the upper outlier fence
    upperThreshFence = 1.5*np.percentile(plosClusterVolList, 75)

    #filtering out the background cluster
    upperThreshClusterList = []
    for cluster in (range(len(connectList))):
        if connectList[cluster].getVolume() < upperThreshFence:
            upperThreshClusterList.append(connectList[cluster])

    #finding the clusters without plosPipeline - lists the entire clusters
    bianRawOut = cLib.otsuVox(combinedIm)
    connectRawList = cLib.connectedComponents(bianRawOut)

    #creating a list of all the member indices of the plos connectList
    plosClusterMemberList = []
    for cluster in range(len(connectList)):
        plosClusterMemberList.extend(connectList[cluster].members)

    #creating a list of all the clusters without any decay
    completeClusterMemberList =[]
    for rawCluster in range(len(connectRawList)):
        for index in range(len(plosClusterMemberList)):
            if plosClusterMemberList[index] in connectRawList[rawCluster].members:
                completeClusterMemberList.append(connectRawList[rawCluster])

    return completeClusterMemberList
