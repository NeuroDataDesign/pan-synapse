import tiffIO as tIO
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

def generateVoxHist(voxel, figName='untitled', figNum=-1, bins=10, axisStart=None, axisEnd=None, normed=False):
    fig = plt.figure(figNum)
    plt.title(figName)
    hist, bins = np.histogram(voxel, bins=bins, normed=normed)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    if not (axisStart is None or axisEnd is None):
        plt.xlim(axisStart, axisEnd)
    plt.bar(center, hist, align='center', width=width)
    plt.savefig('../service/static/results/PipelineGraph.png')

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
	plt.savefig('../service/static/results/PipelineGraph.png')

''' Plotly methods
def generateHist(voxel, figName='untitled', figNum=-1, bins=10, axisStart=None, axisEnd=None, normed=False, xaxis='untitled_axis', yaxis='untitled_axis'):
    for i in range(len(voxel.shape)-1):
        voxel = voxel.flatten()
    if normed == False:
        norm=''
    else:
        norm='probability'
    if axisStart == None:
        axisStart = np.min(voxel)
    if axisEnd == None:
        axisEnd = np.max(voxel)
    data = [
        go.Histogram(
            x = voxel,
            histnorm=norm,
            xbins=dict(
                start = axisStart,
                end = axisEnd,
                size = (axisEnd - axisStart)/bins
            )
        )
    ]
    layout = go.Layout(
        title=figName,
        xaxis=dict(
            title=xaxis
        ),
        yaxis=dict(
            title=yaxis
        )
    )
    fig = go.Figure(data=data, layout=layout, image="png")
    return fig



#plotly method for generating stacked histograms

def generateMultiHist(voxelList, figName='untitled', figNum=None, bins=10, axisStart=None, axisEnd=None, normed=False, xaxis='untitled_axis', yaxis='untitled_axis'):
    for voxel in range(len(voxelList)):
        for i in range(len(voxelList[voxel].shape)-1):
            voxelList[voxel] = voxelList[voxel].flatten()
    if normed == False:
        norm=''
    else:
        norm='probability'
    if axisStart == None:
        axisStart = np.min(voxelList)
    if axisEnd == None:
        axisEnd = np.max(voxelList)
    data = []
    for i in range(len(voxelList)):
        data.append(go.Histogram(
                        x = voxelList[i],
                        histnorm=norm,
                        xbins=dict(
                            start = axisStart,
                            end = axisEnd,
                            size = (axisEnd - axisStart)/bins
                    )))
    layout = go.Layout(
        title=figName,
        xaxis=dict(
            title=xaxis
        ),
        yaxis=dict(
            title=yaxis
        ),
        barmode='overlay'
    )
    fig = go.Figure(data=data, layout=layout, image="png")
    return fig
    '''
