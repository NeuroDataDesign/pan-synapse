import numpy as np
import math

class Cluster:
    def __init__(self, members):
        self.members = members
        self.centroid = self.getCentroid()
        self.compactness = self.getStdDistance()
        self.area = self.getArea()

    def getArea(self):
        return len(self.members)

    def getCentroid(self):
        unzipList = zip(*self.members)
        listZ = unzipList[0]
        listY = unzipList[1]
        listX = unzipList[2]
        return [np.average(listZ), np.average(listY), np.average(listX)]

    def getStdDistance(self):
        unzipList = zip(*self.members)
        listZ = unzipList[0]
        listY = unzipList[1]
        listX = unzipList[2]
        listOfDistances = []
        for location in self.members:
            listOfDistances.append(math.sqrt((location[0]-self.centroid[0])**2 + (location[1]-self.centroid[1])**2 + (location[2]-self.centroid[2])**2))
        stdDevDistance = np.std(listOfDistances)
        return stdDevDistance

    def probSphere(self):
        unzipList = zip(*self.members)
        listZ = unzipList[0]
        listY = unzipList[1]
        listX = unzipList[2]
        volume = ((max(listZ) - min(listZ) + 1)*(max(listY) - min(listY) + 1)*(max(listX) - min(listX) + 1))
        ratio = len(self.members)*1.0/volume
        return 1 - abs(ratio/(math.pi/6) - 1)
