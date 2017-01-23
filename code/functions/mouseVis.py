import tiffIO as tIO
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle


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
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig)



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
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig)
