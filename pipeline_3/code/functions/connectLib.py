import sys
sys.path.insert(0, '../functions/')

import time
import pickle
import random

import numpy as np

import scipy.ndimage as ndimage

from scipy import sparse
from cluster import Cluster
from skimage.measure import label
from skimage.filters import threshold_otsu


def getCentroidList(clusterList):
    centroidList = [elem.getCentroid() for elem in clusterList]
    return centroidList

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


def clusterThresh(volume, lowerFence=0, upperFence=250):
    # the connectivity structure matrix
    s = [[[1 for k in xrange(3)] for j in xrange(3)] for i in xrange(3)]

    # find connected components
    labeled, nr_objects = ndimage.label(volume, s)

    #convert labeled to Sparse
    sparseLabeledIm = np.empty(len(labeled), dtype=object)
    for i in range(len(labeled)):
        sparseLabeledIm[i] = sparse.csr_matrix(labeled[i])

    clusterList = []

    #converting to clusterList
    for label in range(1, nr_objects + 1):

        memberList = []

        for z in range(len(sparseLabeledIm)):
            memberListWithoutZ = np.argwhere(sparseLabeledIm[z] == label)
            memberListWithZ = [[z] + list(tup) for tup in memberListWithoutZ]
            memberList.extend(memberListWithZ)

        #volume thresholding
        if len(memberList) < upperFence and len(memberList) > lowerFence:
            clusterList.append(Cluster(memberList))

    return clusterList


def clusterAnalysis(rawData, lowerFence = 20, upperFence = 250, sliceVis=5, bins=50):
    plt.imshow(rawData[sliceVis])
    plt.title('Slice of Clusters Without Uniform Intensities at z=' + str(sliceVis))
    plt.axis('off')
    plt.show()
    clusterList = clusterThresh(rawData, lowerFence, upperFence)
    volumeList = []
    print "Number of clusters: " + str(len(clusterList))
    displayIm = np.zeros_like(rawData)
    for cluster in range(len(clusterList)):
        volumeList.append(clusterList[cluster].getVolume())
        for member in range(len(clusterList[cluster].members)):
            z, y, x = clusterList[cluster].members[member]
            displayIm[z][y][x] = 1
    print "Average Volume: " + str(np.mean(volumeList))
    shape = rawData.shape
    print "Cluster Density: " + str(1.0*np.sum(volumeList)/(shape[0]*shape[1]*shape[2]))
    plt.imshow(displayIm[sliceVis], cmap='gray')
    plt.title('Slice of Clusters With Uniform Intensities at z=' + str(sliceVis))
    plt.axis('off')
    plt.show()
    mv.generateVoxHist(volumeList, figName='Volume Distribution', bins=bins, axisStart=lowerFence, axisEnd=upperFence, xTitle='Volume', yTitle="Number of Clusters")
    zRelationship = np.zeros(len(displayIm))
    for z in range(len(displayIm)):
        zRelationship[z] = np.mean(displayIm[z])
    mv.generatePlotlyLineForSliceDensities(zRelationship, figName="Z-Slice Densities")
    yRelationship = np.zeros(len(displayIm[0]))
    for y in range(len(displayIm[0])):
        yRelationship[y] = np.mean(displayIm[:, y])
    mv.generatePlotlyLineForSliceDensities(yRelationship, figName="Y-Slice Densities")
    xRelationship = np.zeros(len(displayIm[0][0]))
    for x in range(len(displayIm[0][0])):
        xRelationship[x] = np.mean(displayIm[:, :, x])
    mv.generatePlotlyLineForSliceDensities(xRelationship, figName="X-Slice Densities")


def noiseSuppression(clusterList, image, z):
    randClusterDist = []
    for i in range(100000):
        point = [int(random.random()*image.shape[0]), int(random.random()*image.shape[1]), int(random.random()*image.shape[2])]
        randClusterDist.append(image[point[0]][point[1]][point[2]])

    mu = np.average(randClusterDist)
    sigma = np.std(randClusterDist)

    aveList = []
    for cluster in clusterList:
        curClusterDist = []
        for member in cluster.members:
            curClusterDist.append(image[member[0]][member[1]][member[2]])
        aveList.append(np.mean(curClusterDist))

    finalClusters = []
    for i in range(len(aveList)): #this is bad and i should feel bad
        if (aveList[i] - mu)/float(sigma) > z:
            finalClusters.append(clusterList[i])

    return finalClusters


def generateAnnotations(clusterList, originalData):
    outVol = np.zeros_like(originalData)
    for cluster in clusterList:
        for member in cluster.members:
            outVol[member[0]][member[1]][member[2]] = 1

    return outVol
