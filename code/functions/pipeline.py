import sys
sys.path.insert(0, '../functions/')
import plosLib as pLib
import connectLib as cLib
from cluster import Cluster
import mouseVis as mv
import tiffIO as tIO
import visualize as vis
import cPickle as pickle
from scipy import ndimage
#Takes in tiffimage file and z slice that you want to visualize

def pipeline(tiffImage,
             visSlice=1,
             plosNeighborhood=1,
             plosLowerZBound=1,
             plosUpperZBound=1,
             volThreshLowerBound=0,
             volThreshUpperBound=50):

    #uplod the data
    data0 = tIO.unzipChannels(tIO.loadTiff(tiffImage))[0][5:10]

    #finding the clusters after plosPipeline
    print "Finding clusters"
    plosOut = pLib.pipeline(data0, plosNeighborhood, plosLowerZBound, plosUpperZBound)

    #binarize output of plos lib
    bianOut = cLib.otsuVox(plosOut)


    #dilate the output based on neigborhood size
    for i in range(int((plosNeighborhood+plosUpperZBound+plosLowerZBound)/3.)):
        bianOut = ndimage.morphology.binary_dilation(bianOut).astype(int)

    #run connected component
    connectList = cLib.connectedComponents()

    #threshold decayed clusters (get rid of background and glia cells)
    threshClusterList = cLib.thresholdByVolumeNaive(connectList, lowerLimit = 0, upperLimit = 50)

    print "Done finding clusters"
    print "Visualizing Results At z=" + str(visSlice)
    #visualize
    image = vis.visualize(visSlice, data0, threshClusterList)
    return (image, threshClusterList)
