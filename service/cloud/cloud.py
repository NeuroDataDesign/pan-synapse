## cloud methods for storing data on s3, retrieivng results, and submitting batch job
import os
import sys
import boto3
import uuid
sys.path.insert(0, '../')

#takes in name of data file (string)
#returns key for data
def uploadData(inputData):
    s3 = boto3.resource('s3')
    key = str(uuid.uuid1().int) + '.txt'
    data = open(inputData, 'rb')
    s3.Bucket('nddtestbucket').put_object(Key=key, Body=data)
    return key

#takes in string data directory and key for S3 object
def getData(key, datadir):
    s3 = boto3.resource('s3')
    filename = datadir + '/' + key
    data = s3.meta.client.download_file('nddtestbucket', key, filename)
    return filename

def submitJob(key):
    client = boto3.client('batch')
    response = client.submit_job(
        jobName = key.split('.')[0],
        jobQueue = 'testqueue',
        jobDefinition = 'testcloudjob',
        containerOverrides = {
            'command': ['python', 'testjob.py', key]
        }
    )

key = uploadData("data.txt")
submitJob(key)
