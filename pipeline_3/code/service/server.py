import sys
sys.path.append("../functions")
import os
import boto3
from flask import Flask, redirect, url_for, request, render_template, session, flash

app = Flask(__name__)

def submitJob(name, bucket, data):
    client = boto3.client("batch")
    #createComputeEnvironment()
    #createJobQueue()
    #createJobDefinition()
    response = client.submit_job(
        jobName = str(name),
        jobQueue = "synapsys_jobs",
        jobDefinition = "synapsys_pipeline",
        containerOverrides = {
            "command": ["python", "runPipeline_3.py", bucket, data]
        }
    )

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html",
                            errorName = False,
                            errorBucket = False,
                            errorData = False)

@app.route("/submitJob", methods = ["GET", "POST"])
def submit():
    name = request.form["name"]
    bucket = request.form["bucket"]
    data = request.form["data"]
    errorName = False
    errorBucket = False
    errorData = False
    if len(name) == 0 or len(bucket) == 0:
        if len(name) == 0:
            errorName = True
        if len(bucket) == 0:
            errorBucket = True
        if len(data) == 0:
            errorData = True
        return render_template("index.html/",
                                errorName = errorName,
                                errorBucket = errorBucket,
                                errorData = errorData)
    else:
        submitJob(name, bucket, data)
        return render_template("analyze.html")

if __name__ == "__main__":
    app.run(debug = True, port = 8000)
