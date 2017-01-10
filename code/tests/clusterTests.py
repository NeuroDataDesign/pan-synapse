import sys
sys.path.insert(0, '../functions/')
from epsilonDifference import epsilonDifference as floatEq
from cluster import Cluster

testData1 = [[3,3,3], [3,3,2], [3,3,4], [3,2,3], [3,4,3], [2,3,3], [4,3,3]]
testData2 = [[3,3,3], [3,3,4], [3,4,4], [3,4,5], [3,5,5], [4,5,5], [4,5,6]]

print 'Cluster in cluster.py'
testCluster1 = Cluster(testData1)
testCluster2 = Cluster(testData2)

#test the centroid method
test1 = testCluster1.getCentroid()
print '\tTest 1: ', test1 == [3., 3., 3.],'\n\t\tExpected: [3, 3, 3]\tResult: ', test1
