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

#pickle.dump(connectList, open('plos.clusters', 'w'))
#connectList = pickle.load(open('plos.clusters', 'rb'))

#finding the clusters without plosPipeline - lists the entire clusters

bianRawOut = cLib.otsuVox(data0)
clusterRawList = cLib.connectedComponents(bianRawOut)
threshRawClusterList = cLib.naiveThreshold(clusterRawList)

#pickle.dump(threshRawClusterList, open('raw.clusters', 'w'))
#threshRawClusterList = pickle.load(open('raw.clusters', 'rb'))

#Coregistering clusters with raw data
completeClusterList = cLib.clusterCoregister(connectList, threshRawClusterList)

#pickle.dump(completeClusterList, open('coregistered.clusters', 'w'))
#completeClusterList = pickle.load(open('coregistered.clusters', 'rb'))

#visualize
#completeClusterList = pickle.load(open('coregistered.clusters', 'r'))

#####Checking Volumes
#completeClusterVolumes = []
#for cluster in completeClusterList:
    #completeClusterVolumes.append(cluster.getVolume())
#print completeClusterVolumes
#print completeClusterList

vis.visualize(1, data0, connectList)
