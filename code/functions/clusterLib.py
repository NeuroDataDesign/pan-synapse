import numpy as np

class Cluster:
    def __init__(self):
        self.centroid = None
        self.variance = None
        self.members = []

class LambdaMeans:
    def __init__(self, voxel, reductionCutoff):
        self.data = voxel
        #this should be a n-tuple of data dimentionality
        self.reductionCutoff = reductionCutoff

    def map(self, partition):
        #if any dim size is still above the threshold
        if any([(a>b) for a, b in zip(partition.shape, self.reductionCutoff)]):
            #perform octal spacial reduction

            #NOTE: integer division is good here since indeces must
            #be ints, and it will provide consistent tie breaking due
            #due to uniform truncation
            zSep, ySep, xSep= [dim/2 for dim in partition.shape]

            #TODO there likely exists a better way to do this
            #split z
            t = data[:zSep]
            b = data[zSep:]

            #split y
            tf = t[:,ySep]
            tb = t[ySep:]

            bf = b[:,ySep]
            bb = b[ySep:]

            #split x
            tfl = tf[:xSep]
            tfr = tf[xSep:]
            bfl = bf[:xSep]
            bfr = bf[xSep:]

            tbl = tb[:xSep]
            tbr = tb[xSep:]
            bbl = bb[:xSep]
            bbr = bb[xSep:]

            #map the voxels out, and reduce the results
            return self.reduce(self.map(
                tfl,
                tfr,
                tbl,
                tbr,
                bfl,
                bfr,
                bbl,
                bbr
            ))

        #if the supervoxel is under all required dim constraints
        else:
            return self.generateClusters(partition)

    def reduce(self, tfl, tfr, tbl, tbr, bfl, bfr, bbl, bbr):
        #TODO join all clusters on edges and return as one supervoxel
        pass

    def generateClusters(self, partition):
        #perform cluster based lambda means on the base supervoxel
        #TODO waiting on a reply from Marcus Commiter on existing implementations
        pass
