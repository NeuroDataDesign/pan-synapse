import tiffIO as tIO
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
py.sign_in('levinwil', 'zs8MPogNdFIeRkMXi62h')

#matplotlib method for histogram
def generateHist(voxel, title = 'Untitled', bins = 50, xaxis = 'untitled_axis', yaxis = 'untitled_axis', axisStart = None, axisEnd = None, normed = True, pickle = False):
    voxel = np.array(voxel)
    voxel = voxel.flatten()
    if (type(axisStart) == type(1) or type(axisStart) == type(1.0)):
        start = axisStart
    else:
        start = np.min(voxel)
    if (type(axisEnd) == type(1) or type(axisEnd) == type(1.0)):
        end = axisEnd
    else:
        end = np.max(voxel)
    plot = plt.hist(voxel, bins= bins,  range = (start, end), normed= normed)
    if (pickle):
        pickle.dump(plot, open(title + '.histogram', 'w'))
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.show()

#matplotlib method for plotting mutliple histograms
def generateMultiHist(voxelList, title = 'Untitled', bins=10, xaxis = 'untitled_axis', yaxis = 'untitled_axis', axisStart = None, axisEnd = None, normed = True, stacked = True, pickle = False):
    for i in range(len(voxelList)):
        voxelList[i] = np.array(voxelList[i])
        voxelList[i] = voxelList[i].flatten()
    if (type(axisStart) == type(1) or type(axisStart) == type(1.0)):
        start = axisStart
    else:
        start = np.min(voxel)
    if (type(axisEnd) == type(1) or type(axisEnd) == type(1.0)):
        end = axisEnd
    else:
        end = np.max(voxel)
    plt.hist(voxelList, bins = bins, range = (start, end), normed = normed, stacked = stacked)
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.show()
    
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
