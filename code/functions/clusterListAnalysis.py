import pickle
import cluster
import numpy as np
import matplotlib.pyplot as plt
import mouseVis as mv

clusters = pickle.load(open('complete.clusters'))
volumeList = np.zeros((len(clusters)))
for cluster in range(len(clusters)):
    volumeList[cluster] = clusters[cluster].getVolume()

print 'number of clusters: ' + str(len(volumeList))
print 'average volume: ' + str(np.average(volumeList))
print 'percentage of data: ' + str(np.sum(volumeList)*1.0/(1024*1024*4))
mv.generateHist(volumeList, normed = False, bins = 100, xaxis = 'Volume', yaxis = 'frequency', figName='Cluster Volumes')
