import math

import numpy as np

from scipy.ndimage.measurements import center_of_mass

from random import randrange as rand
from random import uniform as floatRand

def get3DRigid(pitchRange = .1,
               rollRange = .1,
               yawRange = .1,
               xRange = 0.,
               yRange = 0.,
               zRange = 0.,
               pitch=None,
               yaw=None,
               roll=None,
               zT=None,
               yT=None,
               xT=None):

    #generate a random rigid body transform in given bounds
    a = floatRand(pitchRange-(pitchRange/2.), pitchRange+(pitchRange/2.))
    b = floatRand(yawRange-(yawRange/2.), yawRange+(yawRange/2.))
    c = floatRand(rollRange-(rollRange/2.), rollRange+(rollRange/2.))

    xt = floatRand(xRange-(xRange/2.), xRange+(xRange/2.))
    yt = floatRand(yRange-(yRange/2.), yRange+(yRange/2.))
    zt = floatRand(zRange-(zRange/2.), zRange+(zRange/2.))

    #set default params, if passed
    if yaw is not None:
        a = yaw
    if pitch is not None:
        b = pitch
    if roll is not None:
        c = roll
    if xT is not None:
        xt = xT
    if yT is not None:
        yt = yT
    if zT is not None:
        zt = zT

    #generate the transform
    transform = np.stack([
        [math.cos(a)*math.cos(b), math.cos(a)*math.sin(b)*math.sin(c)-math.sin(a)*math.cos(c), math.cos(a)*math.sin(b)*math.cos(c)+math.sin(a)*math.sin(c), xt],
        [math.sin(a)*math.cos(b), math.sin(a)*math.sin(b)*math.sin(c)+math.cos(a)*math.cos(c), math.sin(a)*math.sin(b)*math.cos(c)-math.cos(a)*math.sin(c), yt],
        [-math.sin(b), math.cos(b)*math.sin(c), math.cos(b)*math.cos(c), zt],
        [0., 0., 0., 1.]
    ])
    return transform

def apply3DRigid(initialVolume, transform, verbose=False):
    #create a body to hold return values
    rigidMatrix = np.zeros_like(initialVolume)

    #create var to keep track of out of bounds percent
    out = 0.
    sigOut = 0.

    #convert every voxel
    for z in range(initialVolume.shape[0]):
        for y in range(initialVolume.shape[1]):
            for x in range(initialVolume.shape[2]):

                #shift the volume so that the transform is applied to the center, and not the top left back edge
                shift = [initialVolume.shape[2]/2., initialVolume.shape[1]/2., initialVolume.shape[0]/2.]
                shiftedPoint = list(np.subtract([x, y, z], shift))
                shiftedPoint.append(1.)

                #calculate the transform, drop the irrelavent 1 at the end
                new = np.dot(transform, shiftedPoint)[:3]

                #shift the volume back to its original spot after transform
                final = np.add(new, shift)

                #attempt to assign new spot
                try:
                    rigidMatrix[round(final[2]), round(final[1]), round(final[0])] = initialVolume[z, y, x]

                #if transformed place is out of bounds, dont assign it
                except IndexError:
                        out+=1.
                        if not initialVolume[z, y, x]:
                            sigOut+=1
                        continue
    #print information, if required
    if verbose:
        print 'Out of bounds fraction: ', out/float(initialVolume.shape[0]*initialVolume.shape[1]*initialVolume.shape[2])
        print 'Non-0 Out of bounds fraction: ', sigOut/float(initialVolume.shape[0]*initialVolume.shape[1]*initialVolume.shape[2])

    return rigidMatrix

def align3DCOM(npVolA, npVolB, verbose=False):
    #get the centers of mass
    comA = center_of_mass(npVolA)
    comB = center_of_mass(npVolB)

    if verbose:
        print 'comA', comA, '\t', 'comB: ', comB

    #find the disperity
    translationVector = np.subtract(comB, comA)

    #prep the vectorfor apply3DRigid
    translationVector = np.flipud(translationVector)
    translationVector = np.append(translationVector, 1.)
    transform = np.identity(4)
    transform[:,3]=translationVector

    if verbose:
        print 'transform: ', transform

    return apply3DRigid(npVolA, transform, verbose=verbose)

def simpleRegister(clusters1, clusters2, verbose=False):
    pairings = []
    this = len(clusters1)
    for clusterIdx in range(len(clusters1)):
        if verbose:
            print 'Progress: ', clusterIdx/float(this)
        lossList = [np.sum(abs(np.array(clusters1[clusterIdx].centroid) - np.array(elem.centroid))) for elem in clusters2]
        pairings.append((clusterIdx, np.argmin(lossList)))
    return pairings

def randomSubset(original, k):
    subset = []
    while len(subset) != k:
        chosen = original[rand(0, len(original))]
        if not chosen in subset:
            subset.append(chosen)
    return subset

def resolve(regList, toTrack = 50):

    #NOTE as of current this selects a random subset of 50 nodes to trace
    print 'here'
    toTrack = regList[0][:toTrack]
    #initialize a container for the final sequence
    seq = []

    #Follow each pairing like a thread
    for num, elem in enumerate(toTrack):
        print 'progress: ', num/50.
        print elem
        #initialize a container to hold the current thread
        myThread = [elem[0]]
        #starts at 1 since 0 seed is already in thread
        for tp in range(1, len(regList)):
            myThread.append(regLst[tp-1][myThread[-1]][1])
        seq.append(myThread)

    return seq
