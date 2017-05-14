import boto3
import sys
import argparse
sys.path.insert(0, "../functions")

def submitJob(bucket, name):
    try:
        createComputeEnvironment()
    except:
        print "Using existing Compute Environment."
    try:
        createJobQueue()
    except:
        print "Using existing Job Queue."
    try:
        createJobDefinition()
    except:
        print "Using existing Job Definition."
    response = client.submit_job(
        jobName = name.split('.')[0],
        jobQueue = "synapsys_jobs",
        jobDefinition = "synapsys_pipeline",
        containerOverrides = {
            "command": ["python", "runPipeline_3.py", bucket, name]
        }
    )

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
    print "JOB DEF:\n" + str(response)
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
    print "JOB QUEUE:\n" + str(response)
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
    print "COMPUTE ENV:\n" + response
    return "synapsys_ce"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synapsys pipeline on the cloud')
    parser.add_argument('bucket', type = str, help= 'Job name')
    parser.add_argument('name', type = str, help='The S3 bucket with the input dataset')
    #parser.add_argument('--AWS_SECRET_KEY', type = str, help = 'AWS Secret Keys')
    args = parser.parse_args()
    name = args.name
    bucket = args.bucket
    client = boto3.client('batch')
    submitJob(bucket, name)
