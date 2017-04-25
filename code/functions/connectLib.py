import sys
sys.path.insert(0, '../functions/')
from skimage.filters import threshold_otsu
from skimage.measure import label
from cluster import Cluster
import numpy as np
import cv2
import plosLib as pLib
import pickle
import scipy.ndimage as ndimage
import time
from scipy import sparse
import matplotlib.pyplot as plt
import mouseVis as mv

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

def knn_filter(volume, n):
    #neighborList = []
    outVolume = np.zeros_like(volume)
    #for all voxels in volume
    for z in range(volume.shape[0]):
        for y in range(volume.shape[1]):
            for x in range(volume.shape[2]):
                #get all valid neighbors
                neighbors = []
                for a in (-1, 1):
                    try:
                        neighbors.append(volume[z][y+a][x])
                        neighbors.append(volume[z][y][x+a])

                    #just keep going and append nothing if on edge
                    except IndexError:
                        continue

                #if at least half of your neighbors are true, be true
                #neighborList.append(np.count_nonzero(neighbors))
                if np.count_nonzero(neighbors) >= n:
                    outVolume[z][y][x] = 1
                else:
                    outVolume[z][y][x] = 0

    return outVolume
    
def adaptiveThreshold(inImg, sx, sy):
    max = np.max(inImg)
    outImg = np.zeros_like(inImg)
    shape = outImg.shape
    sz = shape[0]
    subzLen = shape[0]/sz
    subYLen = shape[1]/sy
    subxLen = shape[2]/sx
    for zInc in range(1, sz + 1):
        for yInc in range(1, sy + 1):
            for xInc in range(1, sx + 1):
                sub = inImg[(zInc-1)*subzLen: zInc*subzLen, (yInc-1)*subYLen: yInc*subYLen, (xInc-1)*subxLen: xInc*subxLen]
                subThresh = binaryThreshold(sub, 90)
                outImg[(zInc-1)*subzLen: zInc*subzLen, (yInc-1)*subYLen: yInc*subYLen, (xInc-1)*subxLen: xInc*subxLen] = subThresh
    return outImg

def binaryThreshold(img, percentile=90):
    img = (img/256).astype('uint8')
    threshImg = np.zeros_like(img)
    percentile = np.percentile(img, percentile)
    for i in range(len(img)):
        threshImg[i] = cv2.threshold(img[i], percentile, 255, cv2.THRESH_TOZERO)[1]
    return threshImg
