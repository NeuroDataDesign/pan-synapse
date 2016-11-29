import tiffIO as tIO
import mouseVis as mv
import plosLib as pLib
import matplotlib.pyplot as plt
import numpy as np
import cv2

data0 = tIO.unzipChannels(tIO.loadTiff('../data/SEP-GluA1-KI_tp1.tif'))[0][0:5]
pLib.pipeline(data0)
