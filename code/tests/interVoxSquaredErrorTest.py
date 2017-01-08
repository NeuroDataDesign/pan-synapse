import sys
sys.path.insert(0, '../functions/')
import numpy as np
import pickle
import plosLib as pLib

synthOnes = pickle.load(open('synthDat/smallOnes.synth', 'r'))
synthGauss = pickle.load(open('synthDat/smallGaussian.synth', 'r'))

#if all numbers are the same, and neighborhood on edge of required data
test1 = pLib.getInterVoxelSquaredError(synthOnes, 2, 2, 2, 2, 2)
print '\tTest 1: ', test1 == 0.,'\n\t\tExpected: 0\tResult: ', test1

#if neighborhood is violated, return 0.
test2 = pLib.getInterVoxelSquaredError(synthOnes, 2, 2, 2, 5, 5)
print '\tTest 2: ', test2 == 0.,'\n\t\tExpected: 0\tResult: ', test2

#if there is some error
test3 = pLib.getInterVoxelSquaredError(synthGauss, 2, 2, 2, 2, 2)
print '\tTest 3: ', test3 == 200.,'\n\t\tExpected: 200\tResult: ', test3
