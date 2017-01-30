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

def pipeline(tiffImage, visSlice=1):
    data0 = tIO.unzipChannels(tIO.loadTiff(tiffImage))[0][5:10]
    #finding the clusters after plosPipeline - list the decayed clusters
    print "Finding clusters"
    plosOut = pLib.pipeline(data0)
    bianOut = cLib.otsuVox(plosOut)
    connectList = cLib.connectedComponents(ndimage.morphology.binary_dilation(bianOut).astype(int))
    #threshold decayed clusters (get rid of background and glia cells)
    threshClusterList = cLib.thresholdByVolumeNaive(connectList, lowerLimit = 0, upperLimit = 50)
    #NOTE: add in cluster dilation here

    #pickle.dump(threshClusterList, open('plos.clusters', 'w'))

    #pickle.dump(completeClusterList, open('complete.clusters', 'w'))
    print "Done finding clusters"
    print "Visualizing Results At z=" + str(visSlice)
    #completeClusterList = pickle.load(open('complete.clusters', 'rb'))
    #visualize
    image = vis.visualize(visSlice, data0, threshClusterList)
    return (image, threshClusterList)
    #return (image, threshClusterList)

####Testing Code
#    pipeline('../../data/SEP-GluA1-KI_tp1.tif')
