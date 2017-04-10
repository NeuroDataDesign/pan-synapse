import pipeline as pipe
import mouseVis as mv
import plotly.offline as py
import cv2
import glob
import os
import csv
from cluster import Cluster

def generateCSV(myID, results):
    myOutput = []
    for elem in results:
        centroid1 = elem.getCentroid()
        centroid2 = elem.timeRegistration.getCentroid()
        myOutput.append([centroid1[0], centroid1[1], centroid1[2], elem.getVolume(),
                         centroid2[0], centroid2[1], centroid2[2], elem.timeRegistration.getVolume()])

    with open('../service/static/results/' + str(myID)+'.csv','w') as outFile:
        scribe = csv.writer(outFile)
        scribe.writerows(myOutput)


#This library is designed to act as the driver for the docker and the web service
def runPipeline(myID):
    if len(glob.glob('../../data/*.tif')) != 0:
        fileList =  glob.glob('../service/static/data/' + str(myID) + '_*.tif')
    else:
        sys.exit("FILE NOT FOUND")

    #Generate results form pipeline
    print 'Starting Pipeline'
    results = pipe.pipeline(fileList, verbose=True)

    #generate visualization
    #mv.generatePlotlyLineGraph(myID, results)

    #generate csv
    generateCSV(myID, results)

    return
