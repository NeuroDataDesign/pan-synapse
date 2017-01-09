import sys
sys.path.insert(0, '../functions/')
from skimage.filters import threshold_otsu
from skimage.measure import label
import numpy as np
import cv2
import willsConnectLib as cLib

print 'densityOfSlice'
test1 = pLib.generateForegroundProbMap(synthGauss, np.mean(synthGauss), np.var(synthGauss))
print '\tTest 1: ', floatEq(.408153, test1[0][0][0]),'\n\t\tExpected: .408153\tResult: ', test1[0][0][0]


print cLib.densityOfSlice(data)
