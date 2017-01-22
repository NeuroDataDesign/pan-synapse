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
def naiveThreshold(clusterList):
    #putting the finalclusters volumes in a list
    finalClusterList =[]
    for cluster in clusterList:
        if cluster.getVolume() > 3 and cluster.getVolume() < 104:
            finalClusterList.append(cluster)

    #finding the upper outlier fence
    '''
    Q3 = np.percentile(finalClusterVolList, 75)
    Q1 = np.percentile(finalClusterVolList, 25)
    IQR = Q3 - Q1
    upperThreshFence = Q3 + 1.5*IQR

    #filtering out the background cluster
    upperThreshClusterList = []
    for cluster in (range(len(clusterList))):
        if clusterList[cluster].getVolume() < upperThreshFence:
            upperThreshClusterList.append(clusterList[cluster])
            '''
    return finalClusterList

def getClusterVolumes(clusterList):
    clusterVols = []
    for cluster in clusterList:
        clusterVols.append(cluster.getVolume())
    return clusterVols

def thresholdBackground(plosClusterList):
    plosClusterVolumes = getClusterVolumes(plosClusterList)
    #finding the upper outlier fence
    Q3 = np.percentile(plosClusterVolumes, 75)
    Q1 = np.percentile(plosClusterVolumes, 25)
    IQR = Q3 - Q1
    upperThreshFence = Q3 + 1.5*IQR
    finalPlosList = []
    #filtering out the background cluster
    for i in range(len(plosClusterList)):
        if plosClusterList[i].getVolume() < upperThreshFence:
            finalPlosList.append(plosClusterList[i])

    return finalPlosList

#pass in the list of clusters that have gone through the plos pipeline, and the list that hasn't
def clusterCoregister(plosClusterList, rawClusterList):
    #creating a list of all the clusters without any decay
    finalClusterList =[]
    for rawCluster in rawClusterList:
        for cluster in plosClusterList:
            if any(member in rawCluster.getMembers() for member in cluster.getMembers()):
                finalClusterList.append(rawCluster)

    return finalClusterList
