import tiffIO as tIO
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
import cluster

def getAllClusterMembers(clusterList):
    #complete cluster member list
    clusterMemberList = []
    for cluster in clusterList:
        for member in cluster.getMembers():
            clusterMemberList.append(member)
    return clusterMemberList

def getBoundary(zslice, clusterMemberList):
    boundaryPixels = []
    visClusters = []
    for elem in clusterMemberList:
        if elem[0]==zslice:
            visClusters.append([elem[1], elem[2]])
    if (len(visClusters)==0):
        return []
    for pixel in visClusters:
        # upper boundary case
        if (pixel[0]+1 <1024 and [pixel[0]+1, pixel[1]] not in visClusters): #for y
            boundaryPixels.append([pixel[0]+1, pixel[1]])
        if (pixel[1]+1 <1024 and [pixel[0], pixel[1]+1] not in visClusters): #for x
            boundaryPixels.append([pixel[0], pixel[1]+1])
        #lower boundary case
        if (pixel[0]-1 >=0 and [pixel[0]-1, pixel[1]] not in visClusters): #for  y
            boundaryPixels.append([pixel[0]-1, pixel[1]])
        if (pixel[1]-1 >=0 and [pixel[0], pixel[1]-1] not in visClusters): #for x
            boundaryPixels.append([pixel[0], pixel[1]-1])
    return boundaryPixels

def visualize(zslice, image3D, clusters):
    image = image3D[zslice]
    #convert image to RGB
    imageRGB = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    boundaryPixels = getBoundary(zslice, getAllClusterMembers(clusters))
    for pixel in boundaryPixels:
        #changing boundary pixel color to yellow
        imageRGB[pixel[0],pixel[1]] = [65535, 65535, 0]
    #pickle
    #pickle.dump(imageRGB, open('final.image', 'w'))
    #cv2.imshow('Image slice at z = ' + str(zslice), imageRGB)
    return imageRGB

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

def generatePlotlyLineGraph(myID, coregisteredVolumeList, figName="Graph of Cluster Volumes Over Time"):
    data = []
    for cluster in range(len(coregisteredVolumeList)):
        singleVolumeList = []
        times = []
        for timePoint in range(len(coregisteredVolumeList[cluster])):
            singleVolumeList.append(coregisteredVolumeList[cluster][timePoint])
            times.append(timePoint)
        data.append(go.Scatter(
                        y = singleVolumeList,
                        x = times,
                        mode = 'lines+markers',
                        name = "Cluster " + str(cluster)
                    ))
    layout = go.Layout(
        title=figName,
        xaxis=dict(
            title='Timepoint'
        ),
        yaxis=dict(
            title='Volume'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='static/data/'+str(myID)+'.html')
