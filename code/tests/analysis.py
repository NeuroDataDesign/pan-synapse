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
data0 = tIO.unzipChannels(tIO.loadTiff('../../data/SEP-GluA1-KI_tp1.tif'))[0][5:10]

#Outdated TODO: change this to pipelineTest.py

#clusters = cLib.completePipeline(data0)
pickle.dump(clusters, open('./synthDat/pipeline.clusters', 'w'))
