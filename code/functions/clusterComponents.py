import scipy.ndimage as ndimage

class ClusterComponent:

    def __init__(self, bianIm):
        self.s = [[[1 for k in xrange(3)] for j in xrange(3)] for i in xrange(3)]
        label_im, nr_objects = ndimage.label(bianIm, self.s)
        self.numClusters = nr_objects
        self.labeledIm = label_im
        self.volumes = self.getVolumes()
        self.centroids = self.getCentroids()

    def volumeThreshold(self, threshold=250):
        mask = self.labeledIm > self.labeledIm.mean()
        sizes = ndimage.sum(mask, self.labeledIm, range(self.numClusters + 1))
        mask_size = sizes > threshold
        remove_pixel = mask_size[self.labeledIm]
        self.labeledIm[remove_pixel] = 0
        new_label_im, new_nr_objects = ndimage.label(self.labeledIm, self.s)
        self.labeledIm = new_label_im
        self.numClusters = new_nr_objects
        self.volumes = self.getVolumes()
        self.centroids = self.getCentroids()

    def getVolumes(self):
        mask = self.labeledIm > self.labeledIm.mean()
        temp, temp_nr_objects = ndimage.label(self.labeledIm, self.s)
        sizesTemp = ndimage.sum(mask, temp, range(self.numClusters + 1))
        sizesTempRemoved0 = [sizesTemp[i] for i in range(1, len(sizesTemp))]
        return sizesTempRemoved0

    def getCentroids(self):
        centers = ndimage.measurements.center_of_mass(self.labeledIm, self.labeledIm, [i for i in range(self.numClusters)])
        return centers
