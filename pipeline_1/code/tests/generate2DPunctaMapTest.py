import sys
sys.path.insert(0, '../functions/')
import tiffIO as tIO
import mouseVis as mv
import plosLib as pLib
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math
import pickle
import epsilonDifference as epDiff

#testing decay map
data_slice = pickle.load(open('synthDat/exponDecay.synth', 'r'))
print "gemerate2DPunctaMap in plosLib.py"
print '\tTest 1:  ' + str(epDiff.epsilonDifference(0.000427143453979, pLib.generate2DPunctaMap(data_slice, 1)[50][50], .0000001))
print '\t\tExpected: 0.000427143454\tResult: ' + str(pLib.generate2DPunctaMap(data_slice, 1)[50][50])

#testing along top
print '\tTest 2:  ' + str(epDiff.epsilonDifference(0, pLib.generate2DPunctaMap(data_slice, 1)[50][0], .0000001))
print '\t\tExpected: 0.0\tResult: ' + str(pLib.generate2DPunctaMap(data_slice, 1)[50][0])

#testing along left
print '\tTest 3:  ' + str(epDiff.epsilonDifference(0, pLib.generate2DPunctaMap(data_slice, 1)[0][50], .0000001))
print '\t\tExpected: 0.0\tResult: ' + str(pLib.generate2DPunctaMap(data_slice, 1)[0][50])

#testing along bottom
print '\tTest 4:  ' + str(epDiff.epsilonDifference(0, pLib.generate2DPunctaMap(data_slice, 1)[50][99], .0000001))
print '\t\tExpected: 0.0\tResult: ' + str(pLib.generate2DPunctaMap(data_slice, 1)[0][0])

#testing along right
print '\tTest 5:  ' + str(epDiff.epsilonDifference(0, pLib.generate2DPunctaMap(data_slice, 1)[99][50], .0000001))
print '\t\tExpected: 0.0\tResult: ' + str(pLib.generate2DPunctaMap(data_slice, 1)[99][50])

allPointNines = pickle.load(open('synthDat/allPointNines.synth', 'r'))
print '\tTest 6:  ' + str(epDiff.epsilonDifference(0.071789798769185, pLib.generate2DPunctaMap(allPointNines, 2)[3][6], .0001))
print '\t\tExpected: 0.071789798769185\tResult: ' + str(pLib.generate2DPunctaMap(allPointNines, 2)[3][6])
