import sys
sys.path.insert(0, '../functions/')
from skimage.filters import threshold_otsu
from skimage.measure import label
import numpy as np
import cv2


#pass in list of clusters
def densityOfSlice(clusters, maxZ, maxY, maxX, minZ, minY, minX):
    return str(clusters.length/((maxZ-minZ)*(maxY-minY) * (maxX-minX)*0.12*0.12*0.5 )) + " clusters per squared micron"
