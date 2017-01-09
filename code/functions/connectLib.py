import sys
sys.path.insert(0, '../functions/')
from skimage.filters import threshold_otsu
from skimage.measure import label
from cluster import Cluster
import numpy as np
import cv2

def otsuVox(probVox):
    bianVox = np.zeros_like(probVox)
    for zIndex, curSlice in enumerate(probVox):
        #if the array contains all the same values
        if np.max(curSlice) == np.min(curSlice):
            #otsu thresh will fail here, leave bianVox as all 0's
            continue
        thresh = threshold_otsu(curSlice)
        bianVox[zIndex] = curSlice > thresh
    return bianVox

def connectedComponents(voxel):
    labelMap = label(voxel)
    clusterList = []
    #plus 1 since max label should be included
    for uniqueLabel in range(0, np.max(labelMap)+1):
        memberList = zip(*np.where(voxel = uniqueLabel))
        clusterList.append(Cluster(memberList))
    return clusterList

#pass in list of clusters
def densityOfSlice(clusters, maxZ, maxY, maxX, minZ, minY, minX):
    return str(clusters.length/((maxZ-minZ)*(maxY-minY) * (maxX-minX)*0.12*0.12*0.5 )) + " clusters per squared micron"
