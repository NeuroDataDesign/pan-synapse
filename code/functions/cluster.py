import numpy as np

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

    #TODO develop a better compactness metric
    def getCompactness(self):
        unzipList = zip(*self.members)
        listZ = unzipList[0]
        listY = unzipList[1]
        listX = unzipList[2]
        z_size_of_cluster = max(listZ) - min(listZ)
        y_size_of_cluster = max(listY) - min(listY)
        x_size_of_cluster = max(listX) - min(listX)
        return len(self.members)/(z_size_of_cluster*y_size_of_cluster*x_size_of_cluster)
