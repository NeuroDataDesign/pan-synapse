import sys
sys.path.insert(0, '../functions/')
from epsilonDifference import epsilonDifference as floatEq
from cluster import Cluster
import epsilonDifference as epDiff

testData1 = [[3,3,3], [3,3,2], [3,3,4], [3,2,3], [3,4,3], [2,3,3], [4,3,3]]
testData2 = [[3,3,3], [3,3,4], [3,4,4], [3,4,5], [3,5,5], [4,5,5], [4,5,6]]
testData3 = [[0, 0, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1],]

print 'Cluster in cluster.py'
testCluster1 = Cluster(testData1)
testCluster2 = Cluster(testData2)
testCluster3 = Cluster(testData3)

#test the centroid method
print '\tTest 1: ', testCluster1.getCentroid() == [3., 3., 3.],'\n\t\tExpected: [3, 3, 3]\tResult: ', testCluster1.getCentroid()
print '\tTest 2: ', epDiff.epsilonDifference(3.28571429, testCluster2.getCentroid()[0], .001) and epDiff.epsilonDifference(4.14285714, testCluster2.getCentroid()[1], .001) and epDiff.epsilonDifference(4.57142857, testCluster2.getCentroid()[2], .001),'\n\t\tExpected: [3.28571429, 4.14285714, 4.57142857]\tResult: ', testCluster2.getCentroid()
print '\tTest 3: ', testCluster3.getCentroid() == [0.5, 0.5, 0.5],'\n\t\tExpected: [0.5, 0.5, 0.5]\tResult: ', testCluster3.getCentroid()

#test the compactness method
print '\tTest 4: ', testCluster3.getCompactness() == 0,'\n\t\tExpected: 0\tResult: ', testCluster3.getCompactness()
