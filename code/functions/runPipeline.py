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
import argparse

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

def uploadResults(bucket, s3dir, key, results):
    s3 = boto3.resource('s3')
    key = s3dir + '/' + key + '_results' + '.csv'
    data = open(results, 'rb')
    s3.Bucket(bucket).put_object(Key=key, Body=data)
    return key

def uploadData(bucket, s3dir, keys):
    s3 = boto3.resource('s3')
    for key in keys:
        data = open('../../data/' + key)
        s3.Bucket(bucket).put_object(Key = s3dir + '/' + key, Body = data)

def getData(bucket, s3dir, keys, datadir):
    s3 = boto3.resource('s3')
    for key in keys:
        filename = datadir + '/' + key
        data = s3.meta.client.download_file(bucket, s3dir + '/' + key, filename)
    return keys

#This library is designed to act as the driver for the docker and the web service
#Files MUST be named 'key_i.tif' where i is integer of time point.
def runPipeline(bucket, s3dir, keys):
    getData(bucket, s3dir, keys, '../../data')
    if len(glob.glob('../../data/*.tif')) != 0:
        fileList =  sorted(glob.glob('../../data/*.tif'))
    else:
        sys.exit("FILE NOT FOUND")
    #Generate results form pipeline
    print 'Starting Pipeline'
    results = pipe.pipeline(loadTiff(fileList[0]), loadTiff(fileList[1]))
    result_key = keys[0].split('_')[0]
    #generate visualization
    #mv.generatePlotlyLineGraph(myID, results)

    #generate csv
    generateCSV(results)
    uploadResults(bucket, s3dir, result_key, '../../results/results.csv')

    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synapsys pipeline on the cloud')
    parser.add_argument('--bucket', type = str, help='The S3 bucket with the input dataset')
    parser.add_argument('--dir', type = str, help = 'The S3 folder with the input dataset')
    parser.add_argument('--timepoint1', type = str, help = 'The key to the first timepoint file. Key'
                                        'should be same as filename. Must be formated as
                                        'uniqueID_1.tif. e.g. jhu_1.tif')
    parser.add_argument('--timepoint2', type = str, help = 'The key to the second timepoint file. Key'
                                        'should be same as filename. Must be formated as
                                        'uniqueID_2.tif e.g. jhu_2.tif')
    args = parser.parse_args()
    bucket = args.bucket
    path = args.dir
    tp1 = args.timepoint1
    tp2 = args.timepoint2
    #uploadData(sys.argv[1], sys.argv[2:])
    runPipeline(bucket, path, [tp1, tp2])
