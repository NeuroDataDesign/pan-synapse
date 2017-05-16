import boto3
import sys
import argparse
import time

client = boto3.client('batch')

def uploadData(bucket, data, key):
    s3 = boto3.resource('s3')
    data = open(data, 'rb')
    s3.Bucket(bucket).put_object(Key=key, Body=data)
    return key

def getResults(bucket, resultsdir, key):
    s3 = boto3.resource('s3')
    filename = resultsdir + '/' + key + '_results.dat'
    data = s3.meta.client.download_file(bucket, key + '_results.dat', filename)
    return key

def submitJob(bucket, name):
    try:
        createComputeEnvironment()
    except:
        print "Using existing Compute Environment."
    time.sleep(3)
    try:
        createJobQueue()
    except:
        print "Using existing Job Queue."
    time.sleep(3)
    try:
        createJobDefinition()
    except:
        print "Using existing Job Definition."
    time.sleep(3)
    response = client.submit_job(
        jobName = name.split('.')[0],
        jobQueue = "synapsys_jobs",
        jobDefinition = "synapsys_pipeline",
        containerOverrides = {
            "command": ["python", "runPipeline_3.py", bucket, name]
        }
    )
    print "Submitted Job"

def verifyCredentials():
    return

def createJobDefinition():
    response = client.register_job_definition(
        jobDefinitionName= "synapsys_pipeline",
        type = "container",
        containerProperties = {
            "image": "389826612951.dkr.ecr.us-east-1.amazonaws.com/synapsys",
            "vcpus": 2,
            "memory": 5000,
            "command": ["python", "runPipeline_3.py"]
        },
    )
    print "Created job definition"
    return "synapsys_pipeline"

def createJobQueue():
    response = client.create_job_queue(
        jobQueueName= "synapsys_jobs",
        state = "ENABLED",
        priority = 1,
        computeEnvironmentOrder = [
            {
                "order": 1,
                "computeEnvironment": "synapsys_ce"
            }
        ],
    )
    print "Created Job Queue"
    return "synapsys_jobs"

def createComputeEnvironment():
    response = client.create_compute_environment(
        computeEnvironmentName = "synapsys_ce",
        type = "MANAGED",
        state = "ENABLED",
        computeResources = {
            "type": "EC2",
            "minvCpus": 0,
            "maxvCpus": 256,
            "desiredvCpus": 0,
            "instanceTypes": ["m4.large"],
            "subnets": ["subnet-17c65f72", "subnet-75006549", "subnet-4e2ace06", "subnet-7ca59151", "subnet-74f3d02f"],
            "securityGroupIds": ["sg-41927a3e"],
            "instanceRole": "arn:aws:iam::389826612951:instance-profile/ecsInstanceRole",
        },
        serviceRole='arn:aws:iam::389826612951:role/service-role/AWSBatchServiceRole'
    )
    iam = boto3.client('iam')
    response = iam.attach_role_policy(
        RoleName = "ecsInstanceRole",
        PolicyArn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
    )
    print "Updated role permissions"
    print "Created compute environment"
    return "synapsys_ce"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synapsys pipeline on the cloud')
    parser.add_argument('bucket', type = str, help= 'Job name')
    parser.add_argument('name', type = str, help='The S3 bucket with the input dataset')
    #parser.add_argument('--AWS_SECRET_KEY', type = str, help = 'AWS Secret Keys')
    args = parser.parse_args()
    name = args.name
    bucket = args.bucket
    submitJob(bucket, name)
