import sys
sys.path.insert(0, '../functions/')
import plosLib as plos
import connectLib as cLib
from cluster import Cluster
import mouseVis as mv
import tiffIO as tIO
import cv2
import numpy as np
import visualize as vis
import cPickle as pickle

data0 = tIO.unzipChannels(tIO.loadTiff('../../data/SEP-GluA1-KI_tp1.tif'))[0][5:10]

#PLOS pipeline
plosOut = plos.pipeline(data0, neighborhood = 1)
#Otsu's Method
bianOut = cLib.otsuVox(plosOut)
#Connected Components
connectList = cLib.connectedComponents(bianOut)
#Removing outlier clusters (background, noise)
connectList = cLib.thresholdBackground(connectList)

print 'done finding plos clusters'
#finding the clusters without plosPipeline - lists the entire clusters
bianRawOut = cLib.otsuVox(data0)
clusterRawList = cLib.connectedComponents(bianRawOut)
threshClusterList = cLib.naiveThreshold(clusterRawList)
print 'done finding raw clusters'
#Coregistering clusters with raw data
completeClusterList = cLib.clusterCoregister(connectList, clusterRawList)
print 'done finding final clusters'

pickle.dump(threshClusterList, open('coregistered.clusters', 'w'))
print 'done pickling clusters'

#visualize
completeClusterList = pickle.load(open('coregistered.clusters', 'r'))
completeClusterVolumes = []
for cluster in completeClusterList:
    completeClusterVolumes.append(cluster.getVolume())
print completeClusterVolumes
print completeClusterList
vis.visualize(1, data0, completeClusterList)
