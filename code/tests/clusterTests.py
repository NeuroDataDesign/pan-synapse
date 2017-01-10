import sys
sys.path.insert(0, '../functions/')
from epsilonDifference import epsilonDifference as floatEq
from cluster import Cluster
import epsilonDifference as epDiff
import matplotlib.pyplot as plt
import connectLib as cLib
import pickle

testData1 = [[3,3,3], [3,3,2], [3,3,4], [3,2,3], [3,4,3], [2,3,3], [4,3,3]]
testData2 = [[3,3,3], [3,3,4], [3,4,4], [3,4,5], [3,5,5], [4,5,5], [4,5,6]]
testData3 = [[0, 0, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1],]
testData4 = pickle.load(open('synthDat/exponDecayIndexList.synth', 'r'))
testData5 = pickle.load(open('synthDat/smallTwoGaussian.synth', 'r'))

print 'Cluster in cluster.py'
testCluster1 = Cluster(testData1)
testCluster2 = Cluster(testData2)
testCluster3 = Cluster(testData3)
testCluster4 = Cluster(testData4)

#test the centroid method
print '\tTest 1: ', testCluster1.getCentroid() == [3., 3., 3.],'\n\t\tExpected: [3, 3, 3]\tResult: ', testCluster1.getCentroid()
print '\tTest 2: ', epDiff.epsilonDifference(3.28571429, testCluster2.getCentroid()[0], .001) and epDiff.epsilonDifference(4.14285714, testCluster2.getCentroid()[1], .001) and epDiff.epsilonDifference(4.57142857, testCluster2.getCentroid()[2], .001),'\n\t\tExpected: [3.28571429, 4.14285714, 4.57142857]\tResult: ', testCluster2.getCentroid()
print '\tTest 3: ', testCluster3.getCentroid() == [0.5, 0.5, 0.5],'\n\t\tExpected: [0.5, 0.5, 0.5]\tResult: ', testCluster3.getCentroid()

#test the compactness method
print '\tTest 4: ', testCluster3.getStdDistance() == 0,'\n\t\tExpected: 0\tResult: ', testCluster3.getStdDistance()
print "\tTesting probSphere method with spherical data. Probability: " + str(testCluster4.probSphere())
print "\tTesting getStdDistance method with spherical data. Compactness: " + str(testCluster4.getStdDistance())

#test the densityOfSlice method
#NOTE:slicing from 1 to remove background cluster
clusterList = cLib.connectedComponents(cLib.otsuVox(testData5))[1:]

test5 = cLib.densityOfSlice(clusterList, 0, 5, 0, 5, 0, 5)
print '\tTest 5: ', epDiff.epsilonDifference(test5, 2.22222222),'\n\t\tExpected: 2.22222\tResult: ', test5

test6 = cLib.densityOfSlice(clusterList, 0, 2, 0, 2, 0, 2)
print '\tTest 6: ', epDiff.epsilonDifference(test6, 17.3611),'\n\t\tExpected: 17.3611\tResult: ', test6

test7 = cLib.densityOfSlice(clusterList, 2, 3, 2, 3, 2, 3)
print '\tTest 7: ', 0.,'\n\t\tExpected: 0.\tResult: ', test7
