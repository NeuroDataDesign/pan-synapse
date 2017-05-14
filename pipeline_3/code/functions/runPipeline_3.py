import pipeline as pipe
import cluster
import matIO as io
import numpy as np
import glob
import sys
import os
import csv
import boto3
import argparse
import pickle

def generateCSV(results):
    myOutput = []
    for elem in results:
        centroid1 = elem.getCentroid()
        myOutput.append([centroid1[0], centroid1[1], centroid1[2], elem.getVolume()])

    with open('../../results/results.csv','w') as outFile:
        scribe = csv.writer(outFile)
        scribe.writerows(myOutput)

    print 'CSV generated'

def uploadResults(bucket, result_key, results):
    s3 = boto3.resource('s3')
    data = open(results, 'rb')
    s3.Bucket(bucket).put_object(Key=result_key, Body=data)
    return result_key

def getData(bucket, key, datadir):
    s3 = boto3.resource('s3')
    filename = datadir + '/' + key
    try:
        data = s3.meta.client.download_file(bucket, key, filename)
    except:
        sys.exit('File does not exist, or incorrect bucket/key')
    return key

#This library is designed to act as the driver for the docker and the web service
def runPipeline(bucket, key):
    print 'Getting Data'
    #getData(bucket, key, '../../data')
    if len(glob.glob('../../data/*.mat')) != 0:
        fileList =  sorted(glob.glob('../../data/*.mat'))
    else:
        sys.exit("MAT File not found, Exiting...")
    data = np.array(io.loadMat('../../data/' + key))
    print 'Starting Pipeline'
    results = pipe.pipeline(data)
    result_key = key + '_results.dat'

    print 'Generating Results'
    #generateCSV(results)
    pickle.dump(results, open('../../results/out.dat', 'w'))

    print 'Uploading Results'
    uploadResults(bucket, result_key, '../../results/out.dat')
#ADD other result formats (visuals, etc)
    print 'Synapsys finished'
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synapsys pipeline on the cloud')
    parser.add_argument('bucket', type = str, help='The S3 bucket with the input dataset')
    parser.add_argument('name', type = str, help = 'The name of the file')
    args = parser.parse_args()
    bucket = args.bucket
    name = args.name
    runPipeline(bucket, name)
