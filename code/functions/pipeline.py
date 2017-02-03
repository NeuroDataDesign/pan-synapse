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
#Takes in tiffimage file and z slice that you want to visualize

def pipeline(tiffDict,
             plosNeighborhood=1,
             plosLowerZBound=1,
             plosUpperZBound=1,
             volThreshLowerBound=0,
             volThreshUpperBound=50,
             verbose = False):

    #initialize a container for the results of each volume
    resList = []
    total = len(resDict)
    for num, tiffImage in enumerate(tiffDict):

        if verbose:
            print 'Progress: ', num/float(total)

        #uplod the data
        data0 = tIO.unzipChannels(tIO.loadTiff(tiffImage))[0][5:10]

        #finding the clusters after plosPipeline
        plosOut = pLib.pipeline(data0, plosNeighborhood, plosLowerZBound, plosUpperZBound)

        #binarize output of plos lib
        bianOut = cLib.otsuVox(plosOut)

        #dilate the output based on neigborhood size
        for i in range(int((plosNeighborhood+plosUpperZBound+plosLowerZBound)/3.)):
            bianOut = ndimage.morphology.binary_dilation(bianOut).astype(int)

        #run connected component
        connectList = cLib.connectedComponents(bianOut)

        #threshold decayed clusters (get rid of background and glia cells)
        threshClusterList = cLib.thresholdByVolumeNaive(connectList, lowerLimit = 0, upperLimit = 50)

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
