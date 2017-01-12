import tiffIO as tIO
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
py.sign_in('levinwil', 'zs8MPogNdFIeRkMXi62h')
#plotly method for histograms
'''
def generateVoxHist(voxel, figName='untitled', figNum=-1, bins=10, axisStart=None, axisEnd=None, normed=False, xaxis='untitled_axis', yaxis='untitled_axis'):
    for i in range(len(voxel.shape)-1):
        voxel = voxel.flatten()
    print voxel.shape
    data = [
        go.Histogram(
            x = voxel,
            histnorm='probability',
            xbins=dict(
                start = axisStart,
                end = axisEnd
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
'''
#matplotlib method for histogram
def generateVoxHist(voxel, title = 'Untitled', bins = 50, xaxis = 'untitled_axis', yaxis = 'untitled_axis', normed = True):
    voxel = np.array(voxel)
    voxel = voxel.flatten()
    plt.hist(voxel, bins= bins, normed= normed)
    plt.title = title
    plt.xlabel = xaxis
    plt.ylabel = yaxis
    plt.show()
#plotly method for generating stacked histograms
'''
def generateMultiVoxHist(voxelList, figName='untitled', figNum=None, bins=10, axisStart=None, axisEnd=None, normed=False, xaxis='untitled_axis', yaxis='untitled_axis'):
    data =[]
    for i in range(len(voxelList)):
        data.append(go.Histogram(
                        x = voxelList[i],
                        histnorm='probability',
                        xbins=dict(
                            start = axisStart,
                            end = axisEnd,
                            size = 0.7
                        )
                    ))
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
'''
#matplotlib method for plotting mutliple histograms
def generateMultiVoxHist(voxelList, title = 'Untitled', bins=10, xaxis = 'untitled_axis', yaxis = 'untitled_axis', normed = True, stacked = True):
    for i in range(len(voxelList)):
        voxelList[i] = np.array(voxelList[i])
        voxelList[i] = voxelList[i].flatten()
    plt.hist(voxelList, bins=bins, normed= normed, stacked = stacked)
    plt.title = title
    plt.xlabel = xaxis
    plt.ylabel = yaxis
    plt.show()
