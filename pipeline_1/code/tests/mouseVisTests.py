import sys
sys.path.insert(0, '../functions/')
import mouseVis
import random
import numpy as np

data1 = np.zeros([100])
for i in range(len(data1)):
    data1[i] = random.random()*100
mouseVis.generateHist(data1, figName= 'random data 1', yaxis='proportion of data')

data2 = np.zeros([100])
for i in range(len(data1)):
    data2[i] = random.random()*100
mouseVis.generateHist(data2, figName = 'random data 2', yaxis='proportion of data')

data3 = [data1, data2]
mouseVis.generateMultiHist(data3, figName = 'random data multiVoxHist', yaxis='proportion of data')
