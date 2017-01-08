import sys
sys.path.insert(0, '../functions/')
import numpy as np
import pickle
import plosLib as pLib
from epsilonDifference import epsilonDifference as floatEq

synthOnes = pickle.load(open('synthDat/smallOnes.synth', 'r'))
synthGauss = pickle.load(open('synthDat/gaussianProb.synth', 'r'))

print 'generate3DPunctaMap in plosLib.py'
#if all numbers are the same, and neighborhood on edge of required data
test1 = pLib.generate3DPunctaMap(synthOnes, 2, 2)
print '\tTest 1: ', test1[2][2][2] == 1.,'\n\t\tExpected: 1\tResult: ', test1[2][2][2]

#if neighborhood is violated, return 0.
test2 = pLib.generate3DPunctaMap(synthOnes, 2, 4)
print '\tTest 2: ', test2[2][2][2] == 0.,'\n\t\tExpected: 0\tResult: ', test2[2][2][2]

#if there is some error
test3 = pLib.generate3DPunctaMap(synthGauss, 2, 2)
print '\tTest 3: ', floatEq(test3[2][2][2], .40936) ,'\n\t\tExpected: .40936\tResult: ', test3[2][2][2]
