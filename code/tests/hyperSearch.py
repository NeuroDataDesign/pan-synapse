import sys
sys.path.append('../functions')

import cv2
import pickle
import itertools

from cluster import Cluster
from connectLib import clusterThresh

import numpy as np
import matplotlib.pyplot as plt

from plosLib import pipeline as PLOS
from random import randrange as rand

def binaryThreshold(img, percentile=90):
    img = (img/256).astype('uint8')
    threshImg = np.zeros_like(img)
    percentile = np.percentile(img, percentile)
    for i in range(len(img)):
        threshImg[i] = cv2.threshold(img[i], percentile, 255, cv2.THRESH_BINARY)[1]
    return threshImg

def adaptiveThreshold(inImg, sx, sy, sz, p):
    outImg = np.zeros_like(inImg)
    shape = outImg.shape
    subXLen = shape[0]/sx
    subYLen = shape[1]/sy
    subZLen = shape[2]/sz
    for xInc in range(1, sx + 1):
        for yInc in range(1, sy + 1):
            for zInc in range(1, sz + 1):
                sub = inImg[(xInc-1)*subXLen: xInc*subXLen, (yInc-1)*subYLen: yInc*subYLen, (zInc-1)*subZLen: zInc*subZLen]
                subThresh = binaryThreshold(sub, p)
                outImg[(xInc-1)*subXLen: xInc*subXLen, (yInc-1)*subYLen: yInc*subYLen, (zInc-1)*subZLen: zInc*subZLen] = subThresh
    return outImg

def neighborhoodDensity(data, interPlane = 1, intraPlane = 1, percentile = 50):
    output = np.zeros_like(data)
    for z in range(data.shape[0]):
        for y in range(data.shape[1]):
            for x in range(data.shape[2]):
                zLow = z-intraPlane
                zHigh = z+intraPlane
                yLow = y-interPlane
                yHigh = y+interPlane
                xLow = x-interPlane
                xHigh = x+interPlane
                if zLow>=0 and zHigh<data.shape[0] and yLow>=0 and yHigh<data.shape[1] and xLow>=0 and xHigh<data.shape[2]:
                    subVol = data[zLow:zHigh, yLow:yHigh, xLow:xHigh]
                    if not all(subVol.shape) == 0:
                        thresh = np.percentile(subVol, percentile)
                        binSubVol = subVol >= thresh
                        output[z][y][x] = (np.count_nonzero(binSubVol)/float(interPlane*interPlane*intraPlane)) * data[z][y][x] * np.average(subVol)
    return output

def generatePointSet():
    center = (rand(0, 9), rand(0, 999), rand(0, 999))
    toPopulate = []
    for z in range(-3, 2):
        for y in range(-3, 2):
            for x in range(-3, 2):
                curPoint = (center[0]+z, center[1]+y, center[2]+x)
                #only populate valid points
                valid = True
                for dim in range(3):
                    if curPoint[dim] < 0 or curPoint[dim] >= 1000:
                        valid = False
                if valid:
                    toPopulate.append(curPoint)
    return set(toPopulate)

def generateTestVolume(n):
    #create a test volume
    volume = np.zeros((10, 1000, 1000))
    myPointSet = set()
    for _ in range(n):
        potentialPointSet = generatePointSet()
        #be sure there is no overlap
        while len(myPointSet.intersection(potentialPointSet)) > 0:
                potentialPointSet = generatePointSet()
        for elem in potentialPointSet:
            myPointSet.add(elem)
    #populate the true volume
    for elem in myPointSet:
        volume[elem[0], elem[1], elem[2]] = rand(40000, 60000)
    #introduce noise
    noiseVolume = np.copy(volume)
    for z in range(noiseVolume.shape[0]):
        for y in range(noiseVolume.shape[1]):
            for x in range(noiseVolume.shape[2]):
                if not (z, y, x) in myPointSet:
                    toPop = rand(0, 10)
                    if toPop == 5:
                        noiseVolume[z][y][x] = rand(0, 60000)
    return volume, noiseVolume

