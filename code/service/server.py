import sys
sys.path.append('../functions')
import os
import boto3
from flask import Flask, redirect, url_for, request, render_template, session, flash

app = Flask(__name__)

def submitJob(name, tp1, tp2):
    client = boto3.client('batch')
    response = client.submit_job(
        jobName = str(name),
        jobQueue = 'testqueue',
        jobDefinition = 'synapsys_pipeline:3',
        containerOverrides = {
            'command': ['python', 'runPipeline.py', tp1, tp2]
        }
    )

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html',
                            errorName = False,
                            errorTp1 = False,
                            errorTp2 = False )

@app.route('/submitJob', methods = ['GET', 'POST'])
def submit():
    tp1 = request.form['tp1']
    tp2 = request.form['tp2']
    name = request.form['name']
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
        return render_template('index.html/',
                                errorName = errorName,
                                errorTp1 = errorTp1,
                                errorTp2 = errorTp2,
                                name = name,
                                tp1 = tp1,
                                tp2 = tp2)
    else:
        submitJob(name, tp1, tp2)
        return render_template('analyze.html')

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
