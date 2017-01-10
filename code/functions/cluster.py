import numpy as np
import math

class Cluster:
    def __init__(self, members):
        self.members = members
        self.centroid = self.getCentroid()
        self.compactness = self.getCompactness()

    def getCentroid(self):
        unzipList = zip(*self.members)
        listZ = unzipList[0]
        listY = unzipList[1]
        listX = unzipList[2]
        return [np.average(listZ), np.average(listY), np.average(listX)]

    def getCompactness(self):
        unzipList = zip(*self.members)
        listZ = unzipList[0]
        listY = unzipList[1]
        listX = unzipList[2]
        listOfDistances = []
        volume = ((max(listZ) - min(listZ))*(max(listY) - min(listY))*(max(listX) - min(listX)))
        for location in self.members:
            listOfDistances.append(math.sqrt((location[0]-self.centroid[0])**2 + (location[1]-self.centroid[1])**2 + (location[2]-self.centroid[2])**2))
        stdDevDistance = np.std(listOfDistances)
        return stdDevDistance/volume
