import libtiff
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageSequence

def loadTiff(location):
    return libtiff.TiffFile(str(location)).get_tiff_array()

def unzipChannels(image):
    return np.stack([image[::2],image[1::2]])

def normVoxel(range = (0, 255)):
    pass

if __name__ == '__main__':
    #DEBUG
    multiChanDat = unzipChannels(loadTiff('SEP-GluA1-KI_tp1.tif'))
    cv2.imshow('chan0', multiChanDat[0][0])
    cv2.imshow('chan1', multiChanDat[1][0])
    cv2.waitKey()
