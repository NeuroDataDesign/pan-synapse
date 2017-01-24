import sys
sys.path.insert(0, '../functions/')
import plosLib as pLib
import connectLib as cLib
from cluster import Cluster
import mouseVis as mv
import tiffIO as tIO
import cv2
import numpy as np
import visualize as vis
import cPickle as pickle

data0 = tIO.unzipChannels(tIO.loadTiff('../../data/SEP-GluA1-KI_tp1.tif'))[0][5:10]
#finding the clusters after plosPipeline - list the decayed clusters
plosOut = pLib.pipeline(data0)
bianOut = cLib.otsuVox(plosOut)
connectList = cLib.connectedComponents(bianOut)
#threshold decayed clusters (get rid of background)
threshClusterList = cLib.thresholdByVolumeNaive(connectList, 200)


#pickle.dump(threshClusterList, open('plos.clusters', 'w'))

#finding the clusters without plosPipeline - lists the entire clusters
bianRawOut = cLib.binaryThreshold(data0)
clusterRawList = cLib.connectedComponents(bianRawOut)
clusterRawThreshList = cLib.thresholdByVolumeNaive(clusterRawList, 200)


#pickle.dump(clusterRawThreshList, open('raw.clusters', 'w'))

#final clusters
completeClusterList = cLib.clusterCoregister(threshClusterList, clusterRawThreshList)
pickle.dump(completeClusterList, open('complete.clusters', 'w'))

#completeClusterList = pickle.load(open('complete.clusters', 'rb'))
#visualize
vis.visualize(2, data0, completeClusterList)
