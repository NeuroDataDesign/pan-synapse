import pipeline as pipe
import mouseVis as mv
import plotly.offline as py
import cv2
import glob
import os
import csv
from tiffIO  import loadTiff
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
def runPipeline():
    if len(glob.glob('../../data/*_.tif')) != 0:
        fileList =  sorted(glob.glob('../../data/*_.tif'))
    else:
        sys.exit("FILE NOT FOUND")

    #Generate results form pipeline
    print 'Starting Pipeline'
    results = pipe.pipeline(loadTiff(fileList[0]), loadTiff(fileList[1]))

    #generate visualization
    #mv.generatePlotlyLineGraph(myID, results)

    #generate csv
    generateCSV(results)

    return

if __name__ == '__main__':
    runPipeline()
