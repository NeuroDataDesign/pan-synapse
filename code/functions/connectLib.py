import sys
sys.path.insert(0, '../functions/')
from skimage.filters import threshold_otsu
from skimage.measure import label
from cluster import Cluster
import numpy as np
import cv2
import plosLib as pLib
import pickle

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

def connectedComponents(volume):
    # the connectivity structure matrix
    s = [[[1 for k in xrange(3)] for j in xrange(3)] for i in xrange(3)]

    # find connected components
    labeled, nr_objects = ndimage.label(volume, s)

    #change them to object type Cluster
    if nr_objects == 1:
        nr_objects += 1
    clusterList = []


    for label in range(0, nr_objects):
        memberList = np.argwhere(labeled == label)
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
    return str(clusterPerPixelCubed/(.12*.12*.5)) + 'clusters per cubic microns'

#pass in list of clusters, return a list of thresholded clusters
def thresholdByVolumePercentile(clusterList):
    #putting the plosPipeline clusters volumes in a list
    plosClusterVolList =[]
    for cluster in (range(len(clusterList))):
        plosClusterVolList.append(clusterList[cluster].getVolume())

    #finding the upper outlier fence
    Q3 = np.percentile(plosClusterVolList, 75)
    Q1 = np.percentile(plosClusterVolList, 25)
    IQR = Q3 - Q1
    upperThreshFence = Q3 + 1.5*IQR
    lowerThreshFence = Q1 - 1.5*IQR

    #filtering out the background cluster
    upperThreshClusterList = []
    for cluster in (range(len(clusterList))):
        if clusterList[cluster].getVolume() < upperThreshFence:
            upperThreshClusterList.append(clusterList[cluster])

    return upperThreshClusterList

#pass in list of clusters, return a list of thresholded clusters
def thresholdByVolumeNaive(clusterList, lowerLimit = 0, upperLimit=200):

    #filtering out the background cluster
    naiveThreshClusterList = []
    for cluster in (range(len(clusterList))):
        if clusterList[cluster].getVolume() > lowerLimit and clusterList[cluster].getVolume() < upperLimit:
            naiveThreshClusterList.append(clusterList[cluster])

    return naiveThreshClusterList

#pass in the list of clusters that have gone through the plos pipeline, and the list that hasn't
def clusterCoregister(plosClusterList, rawClusterList):
    #creating a list of all the member indices of the plos cluster list
    plosClusterMemberList = []
    for cluster in range(len(plosClusterList)):
        plosClusterMemberList.extend(plosClusterList[cluster].members)

    #creating a list of all the clusters without any decay
    finalClusterList =[]
    for rawCluster in range(len(rawClusterList)):
        if any(i for i in rawClusterList[rawCluster].members if i in plosClusterMemberList) and not(rawClusterList[rawCluster] in finalClusterList):
            finalClusterList.append(rawClusterList[rawCluster])

    return finalClusterList

def adaptiveThreshold(img, blockSize=61, C=6):
    img = (img/256).astype('uint8')
    threshImg = np.zeros_like(img)
    for i in range(len(img)):
        threshImg[i] = cv2.adaptiveThreshold(img[i], 255, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=blockSize, C=C)
    return threshImg

def binaryThreshold(img):
    img = (img/256).astype('uint8')
    threshImg = np.zeros_like(img)
    percentile = np.percentile(img, 90)
    for i in range(len(img)):
        threshImg[i] = cv2.threshold(img[i], percentile, 255, cv2.THRESH_BINARY)[1]
    return threshImg