def applyGradient(volume, originX, originY):
    outStack = []
    maxDistance = np.sqrt((volume[0].shape[0])**2+(volume[0].shape[1])**2)
    for sample in volume:
        outSample = np.zeros_like(sample)
        for y in range(sample.shape[0]):
            for x in range(sample.shape[1]):
                distance = np.sqrt((x - originX)**2+(y - originY)**2)
                sigma = np.sqrt(distance)/np.sqrt(maxDistance)
                modifier = 1.-(sigma * distance/maxDistance)
                outSample[y][x] = modifier * sample[y][x]
        outStack.append(outSample)
    return np.stack(outStack)

def precision_recall_f1(labels, predictions, overlapRatio):

    if len(predictions) == 0:
        print 'ERROR: prediction list is empty'
        return 0., 0., 0.

    labelFound = np.zeros(len(labels))
    truePositives = 0
    falsePositives = 0

    for prediction in predictions:
        #casting to set is ok here since members are uinque
        predictedMembers = set([tuple(elem) for elem in prediction.getMembers()])
        detectionCutoff = overlapRatio * len(predictedMembers)
        found = False

        for idx, label in enumerate(labels):
            labelMembers = set([tuple(elem) for elem in label.getMembers()])
            #if the predictedOverlap is over the detectionCutoff ratio
            if len(predictedMembers & labelMembers) >= detectionCutoff:
                truePositives +=1
                found=True
                labelFound[idx] = 1

        if not found:
            falsePositives +=1

    precision = truePositives/float(truePositives + falsePositives)
    recall = np.count_nonzero(labelFound)/float(len(labels))
    f1 = 0
    try:
        f1 = 2 * (precision*recall)/(precision + recall)

    except ZeroDivisionError:
        f1 = 0

    return precision, recall, f1

def executeTest(algList, paramList, volumeList):
    #for evey volume
    for volume in volumeList:
        #for every param combination
        for params in itertools.product(*[paramList[alg[1]] for alg in algList]):
            #run the current pipeline with the current params
            testString = volume[2]

            #pipelineVol = volume[1]
            for idx, alg in enumerate(algList):
                #pipelineVol = alg[0](popelineVol, *(params[idx]))
                testString = testString + alg[1]+str(params[idx])
                print testString

            #TODO precision recall here


if __name__ == '__main__':
    #create the test volume set
    volumeList = []
    for i in range(2):
        #label, test = generateTestVolume(2000)
        label, test = generateTestVolume(1)
        volumeList.append([label, test, 'sparse_uniform_'+str(i)])
        #volumeList.append([label, applyGradient(test, 0, 0), 'sparse_gradient_'+str(i)])
        #label, test = generateTestVolume(15000)
        volumeList.append([label, test, 'dense_uniform_'+str(i)])
        #volumeList.append([label, applyGradient(test, 0, 0), 'dense_gradient_'+str(i)])

    #create the list of functions to operate over
    funcList = [[PLOS, '_plos'], [adaptiveThreshold, '_adaptive'], [neighborhoodDensity, '_neighborhood']]

    #create the list of params to operate over
    paramDict = {
            '_plos': [elem for elem in itertools.product([1, 2, 3], repeat=3)],
            '_adaptive': [elem for elem in [[j for j in x]+[y] for x in itertools.product([6, 8, 10], repeat=3) for y in [30, 50, 70, 90]]],
            '_neighborhood': [elem for elem in [[j for j in x]+[y] for x in itertools.product([10, 15, 20], repeat=2) for y in [30, 50, 70, 90]]]
    }

    #iterate through all possibilities of inclusion
    for i in itertools.product([0, 1], repeat=3):
        print i
        #populate the current pipeline
        algList = []
        for algNum, use in enumerate(i):
            if use:
                algList.append(funcList[algNum])

        #iterate through all permutations of algs
        for pipeline in itertools.permutations(algList):
            executeTest(pipeline, paramDict, volumeList)
