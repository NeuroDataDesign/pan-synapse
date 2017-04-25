import sys
sys.path.insert(0, '../functions/')

import cv2
import quality

from cluster import Cluster
from scipy import ndimage
from neighborhoodLib import neighborhoodDensity
from tiffIO  import unzipChannels
import connectLib as cLib
import mouseVis as mv
import registration as rLib
import tiffIO as tIO
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import scipy.misc

import scipy.ndimage as ndimage

def pipeline(fixedImg, movingImg, lowerFence = 0, upperFence = 180):

    fixedImgLandmarks = fixedImg[1]
    movingImgLandmarks = movingImg[1]

    print('running adaptive threshold')
    fixedImg = cLib.adaptiveThreshold(fixedImg[0], 64, 64)
    movingImg = cLib.adaptiveThreshold(movingImg[0], 64, 64)
    ##Volume Thresholding Fixed Img

    print('performing knn filtering')
    #perform knn filtering
    fixedImg = cLib.knn_filter(fixedImg, 2)
    movingImg= cLib.knn_filter(movingImg, 2)

    # the connectivity structure matrix
    s = [[[1 for k in xrange(3)] for j in xrange(3)] for i in xrange(3)]

    print('ANTs transformation')
    realFixedClusters = rLib.ANTs(fixedImg, movingImg, fixedImgLandmarks, movingImgLandmarks, lowerFence, upperFence)

    print('correcting mismatches')
    #filtering wrong ones
    for i in range(len(realFixedClusters)):
        volumeChangeForwards = np.abs(realFixedClusters[i].volume - realFixedClusters[i].timeRegistration.volume)/np.abs(realFixedClusters[i].volume)
        volumeChangeBackwards = np.abs(realFixedClusters[i].volume - realFixedClusters[i].timeRegistration.volume)/np.abs(realFixedClusters[i].timeRegistration.volume)
        if not (volumeChangeForwards < 2 and volumeChangeBackwards < 2):
            realFixedClusters[i].timeRegistration.members = (-1, -1, -1)
            realFixedClusters[i].timeRegistration.volume = -1

    return realFixedClusters
