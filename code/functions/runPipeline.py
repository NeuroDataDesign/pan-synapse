import pipeline as pipe
import mouseVis as mv
import plotly.offline as py
import cv2
import glob
import os
import csv
from cluster import Cluster

def generateCSV(results):
    myOutput = []
    for elem in results:
        centroid1 = elem.getCentroid()
        centroid2 = elem.timeRegistration.getCentroid()
        myOutput.append([centroid1[0], centroid1[1], centroid1[2], elem.getVolume(),
                         centroid2[0], centroid2[1], centroid2[2], elem.timeRegistration.getVolume()])

    with open('../../results','w') as outFile:
        scribe = csv.writer(outFile)
        scribe.writerows(myOutput)

    print 'pipeline complete'


#This library is designed to act as the driver for the docker and the web service
def runPipeline(myID):
    if len(glob.glob('../../data/*.tif')) != 0:
        fileList =  sorted(glob.glob('../../data/*.tif'))
    else:
        sys.exit("FILE NOT FOUND")

    #Generate results form pipeline
    print 'Starting Pipeline'
    results = pipe.pipeline(fileList[0], fileList[1], verbose=False)

    #generate visualization
    #mv.generatePlotlyLineGraph(myID, results)

    #generate csv
    generateCSV(myID, results)

    return
