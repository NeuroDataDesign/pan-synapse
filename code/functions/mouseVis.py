import tiffIO as tIO
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
py.sign_in('levinwil', 'zs8MPogNdFIeRkMXi62h')

def generateVoxHist(voxel, figName='untitled', figNum=-1, bins=10, axisStart=None, axisEnd=None, normed=False, xaxis='untitled_axis', yaxis='untitled_axis'):
    voxel.flatten()
    data = [
        go.Histogram(
            x = voxel,
            histnorm='probability',
            xbins=dict(
                start = axisStart,
                end = axisEnd,
                size = 0.7
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
