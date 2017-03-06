import numpy as np

def neighborhoodDensity(data, interPlane = 1, intraPlane = 1):
    output = np.zeros_like(data)
    for z in range(data.shape[0]):
        for y in range(data.shape[1]):
            for x in range(data.shape[2]):
                subVol = data[z-intraPlane:z+intraPlane, y-interPlane:y+interPlane, x-interPlane:x+interPlane]
                if not all(subVol.shape) == 0:
                    ave = np.average(subVol)
                    binSubVol = subVol > ave
                    output[z][y][x] = (np.count_nonzero(binSubVol)/float(interPlane*interPlane*intraPlane)) * data[z][y][x]
    return output
