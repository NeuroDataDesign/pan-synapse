import sys
sys.path.insert(0, '../functions/')
import plosLib as pLib
import connectLib as cLib
from cluster import Cluster
import mouseVis as mv
import tiffIO as tIO
import visualize as vis
import cPickle as pickle
#Takes in tiffimage file and z slice that you want to visualize
def pipeline(tiffImage, visSlice=0):
    data0 = tIO.unzipChannels(tIO.loadTiff(tiffImage))[0][5:10]
    #finding the clusters after plosPipeline - list the decayed clusters
    plosOut = pLib.pipeline(data0)
    bianOut = cLib.otsuVox(plosOut)
    connectList = cLib.connectedComponents(bianOut)
    #threshold decayed clusters (get rid of background)
    threshClusterList = cLib.thresholdByVolumeNaive(connectList)

    #pickle.dump(threshClusterList, open('plos.clusters', 'w'))

    #finding the clusters without plosPipeline - lists the entire clusters
    bianRawOut = cLib.binaryThreshold(data0)
    clusterRawList = cLib.connectedComponents(bianRawOut)
    clusterRawThreshList = cLib.thresholdByVolumeNaive(clusterRawList)

    #pickle.dump(clusterRawThreshList, open('raw.clusters', 'w'))

    #final clusters
    completeClusterList = cLib.clusterCoregister(threshClusterList, clusterRawThreshList)
    #pickle.dump(completeClusterList, open('complete.clusters', 'w'))

    #completeClusterList = pickle.load(open('complete.clusters', 'rb'))
    #visualize
    vis.visualize(visSlice, data0, completeClusterList)


####Testing Code
#    pipeline('../../data/SEP-GluA1-KI_tp1.tif')
