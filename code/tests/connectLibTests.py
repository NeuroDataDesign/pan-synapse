import sys
import pickle
import numpy as np
sys.path.insert(0, '../functions/')
from epsilonDifference import epsilonDifference as floatEq
from connectLib import otsuVox

synthGauss = pickle.load(open('synthDat/smallGaussian.synth', 'r'))
synthTwoGauss = pickle.load(open('synthDat/smallTwoGaussian.synth', 'r'))

print 'otsuVox in connectLib.py'
synthGaussSolution = [(1, 2, 2), (2, 1, 2), (2, 2, 1), (2, 2, 2), (2, 2, 3), (2, 3, 2), (3, 2, 2)]
test1 = zip(*np.where(otsuVox(synthGauss) == 1.))
print '\tTest 1: ', test1 == synthGaussSolution,'\n\t\tExpected: ', synthGaussSolution, '\n\t\tResult: ', test1

synthTwoGaussSolution = [(1, 2, 2), (2, 1, 2), (2, 2, 1), (2, 2, 2), (2, 2, 3), (2, 3, 2), (3, 2, 2)]
test2 = zip(*np.where(otsuVox(synthGauss) == 1.))
print '\tTest 2: ', test2 == synthTwoGaussSolution,'\n\t\tExpected: ', synthTwoGaussSolution, '\n\t\tResult: ', test2
