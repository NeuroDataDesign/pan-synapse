import cv2
import time
import numpy as np

from random import randint
from scipy.spatial import KDTree
from scipy.ndimage.filters import convolve
from skimage.exposure import equalize_adapthist

class neuroGraph:
    def __init__(self, nodes, edges, vis):
        self._nodes = nodes
        self._edges = edges
        self._vis = vis


def boostDendrites(imgStack, n=2, neighborhood=16, dilations=5, percentile=50):
    dendriteProxStack = []
    nthStack = []

    imgStackEq = np.stack([equalize_adapthist(elem) for elem in imgStack])

    for img in imgStackEq:
        nthImg = nthAve(img, n, neighborhood, neighborhood)
        dil = cv2.dilate(nthImg, None, iterations=dilations)
        mask = dil > np.percentile(dil, percentile)

        dendriteProxImg = img * mask
        dendriteProxStack.append(dendriteProxImg)

        nthStack.append(nthImg)

    return np.stack(dendriteProxStack), np.stack(nthStack)


def estimateGraph(nodeImg, dendrites, thickness=10, neighbors=6, baselineSize=10):
    ddCp = dendrites.copy()

    baseline = []
    for i in range(baselineSize):
        y0, x0 = randint(0, dendrites.shape[0]), randint(0, dendrites.shape[1])
        y1, x1 = randint(0, dendrites.shape[0]), randint(0, dendrites.shape[1])

        length = int(np.hypot(x1-x0, y1-y0))
        x, y = np.linspace(x0, x1, length).astype(int), np.linspace(y0, y1, length).astype(int)

        edgeStats = []
        for k in range(length):
            sub = dendrites[max(y[k]-thickness,0):min(y[k]+thickness, dendrites.shape[0]), max(x[k]-thickness, 0):min(x[k]+thickness, dendrites.shape[1])]
            edgeStats.append(np.mean(sub))

        baseline.append(np.mean(edgeStats))

    baseMu = np.mean(baseline)
    baseSig = np.std(baseline)

    edges = []

    nodes = zip(*(np.nonzero(nodeImg)))
    tree = KDTree(nodes)
    for curIdx, node in enumerate(nodes):
        partnerIdxList = tree.query(node, k=neighbors)[1]
        partners = []
        for partnerIdx in partnerIdxList:
            if partnerIdx > curIdx:
                partners.append(nodes[partnerIdx])

        for partner in partners:
            y0, x0 = node
            y1, x1 = partner

            length = int(np.hypot(x1-x0, y1-y0))
            x, y = np.linspace(x0, x1, length).astype(int), np.linspace(y0, y1, length).astype(int)

            edgeStats = []
            for k in range(length):
                sub = dendrites[max(y[k]-thickness,0):min(y[k]+thickness, dendrites.shape[0]), max(x[k]-thickness, 0):min(x[k]+thickness, dendrites.shape[1])]
                edgeStats.append(np.mean(sub))

            dp = np.mean(edgeStats)
            z = (dp - baseMu)/float(baseSig)
            if z > 1.5:
                edges.append([y, x])

    for edge in edges:
        y = edge[0]
        x = edge[1]
        for k in range(len(y)):
            ddCp[max(y[k]-3,0):min(y[k]+3, dendrites.shape[0]), max(x[k]-3, 0):min(x[k]+3, dendrites.shape[1])] = 255

    return nodes, edges, ddCp


def evolveDendrites(data, epochs=2, n=2, neighborhood=16, dilations=5, percentile=50):
    species = data
    kernel = np.ones((8, 8))
    for i in range(epochs):
        genus, _ = boostDendrites(np.stack([equalize_adapthist(elem) for elem in species]),
                                     percentile=percentile,
                                     neighborhood=neighborhood,
                                     n = n,
                                     dilations=dilations)

        species = np.stack([convolve(elem, kernel) for elem in genus]).astype(np.int64)

    return species


def generateNeuroGraphStack(data):

    neuroGraphStack = []

    print 'Growing Dendrites'
    dendriteImgs = evolveDendrites(data, epochs=10, dilations=10)
    print 'Estimating Graph Connections. Completion:'
    for idx, dendriteImg in enumerate(dendriteImgs):
        print '\t', idx/float(len(dendriteImgs))
        nodeImg = generateNodeImg(dendriteImg, 64)
        nodes, edges, vis = estimateGraph(nodeImg, dendriteImg)
        neuroGraphStack.append(neuroGraph(nodes, edges, vis))

    return neuroGraphStack


def generateNodeImg(dendriteImg, step=64):

    kernelX = [[1,0,-1],
           [2, 0, -2],
           [1, 0, -1]]

    kernelY = [[1, 2, 1],
           [0, 0, 0],
           [-1, -2, -1]]

    xGrad = convolve(dendriteImg, kernelX)
    yGrad = convolve(dendriteImg, kernelY)
    grad = np.sqrt(np.add(np.power(xGrad, 2), np.power(yGrad, 2)))

    symmetryKernel = np.ones((16, 16))
    symmetryKernel[1:15, 1:15] = 0
    symmetryKernel[7:9, 7:9] = -1

    potentialNodes = convolve(grad, symmetryKernel)

    nodes = np.multiply(
                np.logical_and(np.logical_xor(potentialNodes,
                                              grad),
                               dendriteImg),
                 dendriteImg)

    nonMaxSuppression = np.zeros_like(nodes)

    for y in range(0, 1024, step):
        for x in range(0, 1024, step):
            sub = nodes[y:y+step, x:x+step]

            aMax = np.argmax(sub)
            yMax = aMax/step
            xMax = aMax%step

            nonMaxSuppression[y+yMax, x+xMax] = sub[yMax, xMax]

    return nonMaxSuppression


def nthAve(img, n, stepY, stepX):
    #divide the image
    out = np.zeros_like(img)
    for yStart in range(0, img.shape[0], stepY):
        curRow = []
        for xStart in range(0, img.shape[1], stepX):
            sub = img[yStart:yStart+stepY, xStart:xStart+stepX]
            out[yStart:yStart+stepY, xStart:xStart+stepX] = np.average(sub)**n
    return np.stack(out)
