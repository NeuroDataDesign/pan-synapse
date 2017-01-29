import sys
sys.path.insert(0, '../functions/')
import pipeline as pipe
import glob
import os

###### FOR DOCKER ######
def runPipelineAndGetResults():
    if len(glob.glob('../../data/*.tif')) != 0:
        fileName =  glob.glob('../../data/*.tif')[0]
        print 'Image: ' + fileName
    else:
        sys.exit("FILE NOT FOUND")

    print "Starting Pipeline"
    pipe.pipeline(fileName)
    print "Analyzing and storing results"
