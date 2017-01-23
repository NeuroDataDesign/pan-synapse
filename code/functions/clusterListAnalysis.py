import pickle
import cluster
import numpy as np
import matplotlib.pyplot as plt

volumeList = []
clusters = pickle.load(open('complete.clusters'))
print 'volumes: '
for cluster in range(len(clusters)):
    volumeList.append(clusters[cluster].getVolume())
    print clusters[cluster].getVolume()

print 'length: '
print len(volumeList)
print 'average: ' + str(np.average(volumeList))
print 'percentage of data: ' + str(np.sum(volumeList)*1.0/(1024*1024*4))

print "displaying as picture: "
indexList = []
for cluster in range(len(clusters)):
    indexList.extend(clusters[cluster].members)

synapseImage = np.zeros((5, 1024, 1024))
for index in range(len(indexList)):
    z, y, x = indexList[index]
    synapseImage[z][y][x] = 100
print synapseImage[2]
plt.imshow(synapseImage[2], cmap = 'gray')
plt.show()
