import tiffIO as tIO
import matplotlib.pyplot as plt
import numpy as np

def generateVoxHist(voxel, figName='untitled', figNum=-1, bins=10, axisStart=None, axisEnd=None, normed=False):
    fig = plt.figure(figNum)
    plt.title(figName)
    hist, bins = np.histogram(voxel, bins=bins, normed=normed)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    if not (axisStart is None or axisEnd is None):
        plt.xlim(axisStart, axisEnd)
    plt.bar(center, hist, align='center', width=width)

def generateMultiVoxHist(voxelList, figName='untitled', figNum=None, bins=10, axisStart=None, axisEnd=None, normed=False, xTitle='untitled_axis', yTitle='untitled_axis'):
	fig = None
	if not figNum is None:
		fig = plt.figure(figNum)
	else:
		fig = plt.figure()
	plt.title(figName)
	plt.xlabel(xTitle)
	plt.ylabel(yTitle)
        colorIter = ['r', 'c', 'm', 'y', 'k', 'b', 'g']
        plt.hist(voxelList, bins, normed=normed, histtype='bar', color=colorIter[:len(voxelList)])
	return fig
