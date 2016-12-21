import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.misc as sciMisc
import cv2
import functools32


def pipeline(baseVoxel, neighborhood=1, lowerBound=1, upperBound=1):
    pMap2DVox = generatepMap2D(generateForegroundVoxel(baseVoxel), neighborhood=neighborhood)
    return generate3DPunctaMap(pMap2DVox, lowerBound, upperBound)

#NOTE Both of these following functions are fully parallelizable, which would increase speed dramatically
def generateForegroundVoxel(baseVoxel):
    return np.stack([generateForegroundProbMap(image, *getBackgroundGaussian(image)) for image in baseVoxel])

def generatepMap2D(foregroundVoxel, neighborhood):
    return np.stack([generate2DPunctaMap(image, neighborhood) for image in foregroundVoxel])

#returns a tuple of mu and sigma^2
#of the gaussian distribution of pixels in an image
def getBackgroundGaussian(mySlice):
    return np.mean(mySlice), np.var(mySlice)

@functools32.lru_cache(maxsize=65535)
def cacheCDF(t, dist):
    return dist.cdf(t)

def generateForegroundProbMap(mySlice, mu, sigma):
    myDist = stats.norm(mu, np.sqrt(sigma))
    vecCDF = np.vectorize(cacheCDF)
    return vecCDF(mySlice, myDist)

def prodConv(myMat, x, y, neighborhood):
    minX = x - neighborhood
    maxX= x + neighborhood
    minY = y - neighborhood
    maxY= y + neighborhood

    #this is the edge pixel case: return 0 since operation is not well defined
    #Minus 1 in the max case since indexing starts at 0 and shape count starts at 1
    if minX < 0 or minY < 0 or maxX > myMat.shape[0] - 1 or maxY > myMat.shape[1] - 1:
        return 0.

    #plus 1 for max since final slice argument is exclusive
    #TODO work with log probs here instead to maintain precision
    return np.prod(myMat[minX: maxX + 1, minY: maxY+1])

def generate2DPunctaMap(pForeground, neighborhood):
    returnMat = np.zeros_like(pForeground)
    for y in range(pForeground.shape[0]):
        for x in range(pForeground.shape[1]):
            returnMat[x][y] = prodConv(pForeground, x, y, neighborhood)
    return returnMat

def getInterVoxelSquaredError(voxel, x, y, z, lowerBound, upperBound):
    minZ = z - lowerBound
    maxZ = z + upperBound

    #this is the edge pixel case: return 0 since operation is not well defined
    #Minus 1 in the max case since indexing starts at 0 and shape count starts at 1
    if minZ < 0 or maxZ > voxel.shape[0] - 1:
        return 0.

    baseProb = voxel[z][y][x]
    #plus 1 for max since final slice argument is exclusive
    return baseProb * np.sum([(baseProb - voxel[i][y][x])**2 for i in range(minZ, maxZ + 1)])

def generate3DPunctaMap(punctaVoxel2D, lowerBound, upperBound):
    returnVox = np.zeros_like(punctaVoxel2D)
    for z in range(punctaVoxel2D.shape[0]):
        for y in range(punctaVoxel2D.shape[1]):
            for x in range(punctaVoxel2D.shape[2]):
                returnVox[z][y][x] = punctaVoxel2D[z][y][x] * np.exp(-1 * getInterVoxelSquaredError(punctaVoxel2D, x, y, z, lowerBound, upperBound))

    #Times 65535 for max int value to make probs look good on visualization
    #cv2.imwrite('../data/post_stitch.jpg', returnVox[2]* 65535)
    return returnVox
