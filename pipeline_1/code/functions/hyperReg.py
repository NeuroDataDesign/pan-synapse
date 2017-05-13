import math

import numpy as np

from scipy.ndimage.measurements import center_of_mass

from random import randrange as rand
from random import uniform as floatRand

def get3DRigid(roll=0,
               pitch=0,
               yaw=0,
               zT=0,
               yT=0,
               xT=0):

    a = yaw
    b = pitch
    c = roll
    xt = xT
    yt = yT
    zt = zT

    #generate the transform
    transform = np.stack([
        [math.cos(a)*math.cos(b), math.cos(a)*math.sin(b)*math.sin(c)-math.sin(a)*math.cos(c), math.cos(a)*math.sin(b)*math.cos(c)+math.sin(a)*math.sin(c), xt],
        [math.sin(a)*math.cos(b), math.sin(a)*math.sin(b)*math.sin(c)+math.cos(a)*math.cos(c), math.sin(a)*math.sin(b)*math.cos(c)-math.cos(a)*math.sin(c), yt],
        [-math.sin(b), math.cos(b)*math.sin(c), math.cos(b)*math.cos(c), zt],
        [0., 0., 0., 1.]
    ])
    return transform


def apply3DRigidVolume(initialVolume, transform, originZ, originY, originX, verbose=False):
    #create a body to hold return values
    rigidMatrix = np.zeros_like(initialVolume)

    #create var to keep track of out of bounds percent
    out = 0.
    sigOut = 0.

    #convert every voxel
    for z in range(initialVolume.shape[0]):
        print z/float(initialVolume.shape[0])
        for y in range(initialVolume.shape[1]):
            for x in range(initialVolume.shape[2]):

                #shift the volume so that the transform is applied to the center, and not the top left back edge
                shift = [originX, originY, originZ]
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

def apply3DRigid(pointList, transform, originZ, originY, originX, verbose=False):
    #create var to keep track of out of bounds percent
    out = 0.
    sigOut = 0.

    #convert every voxel
    for voxel in pointList:

        z = voxel[0]
        y = voxel[1]
        x = voxel[2]

        #shift the volume so that the transform is applied to the center, and not the top left back edge
        shift = [originX, originY, originZ]
        shiftedPoint = list(np.subtract([x, y, z], shift))
        shiftedPoint.append(1.)

        #calculate the transform, drop the irrelavent 1 at the end
        new = np.dot(transform, shiftedPoint)[:3]

        #shift the volume back to its original spot after transform
        final = np.add(new, shift)
        return list(reversed(final))

def parseTransformFile(filePath):
    with open(filePath, 'r') as transformFile:
        content = transformFile.readlines()

    #strip whitespace
    content = [line.strip() for line in content]

    originZ, originY, originX, = None, None, None
    roll, pitch, yaw = None, None, None
    zT, yT, xT = None, None, None

    for line in content:
        if 'CenterOfRotationPoint' in line:
            params = line.split()
            originZ = float(params[1])
            originY = float(params[2])
            #the comprehension at the end is to remove the trailing )
            originX = float(params[3][:-1])

        #The leading ( is there to make sure that 'InitialTransformParameters is not grabbed
        if '(TransformParameters' in line:
            params = line.split()
            roll = float(params[1])
            pitch = float(params[2])
            yaw = float(params[3])
            zT = float(params[4])
            yT = float(params[5])
            #the comprehension at the end is to remove the trailing )
            xT = float(params[6][:-1])

    matrix = get3DRigid(
        roll=roll,
        pitch=pitch,
        yaw=yaw,
        zT=zT,
        yT=yT,
        xT=xT
    )

    return {'originZ':originZ, 'originY':originY, 'originX':originX, 'matrix':matrix}
