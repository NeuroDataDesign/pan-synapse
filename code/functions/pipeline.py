import sys
sys.path.insert(0, '../functions/')

import cv2
import quality

from cluster import Cluster
from scipy import ndimage
from neighborhoodLib import neighborhoodDensity

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
    fixedImg = cLib.adaptiveThreshold(fixedImg, 64, 64, 30)
    movingImg = cLib.adaptiveThreshold(movingImg, 64, 64, 30)
    ##Volume Thresholding Fixed Img

    # the connectivity structure matrix
    s = [[[1 for k in xrange(3)] for j in xrange(3)] for i in xrange(3)]

    # find connected components
    fixedImg, nr_objects = ndimage.label(fixedImg, s)


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

    return rLib.ANTs(fixedImg, labeled, lowerFence, upperFence)
