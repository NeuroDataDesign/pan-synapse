import boto3
import sys
sys.path.insert(0, "../functions")

def submitJob(name, bucket, path, tp1, tp2):
    createComputeEnvironment()
    createJobQueue()
    createJobDefinition()
    response = client.submit_job(
        jobName = str(name),
        jobQueue = "synapsys_jobs",
        jobDefinition = "synapsys_pipeline",
        containerOverrides = {
            "command": ["python", "runPipeline.py", bucket, path, tp1, tp2]
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
            "command": ["python", "runPipeline.py"]
        },
    )
    print "JOB DEF:\n" + response
    return "synapsys_pipeline"

def createJobQueue(computeEnviron):
    response = client.create_job_queue(
        jobQueueName= "synapsys_jobs",
        state = "ENABLED",
        priority = 1,
        computeEnvironmentOrder = [
            {
                "order": 1,
                "computeEnvironment": computeEnviron
            }
        ],
    )
    print "JOB QUEUE:\n" + response
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
            "instanceTypes": ["t2.large"],
        },
    )
    print "COMPUTE ENV:\n" + response
    return "synapsys_ce"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synapsys pipeline on the cloud')
    parser.add_argument('bucket', type = str, help='The S3 bucket with the input dataset')
    parser.add_argument('path', type = str, help = 'The S3 folder with the input dataset')
    parser.add_argument('timepoint1', type = str, help = 'The key to the first timepoint file. Key '+
                                        'should be same as filename. Must be formated as '+
                                        'uniqueID_1.tif. e.g. jhu_1.tif')
    parser.add_argument('timepoint2', type = str, help = 'The key to the second timepoint file. Key '+
                                        'should be same as filename. Must be formated as '+
                                        'uniqueID_2.tif e.g. jhu_2.tif')
    parser.add_argument('--AWS_SECRET_KEY', type = str)
    args = parser.parse_args()
    bucket = args.bucket
    path = args.path
    tp1 = args.timepoint1
    tp2 = args.timepoint2
    submitJob(bucket, path, tp1, tp2)
