class Cluster:
    def __init__(self, members):
        self.members = members
        self.centroid = self.getCentroid()
        self.compactness = self.getCompactness()

    def getCentroid(self):
        pass

    def getCompactness(self):
        pass
