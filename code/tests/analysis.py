import sys
sys.path.insert(0, '../functions/')
from skimage.filters import threshold_otsu
import tiffIO as tIO
import mouseVis as mv
import plosLib as pLib
import connectLib as cLib
import matplotlib.pyplot as plt
import numpy as np
import cv2

#load the data
data0 = tIO.unzipChannels(tIO.loadTiff('../../data/SEP-GluA1-KI_tp1.tif'))[0][0:5]

#generate a foreground probability map for the data
probVox = pLib.pipeline(data0)

#generate a histogram to show bimodlity of the foreground probs
mv.generateVoxHist(probVox)
plt.show()

#get the otsu binarization of the supervoxel
bianVox = cLib.otsuVox(probVox)

#extract the connected components from the bianary voxel
clusters = cLib.cluster(bianVox)
