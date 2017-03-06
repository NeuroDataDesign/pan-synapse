import sys
sys.path.insert(0, '../functions/')
sys.path.insert(0, '../tests/')

import cv2
import quality

from cluster import Cluster
from scipy import ndimage
from neighborhoodLib import neighborhoodDensity

import connectLib as cLib
import mouseVis as mv
import tiffIO as tIO
import cPickle as pickle
import hyperReg as hype
import matplotlib.pyplot as plt

#z zBound, xBound, and yBound are for generating annotations (define image size)
def analyzeTimepoint(tiffImage,
                     interPlane=3,
                     intraPlane=3,
                     lowerVolThresh = 100,
                     upperVolThresh=250,
                     debug=False,
                     QA=False,
                     vis=False,
                     returnBinary=False):

    #run through the neigborhood density filter
    neighborhoodOut = neighborhoodDensity(tiffImage, interPlane=interPlane, intraPlane=3)

    #binarize output of neighborhood pipeline
    bianOut = cLib.otsuVox(neighborhoodOut)

    #perform volume thresholding
    connectList = cLib.clusterThresh(bianOut, lowerVolThresh, upperVolThresh)

    if QA:
        qualityAssurance(connectList)

    if returnBinary:
        return connectList, bianOut

    return connectList

def qualityAssurance(clusterList, zBound=280, yBound=1024, xBound=1024):
    quality.getNumClusters(clusterList)
    annotations = mv.generateAnnotations(clusterList, zBound, yBound, xBound)
    quality.getAverageVolume(annotations)
    quality.getPercentDetected(annotations)
    quality.getVolumeHistogram(clusterList, "Volume Distribution")

def pipeline(tiffDict,
             interPlane=3,
             intraPlane=3,
             volThreshLowerBound=10,
             volThreshUpperBound=250,
             meanNormSlices = True,
             verbose = False,
             returnBinary = False):

    #perform normalization pre-processing if requested
    if meanNormSlices:
        tiffDict = cLib.windowMeanShiftNorm(tiffDict, 4)

    #Generate the Cluster Lists
    if not returnBinary:
        connectList = analyzeTimepoint(tiffDict,
                                       interPlane,
                                       intraPlane,
                                       volThreshLowerBound,
                                       volThreshUpperBound,
                                       QA=verbose,
                                       returnBinary=False)
        return connectList

    else:
        connectList, binary = analyzeTimepoint(tiffDict,
                                               interPlane,
                                               intraPlane,
                                               volThreshLowerBound,
                                               volThreshUpperBound,
                                               QA=verbose,
                                               returnBinary=True)
        return connectList, binary



    '''
    #initialize a container for the results of each volume
    resList = []
    total = len(tiffDict)
    for num, tiffImage in enumerate(tiffDict):

        if verbose:
            print 'Progress: ', num/float(total)


        #get the conneted components from the current time point
        connectList = analyzeTimepoint(tiffImage,
                                       percentile,
                                       volThreshLowerBound,
                                       volThreshUpperBound)
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
    '''
