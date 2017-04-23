import sys
sys.path.append('../functions')
import os
import boto3
from flask import Flask, redirect, url_for, request, render_template, session

app = Flask(__name__)

def submitJob(name, tp1, tp2):
    client = boto3.client('batch')
    response = client.submit_job(
        jobName = str(name),
        jobQueue = 'testqueue',
        jobDefinition = 'synapsys_pipeline:3',
        containerOverrides = {
            'command': ['python', 'testjob.py', tp1, tp2]
        }
    )

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/submitJob', methods = ['GET', 'POST'])
def submit():
    tp1 = request.form['tp1']
    tp2 = request.form['tp2']
    name = request.form['name']
    submitJob(name, tp1, tp2)
    return 'job submitted'

if __name__ == '__main__':
    app.run(debug = True, port = 8000)
