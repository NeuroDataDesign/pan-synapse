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
print "prodConv in plosLib.py"
print '\tTest 1:  ' + str(epDiff.epsilonDifference(0.000427143453979, pLib.prodConv(data_slice, 50, 50, 1), .0000001))
print '\t\tExpected: 0.000427143454\tResult: ' + str(pLib.prodConv(data_slice, 50, 50, 1))

#testing matrix of all 1's
data2 = pickle.load(open('synthDat/smallOnes.synth', 'r'))
print '\tTest 2:  ' + str(epDiff.epsilonDifference(1.0, pLib.prodConv(data2, 2, 2, 2), .0000001))
print '\t\tExpected: 1.0\tResult: ' + str(pLib.prodConv(data2, 2, 2, 2))

#testing along top
print '\tTest 3:  ' + str(epDiff.epsilonDifference(0.0, pLib.prodConv(data2, 3, 4, 1), .0000001))
print '\t\tExpected: 0.0\tResult: ' + str(pLib.prodConv(data2, 3, 4, 1))

#testing along left
print '\tTest 4:  ' + str(epDiff.epsilonDifference(0.0, pLib.prodConv(data2, 0, 3, 1), .0000001))
print '\t\tExpected: 0.0\tResult: ' + str(pLib.prodConv(data2, 0, 3, 1))

#testing along bottom
print '\tTest 5:  ' + str(epDiff.epsilonDifference(0.0, pLib.prodConv(data2, 3, 4, 1), .0000001))
print '\t\tExpected: 0.0\tResult: ' + str(pLib.prodConv(data2, 3, 4, 1))

#testing along right
print '\tTest 6:  ' + str(epDiff.epsilonDifference(0.0, pLib.prodConv(data2, 4, 3, 1), .0000001))
print '\t\tExpected: 0.0\tResult: ' + str(pLib.prodConv(data2, 4, 3, 1))
