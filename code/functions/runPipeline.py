import sys
sys.path.insert(0, '../functions/')
import pipeline as pipe
import mouseVis as mv
import plotly.offline as py
import cv2
import glob
import os

###### FOR DOCKER ######
def runPipeline():
    if len(glob.glob('../../data/*.tif')) != 0:
        fileName =  glob.glob('../../data/*.tif')[0]
        print 'Image: ' + fileName
    else:
        sys.exit("FILE NOT FOUND")

    print "Starting Pipeline"
    results = pipe.pipeline(fileName)
    cv2.imwrite("../service/static/results/PipelineImg.png", results[0])

    print "Analyzing and storing results"
