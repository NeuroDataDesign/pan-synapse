import sys
sys.path.insert(0, '../functions/')
import mouseVis
import random

data1 = [random.random() for i in range(100)]
mouseVis.generateHist(data1, title= 'random data 1', yaxis='proportion of data', axisStart=0, axisEnd = .5)

data2 = [random.random() for i in range(100)]
mouseVis.generateHist(data2, title = 'random data 2', yaxis='proportion of data')

data3 = [data1, data2]
mouseVis.generateMultiHist(data3, title = 'random data multiVoxHist', yaxis='proportion of data', axisStart = 0, axisEnd = .5)
