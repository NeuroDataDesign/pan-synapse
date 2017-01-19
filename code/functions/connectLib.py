import sys
sys.path.insert(0, '../functions/')
from skimage.filters import threshold_otsu
from skimage.measure import label
from cluster import Cluster
import numpy as np
import cv2
import plosLib as pLib

def otsuVox(argVox):
    probVox = np.nan_to_num(argVox)
    bianVox = np.zeros_like(probVox)
    for zIndex, curSlice in enumerate(probVox):
        #if the array contains all the same values
        if np.max(curSlice) == np.min(curSlice):
            #otsu thresh will fail here, leave bianVox as all 0's
            continue
        thresh = threshold_otsu(curSlice)
        bianVox[zIndex] = curSlice > thresh
    return bianVox

def connectedComponents(voxel):
    labelMap = label(voxel)
    clusterList = []
    #plus 1 since max label should be included
    for uniqueLabel in range(0, np.max(labelMap)+1):
        memberList = [list(elem) for elem in zip(*np.where(labelMap == uniqueLabel))]
        if not len(memberList) == 0:
            clusterList.append(Cluster(memberList))
    return clusterList

#pass in list of clusters
def densityOfSlice(clusters, minZ, maxZ, minY, maxY, minX, maxX):
    count = 0
    for cluster in clusters:
        z, y, x = cluster.centroid
        #if cluster is in given volume
        if (z>=minZ) and (z<maxZ) and (y>=minY) and (y<maxY) and (x>=minX) and (x<maxX):
            count+=1

    clusterPerPixelCubed = float(count)/((maxX - minX) * (maxY - minY) * (maxZ - minZ))
    #NOTE .12*.12*.5 microns is the resolution of the given data, this may need to be changed
    #in future implementations for data of different resolutions
    return clusterPerPixelCubed/(.12*.12*.5)

#pass in list of clusters, return a list of thresholded clusters
def thresholdByVolume(clusterList):
    #putting the plosPipeline clusters volumes in a list
    plosClusterVolList =[]
    for cluster in (range(len(clusterList))):
        if clusterList[cluster].getVolume() > 5 and clusterList[cluster].getVolume() < 104:
            plosClusterVolList.append(clusterList[cluster].getVolume())

    #finding the upper outlier fence
    Q3 = np.percentile(plosClusterVolList, 75)
    Q1 = np.percentile(plosClusterVolList, 25)
    IQR = Q3 - Q1
    upperThreshFence = Q3 + 1.5*IQR

    #filtering out the background cluster
    upperThreshClusterList = []
    for cluster in (range(len(clusterList))):
        if clusterList[cluster].getVolume() < upperThreshFence:
            upperThreshClusterList.append(clusterList[cluster])

    return upperThreshClusterList

#pass in the list of clusters that have gone through the plos pipeline, and the list that hasn't
def clusterCoregister(plosClusterList, rawClusterList):
    #creating a list of all the member indices of the plos cluster list
    plosClusterMemberList = []
    for cluster in range(len(plosClusterList)):
        plosClusterMemberList.extend(plosClusterList[cluster].members)

    #creating a list of all the clusters without any decay
    finalClusterList =[]
    for rawCluster in range(len(rawClusterList)):
        for index in range(len(plosClusterMemberList)):
            if ((plosClusterMemberList[index] in rawClusterList[rawCluster].members) and (not(rawClusterList[rawCluster] in finalClusterList))):
                finalClusterList.append(rawClusterList[rawCluster])

    return finalClusterList
