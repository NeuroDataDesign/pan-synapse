import math

import numpy as np
import SimpleITK as itk

from scipy.ndimage.measurements import center_of_mass

from random import randrange as rand
from random import uniform as floatRand

class accumulator:
    def __init__(self, tolerance):
        self.tolerance = tolerance
        self.voteList = []

    def vote(self, pitchToAdd, yawToAdd, rollToAdd):
        #TODO this could be way more efficient but its late and im tired
        inserted = False
        for index, angleVotePair in self.voteList:
            angleSet = angleVotePair[0]

            pitch = angleSet[0]
            yaw = angleSet[1]
            roll = angleSet[2]

            if abs(pitch-pitchToAdd)<self.tolerance and abs(yaw-yawToAdd)<self.tolerance and abs(roll-rollToAdd)<self.tolerance:
                self.voteList[index] = [self.voteList[index][0], self.voteList[index][1]+1]
                inserted = True
                break

        if not inserted:
            self.voteList.append([[pitch, yaw, roll], 1])

    def elect(self):
        self.voteList.sort(key=lambda x:x[1])
        return voteList[0][0]

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
    comA = center_of_mass(npVolA)
    comB = center_of_mass(npVolB)
    translationVector = np.subtract(comB, comA)
    translationVector = np.append(translationVector, 1.)
    transform = np.identity(4)
    transform[:,3]=translationVector
    return apply3DRigid(npVolA, transform, verbose=verbose)

def get3DPointRadialDensity(z, y, x, volume, radius):
    neighborhood = volume[z-radius: z+radius, y-radius: y+radius, x-radius: x+radius]
    return np.count_nonzero(neighborhood)

def generate3DRadialDensityVolume(volume, radius):
    rdv = np.zeros_like(volume)
    for z in range(volume.shape[0]):
        for y in range(volume.shape[1]):
            for x in range(volume.shape[2]):
                density = get3DPointRadialDensity(z, y, x, volume, radius)
                rdv[z][y][x] = density
    return rdv

def randomSubset(original, k):
    subset = []
    while len(subset) != k:
        chosen = original[rand(0, len(original))]
        if not chosen in subset:
            subset.append(chosen)
    return subset

def getRadialOffset(point, pair):
    '''
    The following defines the definition convention of this program
    pitch = c = y axis
    yaw = a = z axis
    roll = b = x axis
    '''

    #get the rotation matrix
    x = (np.cross(point, pair))/(np.linalg.norm(np.cross(point, pair)))
    theta = math.acos((np.dot(point, pair))/(np.linalg.norm(np.dot(point, pair))))
    a = [[0, -x[2], x[1]],
         [x[2], 0, -x[0]],
         [-x[1], x[0], 0]]
    i = np.identity(3)
    r = i + math.sin(theta)*a + (1-math.cos(theta))*(np.linalg.matrix_power(r, 2))

    #retrieve corresponding euler angles
    pitch = math.atan2(r[2][1], r[2][2])
    yaw = math.atan2(r[1][0], r[0][0])
    roll = -1*math.asin(r[2][0])

    return pitch, yaw, roll

def getRDVAloss(rdvA, rdvB, selected, transform):
    transformedPoints = []
    loss = 0.
    #point order is x, y, z
    for point in selected:
        toTransform = np.concatenate(point, [1.])
        result = np.dot(transform, toTransform)
        loss = loss + (rdvA[point[2]][point[1]][point[0]] - rdvB[result[2]][result[1]][result[0]])**2

    return loss

def get3DRadialDensityVolumeAlignment(rdvA, rdvB, epsilon, radiusDelta, selectionRatio = .05, precision = .01):
    #randomly select a subset of points density alignment
    candidates = zip(*np.nonzero(rdvA)) #assigns points in x, y, z order
    numPoints = round(selectionRatio * len(candidates))
    selected = randomSubset(candidates, numPoints)

    #initialize the accumulator
    myTallyBot = accumulator(precision)

    #DEBUG NOTE NOTE NOTE
    num = 0

    #begin the voting loop
    for point in selected:

        #DEBUG NOTE NOTE NOTE
        num+=1.
        print 'progress: ', num/float(len(selected))

        #get the radial density of the current point
        curRD = rdvA[point[0], point[1], point[2]] #0, 1, 2, since RDVA is in zyx orientation
        #get the radius of the current point
        pointR = math.sqrt(point[2]**2 + point[1]**2 + point[0]**2)

        #iterate over all radial density matches in the epsilon range
        for pairRD in range(int(curRD-epsilon), int(curRD+epsilon)):
            #TODO this may be faster if I check radius, then value
            #get all pairs where the radial density values are the same
            firstBatch = zip(*np.where(rdvB==pairRD)) #this returns in x, y, z
            potentialPairs = []

            #only consider pairs within epsilon of the original point's fixed unit sphere
            for pair in firstBatch:
                pairR = math.sqrt(pair[2]**2 + pair[1]**2 + pair[0]**2)
                if abs(pointR - pairR) < radiusDelta:
                    #append the projection of the pair point onto the unit sphere
                    potentialPairs.append([elem/float(np.linalg.norm(pair))*pointR for elem in pair])

            optimalAng = None
            optimalLoss = None
            for pair in potentialPairs:
                #get euler angles associated with radial offset of points
                pitch, yaw, roll = getRadialOffset(point, pair)
                #get transform corresponding to required angles
                transform = get3DRigid(pitch=pitch, yaw=yaw, roll=roll, xT=0., yT=0., zT=0.)

                #get the loss for this transform and point selection
                loss = getRDVAloss(rdvA, rdvB, selected, transform)
                if optimalLoss is None or loss < optimalLoss:
                    optimalLoss = loss
                    optimalAng = [pitch, yaw, roll]

            #append vote to accumulator
            if not optimalAng is None:
                myTallyBot.vote(optimalAng[0], optimalAng[1], optimalAng[2])

    #evaluate the results of the accumulator
    return myTallyBot.elect()


'''
PARAMS
------
radius - size of neigborhood for radial density calculation
epsilon - slack var for difference in radial density
radiusDelta - slack var for divergence in spherical level set
selectionRatio - ratio of data selected for monte carlo election
precision - how close two transfrorms can be before one counts as a vote for the other
'''
def register(npVolA, npVolB, radius, epsilon, radiusDelta, selectionRatio, precision):
    centeredVolA = align3DCOM(npVolA, npVolB)
    rdvA = generate3DRadialDensityVolume(centeredVolA, radius)
    rdvB = generate3DRadialDensityVolume(npVolB, radius)
    eAng = get3DRadialDensityVolumeAlignment(rdvA, rdvB, epsilon=epsilon, radiusDelta=radiusDelta, selectionRatio=selectionRatio, precision=precision)
    return apply3DRigid(centeredVolA,
                        pitch =eAng[0],
                        yaw=eAng[1],
                        roll=eAng[2],
                        zT=0.,
                        yT=0.,
                        xT=0.)
