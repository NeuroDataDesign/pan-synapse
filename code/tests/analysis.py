import sys
sys.path.insert(0, '../functions/')
from skimage.filters import threshold_otsu
from cluster import Cluster
import tiffIO as tIO
import mouseVis as mv
import plosLib as pLib
import connectLib as cLib
import matplotlib.pyplot as plt
import numpy as np
import cv2
import cPickle as pickle

#load the data
data0 = tIO.unzipChannels(tIO.loadTiff('../../data/SEP-GluA1-KI_tp1.tif'))[0][0:5]

#generate a foreground probability map for the data
probVox = pLib.pipeline(data0)

#get the otsu binarization of the supervoxel
bianVox = cLib.otsuVox(probVox)

#extract the clusters from the bianary voxel
clusters = cLib.connectedComponents(bianVox)

#generate a histogram to show distribution of cluster volumes
clusterVols = []
for i in range(len(clusters)):
    clusterVols.append(clusters[i].getVolume())
mv.generateHist(clusterVols, title = 'Cluster Volumes', bins = 100, axisStart = 0, axisEnd = 50)
