from skimage.filters import threshold_otsu
import tiffIO as tIO
import mouseVis as mv
import plosLib as pLib
import matplotlib.pyplot as plt
import numpy as np
import cv2

#load the data
data0 = tIO.unzipChannels(tIO.loadTiff('../data/SEP-GluA1-KI_tp1.tif'))[0][0:5]

#generate a foreground probability map for the data
probVox = pLib.pipeline(data0)

#generate a histogram to show bimodlity of the foreground probs
mv.generateVoxHist(probVox)
plt.show()

#get the thresholds that minimize inter class variance of the bimodal hist
threshList = np.stack([threshold_otsu(curSlice) for curSlice in probVox])
bianVox = np.stack([probVox[i] > thresh for i, thresh in enumerate(threshList)])
