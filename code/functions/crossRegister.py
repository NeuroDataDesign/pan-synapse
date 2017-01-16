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

def getSynapseClusters(rawClusters, PlosClusters):
    synpaseClusters = []
    for cluster in rawClusters:
        for pCluster in PlosClusters:
            if(pCluster.members in cluster.members):
                 synapseClusters.append(cluster)
                 break
    return synapseClusters
