import sys
sys.path.insert(0, '../functions/')
import pipeline as pLine
import glob
import os

###### FOR DOCKER ######
if len(glob.glob('../../data/*.tif')) != 0:
    fileName =  glob.glob('../../data/*.tif')[0]
    print 'Image: ' + fileName
else:
    sys.exit("FILE NOT FOUND")

print "Starting Pipeline"
pLine.pipeline(fileName)
print "Done"
