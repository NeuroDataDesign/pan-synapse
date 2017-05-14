import numpy as np
import scipy.io as sio

def loadMat(fileHandle):
    rawData = sio.loadmat(fileHandle)

    keys = rawData.keys()
    parsedKey = None
    for key in keys:
        if not '__' in key:
            parsedKey = key
            break

    if not parsedKey is None:
        return np.rollaxis(rawData[parsedKey], 2, 0)
        
    else:
        return None
