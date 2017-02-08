import sys
sys.path.append('../functions')
import os
import time
import base64
import thread

from flask import Flask, redirect, url_for, request, render_template, session
from flask_socketio import SocketIO, emit

import runPipeline as run
#generate the app object
app = Flask(__name__)

#configure the upload settings
UPLOAD_FOLDER = './static/data'
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
        return 403

def busy():
    while True:
        time.sleep(1)

@app.route('/blockServer', methods=['GET'])
def block():
    if request.method == 'GET':
        return render_template('block.html')

@socketio.on('blockStart', namespace='/block')
def blockStart():
    thread.start_new_thread(busy, ())
    print '\n\n\nBlocking Server\n\n\n'
    return

@socketio.on('connect', namespace = '/test')
def test_connect():
    print 'Connetion Established'

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
    emit('complete', namespace = '/test')
    print 'Complete Event Sent'

@app.route('/results', methods=['GET'])
def results():
    print 'Result Request Recieved'
    myID = 'static/results/' + str(request.headers['myID']) + '.html'
    print 'Results File Returned'
    return myID

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    # check if the post request has the file part
        if 'file' not in request.files:
            print "stopped here"
            return "no file uploaded"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print "shit"
            return "no file found"
            return redirect(request.url)
        if file and allowedFile(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "good shit"

if __name__ == '__main__':
    socketio.run(app, debug=True, port = 8080)
