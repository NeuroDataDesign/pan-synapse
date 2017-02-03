import sys
sys.path.append('../functions')

import time
import base64

from flask import Flask, redirect, url_for, request, render_template, session
from flask_socketio import SocketIO, emit

import runPipeline as run
#generate the app object
app = Flask(__name__)

#configure the upload settings
UPLOAD_FOLDER = '../../data'
ALLOWED_EXTENSIONS = 'tif'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#generate the async handler
async_mode = None
socketio = SocketIO(app, async_mode = async_mode)

def allowedFile(filename):
    return '.' in filename and filename.split('.')[1].lower() == ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:

        return 'shit'

@socketio.on('connect', namespace = '/test')
def test_connect():
    print ':DD'

@socketio.on('upload', namespace='/test')
def upload(message):
    #generate a unique id based on time of upload
    myID = str(time.time())[3:]

    #save the file
    rawDatList = message['file']
    for tp, rawDat in enumerate(rawDatList):
        fileDat = base64.b64decode(rawDat)
        with open(myID+'_' + str(tp) + '.tiff', 'wb') as f:
            f.write(fileDat)

    #emit a response on successful completion
    socketio.emit('response', {myID:myID})

@socketio.on('analyze', namespace = '/test')
def analyze():
    run.runPipeline('1123')
    print 'good'
    emit('complete', namespace = '/test')
    print 'complete event sent'

@app.route('/results', methods=['GET'])
def results():

    myID = 'static/results/' + str(request.headers['myID']) + '.html'
    print myID
    return render_template('results.html', myID=myID)

if __name__ == '__main__':
    socketio.run(app, debug=True, port = 8080)
