import sys
sys.path.insert(0,'../functions/')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle
from random import randrange as rand
from skimage.measure import label
import plosLib as pLib
import connectLib as cLib


def generatePointSet():
    center = (rand(0, 99), rand(0, 99), rand(0, 99))
    toPopulate = []
    for z in range(-1, 2):
        for y in range(-1, 2):
            for x in range(-1, 2):
                curPoint = (center[0]+z, center[1]+y, center[2]+x)
                #only populate valid points
                valid = True
                for dim in range(3):
                    if curPoint[dim] < 0 or curPoint[dim] >= 100:
                        valid = False
                if valid:
                    toPopulate.append(curPoint)
    return set(toPopulate)

def generateTestVolume():
    #create a test volume
    volume = np.zeros((100, 100, 100))
    myPointSet = set()
    for _ in range(rand(500, 800)):
        potentialPointSet = generatePointSet()
        #be sure there is no overlap
        while len(myPointSet.intersection(potentialPointSet)) > 0:
                potentialPointSet = generatePointSet()
        for elem in potentialPointSet:
            myPointSet.add(elem)
    #populate the true volume
    for elem in myPointSet:
        volume[elem[0], elem[1], elem[2]] = 60000
    #introduce noise
    noiseVolume = np.copy(volume)
    for z in range(noiseVolume.shape[0]):
        for y in range(noiseVolume.shape[1]):
            for x in range(noiseVolume.shape[2]):
                if not (z, y, x) in myPointSet:
                    noiseVolume[z][y][x] = rand(0, 10000)
    return volume, noiseVolume



def executeTest():
    trueVolume, testVolume = generateTestVolume()
    labelVolume = label(trueVolume)
    maxLabel = np.max(labelVolume)

    #get pieline results
    results = cLib.otsuVox(pLib.pipeline(testVolume))
    detected = zip(*np.where(results == 1))

    #get random results for p value comparison
    randomResults = np.zeros_like(testVolume)
    for z in range(randomResults.shape[0]):
        for y in range(randomResults.shape[1]):
            for x in range(randomResults.shape[2]):
                randomResults[z][y][x] = rand(0, 2)
    randomDetected = zip(*np.where(randomResults == 1))

    #score results
    numDetected = 0
    numMistaken = 0
    alreadyCounted = []
    for point in detected:
        labelPointVal = labelVolume[point[0], point[1], point[2]]
        if labelPointVal != 0 and not labelPointVal in alreadyCounted:
            numDetected +=1
            alreadyCounted.append(labelPointVal)
        if labelPointVal == 0:
            numMistaken +=1

    print "\tPipeline:"
    print "\t\tPD: ", float(numDetected)/maxLabel
    print "\t\tFAR: ", float(numMistaken)/(100 * 100 *100)

    randNumDetected = 0
    randNumMistaken = 0
    alreadyCounted = []
    for point in randomDetected:
        labelPointVal = labelVolume[point[0], point[1], point[2]]
        if labelPointVal != 0 and not labelPointVal in alreadyCounted:
            randNumDetected +=1
            alreadyCounted.append(labelPointVal)
        if labelPointVal == 0:
            randNumMistaken +=1

    print "\tRandom:"
    print "\t\tPD: ", float(randNumDetected)/maxLabel
    print "\t\tFAR: ", float(randNumMistaken)/(100 * 100 *100)

    return float(numDetected)/maxLabel, float(numMistaken)/(100 * 100 *100), float(randNumDetected)/maxLabel, float(randNumMistaken)/(100 * 100 *100)

spd=0.
sfar=0.
srpd=0.
srfar=0.

for num in range(1,11):
    print "\nExecuting Test: ", num
    pd, far, rpd, rfar = executeTest()
    spd+=pd
    sfar+=far
    srpd+=rpd
    srfar+=rfar

print '\n\nAverage Performance:'
print '\tPipeline:'
print '\t\tPD: ', spd/10.
print '\t\tFAR: ', sfar/10.
print '\tRandom: '
print '\t\tPD: ', srpd/10.
print '\t\tFAR: ', srfar/10.
