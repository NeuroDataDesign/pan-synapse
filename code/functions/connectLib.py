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

def meanNorm(volume):
    toStack = []
    for plane in volume:
        normFactor = (65535./float(np.max(plane)))
        toStack.append(normFactor * np.array(plane))
    return np.stack(toStack)

def windowMeanShiftNorm(volume, window):
    retStack = []
    rem = volume.shape[0]%window
    for i in range(int(volume.shape[0])/int(window)):
        idealMean = np.average(volume[i])
        retStack.append(volume[i])
        #starts at 1 since ideal mean volume is normed to itself already
        for j in range(1, window):
            retStack.append(volume[i+j]+(idealMean-np.average(volume[i+j])))

    #deal with remainders
    idealRemMean = np.average(volume[-rem])
    for i in range(rem):
        retStack.append(volume[-rem+i]+(idealRemMean-np.average(volume[-rem+i])))

    return np.stack(retStack)

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

    #volume thresholding with upperFence
    mask = labeled > labeled.mean()
    sizes = ndimage.sum(mask, labeled, range(nr_objects + 1))
    mask_size = sizes > upperFence
    remove_pixel = mask_size[labeled]
    labeled[remove_pixel] = 0
    labeled, nr_objects = ndimage.label(labeled, s)

    if not lowerFence == 0:
        #volume thresholding with lowerFence
        mask = labeled > labeled.mean()
        sizes = ndimage.sum(mask, labeled, range(nr_objects + 1))
        mask_size = sizes < lowerFence
        remove_pixel = mask_size[labeled]
        labeled[remove_pixel] = 0
        labeled, nr_objects = ndimage.label(labeled, s)

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

        if not len(memberList) == 0:
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
                std = np.std(sub)/max
                p = 90 + 10*std
                subThresh = binaryThreshold(sub, p)
                outImg[(zInc-1)*subzLen: zInc*subzLen, (yInc-1)*subYLen: yInc*subYLen, (xInc-1)*subxLen: xInc*subxLen] = subThresh
    return outImg

def binaryThreshold(img, percentile=90):
    img = (img/256).astype('uint8')
    threshImg = np.zeros_like(img)
    percentile = np.percentile(img, percentile)
    for i in range(len(img)):
        threshImg[i] = cv2.threshold(img[i], percentile, 255, cv2.THRESH_TOZERO)[1]
    return threshImg
