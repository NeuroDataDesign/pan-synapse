import sys
sys.path.append("../functions")
import os
import boto3
from flask import Flask, redirect, url_for, request, render_template, session, flash

app = Flask(__name__)

def submitJob(name, tp1, tp2):
    client = boto3.client("batch")
    createComputeEnvironment()
    createJobQueue()
    createJobDefinition()
    response = client.submit_job(
        jobName = str(name),
        jobQueue = "synapsys_jobs",
        jobDefinition = "synapsys_pipeline",
        containerOverrides = {
            "command": ["python", "runPipeline.py", tp1, tp2]
        }
    )

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

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html",
                            errorName = False,
                            errorTp1 = False,
                            errorTp2 = False )

@app.route("/submitJob", methods = ["GET", "POST"])
def submit():
    tp1 = request.form["tp1"]
    tp2 = request.form["tp2"]
    name = request.form["name"]
    errorName = False
    errorTp1 = False
    errorTp2 = False
    if len(name) == 0  or len(tp1) == 0 or len(tp2) == 0:
        if len(name) == 0:
            errorName = True
        if len(tp1) == 0:
            errorTp1 = True
        if len(tp2) == 0:
            errorTp2 = True
        return render_template("index.html/",
                                errorName = errorName,
                                errorTp1 = errorTp1,
                                errorTp2 = errorTp2,
                                name = name,
                                tp1 = tp1,
                                tp2 = tp2)
    else:
        submitJob(name, tp1, tp2)
        return render_template("analyze.html")

if __name__ == "__main__":
    app.run(debug = True, port = 8000)
