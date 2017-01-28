import cv2
import numpy as np
from cluster import Cluster
import cPickle as pickle
import matplotlib as plt
##### y, x coordinates are based off of opencv image coordinate system
##### (z,y,x)

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
