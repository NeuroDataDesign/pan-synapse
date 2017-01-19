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


data0 = tIO.unzipChannels(tIO.loadTiff('../../data/SEP-GluA1-KI_tp1.tif'))[0][5:10]
#PLOS pipeline
plosOut = plos.pipeline(data0, neighborhood = 1)
#Otsu's Method
bianOut = cLib.otsuVox(plosOut)
#Connected Components
connectList = cLib.connectedComponents(bianOut)
#Removing outlier clusters (background, noise)
threshClusterList = cLib.thresholdByVolume(connectList)

#finding the clusters without plosPipeline - lists the entire clusters
bianRawOut = cLib.otsuVox(data0)
clusterRawList = cLib.connectedComponents(bianRawOut)

#Coregistering clusters with raw data
completeClusterList = cLib.clusterCoregister(threshClusterList, clusterRawList)

print 'done finding clusters'
#visualize
vis.visualize(3, data0, completeClusterList)
