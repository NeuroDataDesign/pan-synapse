import tiffIO as tIO
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
py.sign_in('levinwil', 'zs8MPogNdFIeRkMXi62h')

def generateVoxHist(voxel, figName='untitled', figNum=-1, bins=10, axisStart=None, axisEnd=None, normed=False, xaxis='untitled_axis', yaxis='untitled_axis'):
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


def generateMultiVoxHist(voxelList, figName='untitled', figNum=None, bins=10, axisStart=None, axisEnd=None, normed=False, xTitle='untitled_axis', yTitle='untitled_axis'):
    data =[]
    for i in (len(voxelList) - 1):
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
