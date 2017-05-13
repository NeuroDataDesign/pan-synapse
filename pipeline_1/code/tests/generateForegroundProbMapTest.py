import sys
sys.path.insert(0, '../functions/')
import numpy as np
import pickle
import plosLib as pLib
from epsilonDifference import epsilonDifference as floatEq

synthOnes = pickle.load(open('synthDat/smallOnes.synth', 'r'))
synthGauss = pickle.load(open('synthDat/smallGaussian.synth', 'r'))


print 'generateForegroundProbMap in plosLib.py'
#if all numbers are the same, and neighborhood on edge of required data
test1 = pLib.generateForegroundProbMap(synthGauss, np.mean(synthGauss), np.var(synthGauss))
print '\tTest 1: ', floatEq(.408153, test1[0][0][0]),'\n\t\tExpected: .408153\tResult: ', test1[0][0][0]
