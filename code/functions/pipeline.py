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

def knn_filter(volume, n):
    #neighborList = []
    outVolume = np.zeros_like(volume)
    #for all voxels in volume
    for z in range(volume.shape[0]):
        for y in range(volume.shape[1]):
            for x in range(volume.shape[2]):
                #get all valid neighbors
                neighbors = []
                for a in (-1, 1):
                    try:
                        neighbors.append(volume[z][y+a][x])
                        neighbors.append(volume[z][y][x+a])

                    #just keep going and append nothing if on edge
                    except IndexError:
                        continue

                #if at least half of your neighbors are true, be true
                #neighborList.append(np.count_nonzero(neighbors))
                if np.count_nonzero(neighbors) >= n:
                    outVolume[z][y][x] = 1
                else:
                    outVolume[z][y][x] = 0

    return outVolume

def pipeline(fixedImg, movingImg, lowerFence = 0, upperFence = 180):

    print 'running adaptive threshold'
    fixedImg = cLib.adaptiveThreshold(fixedImg, 64, 64)
    movingImg = cLib.adaptiveThreshold(movingImg, 64, 64)
    ##Volume Thresholding Fixed Img

    print 'performing knn filtering'
    #perform knn filtering
    fixedImg = knn_filter(fixedImg, 1)
    movingImg= knn_filter(movingImg, 1)

    # the connectivity structure matrix
    s = [[[1 for k in xrange(3)] for j in xrange(3)] for i in xrange(3)]

    print 'extracting connected components'
    # find connected components
    fixedImg, nr_objects = ndimage.label(fixedImg, s)


    print 'thresholding by volume'
    #volume thresholding with upperFence
    mask = fixedImg > fixedImg.mean()
    sizes = ndimage.sum(mask, fixedImg, range(nr_objects + 1))
    mask_size = sizes > upperFence
    remove_pixel = mask_size[fixedImg]
    fixedImg[remove_pixel] = 0
    fixedImg, nr_objects = ndimage.label(fixedImg, s)


    if not lowerFence == 0:
        #volume thresholding with upperFence
        mask = fixedImg > fixedImg.mean()
        sizes = ndimage.sum(mask, fixedImg, range(nr_objects + 1))
        mask_size = sizes < lowerFence
        remove_pixel = mask_size[fixedImg]
        fixedImg[remove_pixel] = 0
        fixedImg, nr_objects = ndimage.label(fixedImg, s)

    ##Connected Components + Volume Thresholding On Moving Image

    # find connected components
    labeled, nr_objects = ndimage.label(movingImg, s)

    #volume thresholding with upperFence
    mask = labeled > labeled.mean()
    sizes = ndimage.sum(mask, labeled, range(nr_objects + 1))
    mask_size = sizes > upperFence
    remove_pixel = mask_size[labeled]
    labeled[remove_pixel] = 0
    labeled, nr_objects = ndimage.label(labeled, s)

    if not lowerFence == 0:
        #volume thresholding with lowerFence
        mask = labeled > labeled.mean()
        sizes = ndimage.sum(mask, labeled, range(nr_objects + 1))
        mask_size = sizes < lowerFence
        remove_pixel = mask_size[labeled]
        labeled[remove_pixel] = 0
        labeled, nr_objects = ndimage.label(labeled, s)

    print 'registering clusters'
    realFixedClusters = rLib.ANTs(fixedImg, labeled, lowerFence, upperFence)

    #filtering wrong ones
    for i in range(len(realFixedClusters)):
        distance = np.linalg.norm([x1 - x2 for (x1, x2) in zip(realFixedClusters[i].getCentroid(), realFixedClusters[i].timeRegistration.getCentroid())])
        volumeChangeForwards = np.abs(realFixedClusters[i].volume - realFixedClusters[i].timeRegistration.volume)/np.abs(realFixedClusters[i].volume)
        volumeChangeBackwards = np.abs(realFixedClusters[i].volume - realFixedClusters[i].timeRegistration.volume)/np.abs(realFixedClusters[i].timeRegistration.volume)
        if not (distance < 500 and volumeChangeForwards < 2 and volumeChangeBackwards < 2):
            realFixedClusters[i].timeRegistration.members = (-1, -1, -1)
            realFixedClusters[i].timeRegistration.volume = -1

    return realFixedClusters
