import sys
sys.path.insert(0, '../functions/')
import cv2
import plosLib as pLib
import connectLib as cLib
from cluster import Cluster
import mouseVis as mv
import tiffIO as tIO
import cPickle as pickle
import hyperReg as hype
from scipy import ndimage
import matplotlib.pyplot as plt

def analyzeTimepoint(tiffImage, plosNeighborhood, plosLowerZBound, plosUpperZBound, debug=False):
    #finding the clusters after plosPipeline
    plosOut = pLib.pipeline(tiffImage, plosNeighborhood, plosLowerZBound, plosUpperZBound)

    #binarize output of plos lib
    bianOut = cLib.otsuVox(plosOut)

    #dilate the output based on neigborhood size
    for i in range(int((plosNeighborhood+plosUpperZBound+plosLowerZBound)/3.)):
        bianOut = ndimage.morphology.binary_dilation(bianOut).astype(int)

    #run connected component
    connectList = cLib.connectedComponents(bianOut)

    if debug:
        return connectList, bianOut

    return connectList

def pipeline(tiffDict,
             plosNeighborhood=1,
             plosLowerZBound=1,
             plosUpperZBound=1,
             volThreshLowerBound=111,
             volThreshUpperBound=158,
             meanNormSlices = True,
             verbose = False):

    #perform normalization pre-processing if requested
    if meanNormSlices:
        tiffDict = cLib.meanNorm(tiffDict)

    #initialize a container for the results of each volume
    resList = []
    total = len(tiffDict)
    for num, tiffImage in enumerate(tiffDict):

        if verbose:
            print 'Progress: ', num/float(total)


        #get the conneted components from the current time point
        connectList = analyzeTimepoint(tiffImage, plosNeighborhood, plosLowerZBound, plosUpperZBound)

        #threshold decayed clusters (get rid of background and glia cells)
        threshClusterList = cLib.thresholdByVolumeNaive(connectList, lowerLimit = volThreshLowerBound, upperLimit = volThreshUpperBound)

        #append the current results to the
        resList.append(threshClusterList)

    #initialize a container for the pairing
    regList = []

    #minus 1 since the last cluster cant be registered to anything
    for num in range(len(resList)-1):
        regList.append(hype.simpleRegister(resList[num], resList[num+1]))

    #now that the pair list is populated, resolve it to a sequence
    seq = hype.resolve(regList)

    finalList = []

    #convert the sequence to a set of data points
    for thread in seq:
        curVolThread = []
        for timePoint in range(len(thread)):
            curCluster = resList[timePoint][thread[timePoint]]
            curVolThread.append(curCluster.volume)
        finalList.append(curVolThread)

    return finalList
