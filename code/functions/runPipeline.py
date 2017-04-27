import pipeline as pipe
import mouseVis as mv
import plotly.offline as py
import cv2
import glob
import sys
import os
import csv
from tiffIO  import loadTiff
from cluster import Cluster
import boto3

def generateCSV(results):
    myOutput = []
    for elem in results:
        centroid1 = elem.getCentroid()
        centroid2 = elem.timeRegistration.getCentroid()
        myOutput.append([centroid1[0], centroid1[1], centroid1[2], elem.getVolume(),
                         centroid2[0], centroid2[1], centroid2[2], elem.timeRegistration.getVolume()])

    with open('../../results/results.csv','w') as outFile:
        scribe = csv.writer(outFile)
        scribe.writerows(myOutput)

    print 'pipeline complete'

def uploadResults(s3dir, key, results):
    s3 = boto3.resource('s3')
    key = s3dir + '/' + key + '_results' + '.csv'
    data = open(results, 'rb')
    s3.Bucket('nddtestbucket').put_object(Key=key, Body=data)
    return key

def getData(s3dir, keys, datadir):
    s3 = boto3.resource('s3')
    for key in keys:
        filename = datadir + '/' + key
        data = s3.meta.client.download_file('nddtestbucket', s3dir + '/' + key, filename)
    return keys

#This library is designed to act as the driver for the docker and the web service
#Files MUST be named 'key_i.tif' where i is integer of time point.
def runPipeline(keys):
    getData(keys, '../../data')
    if len(glob.glob('../../data/*.tif')) != 0:
        fileList =  sorted(glob.glob('../../data/*.tif'))
    else:
        sys.exit("FILE NOT FOUND")
    #Generate results form pipeline
    print 'Starting Pipeline'
    results = pipe.pipeline(loadTiff(fileList[0]), loadTiff(fileList[1]))
    key = keys[0].split('_')[0]
    #generate visualization
    #mv.generatePlotlyLineGraph(myID, results)

    #generate csv
    generateCSV(results)
    uploadResults(key, '../../results/results.csv')

    return

if __name__ == '__main__':
    runPipeline(sys.argv[1:])
