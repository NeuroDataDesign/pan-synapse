import cv2
import numpy as np
from cluster import Cluster
import cPickle as pickle
##### y, x coordinates are based off of opencv image coordinate system
##### (z,y,x)

def getAllClusterMembers(clusterList):
    #complete cluster member list
    clusterMemberList = []
    for cluster in clusterList:
        clusterMemberList.append(cluster.getMembers())
    return clusterMemberList

def getBoundary(zslice, clusterMemberList):
    boundaryPixels = []
    visClusters = []
    for elem in clusterMemberList:
        if elem[0]==zlice:
            visClusters.append([elem[0], elem[1]])
    visY = zip(*visClusters)[0]
    visX = zip(*visClusters)[1]
    for pixel in visClusters:
        # upper boundary case
        if (pixel[0]+1 not in visY and pixel[0]+1 <=1024): #for y
            boundaryPixels.append([pixel[0]+1, pixel[1]])
        if (pixel[1]+1 not in visX and pixel[1]+1 <=1024): #for x
            boundaryPixels.append([pixel[0], pixel[1]+1])
        #lower boundary case
        if (pixel[0]-1 not in visY and pixel[0]-1 >=0): #for  y
            boundaryPixels.append([pixel[0]-1, pixel[1]])
        if (pixel[1]-1 not in visX and pixel[1]-1 >=0): #for x
            boundaryPixels.append([pixel[0], pixel[1]-1])

    #removing duplicates
    boundaryPixels = list(set(boundaryPixels))
    return boundaryPixels

def visualize(zslice, image3D, clusters):
    image = image3d[zslice]
    #convert image to RGB
    imageRGB = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    boundaryPixels = getBoundary(zslice, getAllClusterMembers(clusters))
    for pixel in boundaryPixels:
    #chaning boundary pixel color to yellow
        imgRGB[pixe[0]][pixel[1]][0] = 255
        imgRGB[pixe[0]][pixel[1]][1] = 255
        imgRGB[pixe[0]][pixel[1]][2] = 0
    #pickle
    pickle.dump(imageRGB, open('final.image', 'w'))

    cv2.imshow('Image slice at z = ' + str(zslice), imageRGB)
    cv2.waitKey()
