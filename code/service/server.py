import sys
sys.path.append('../functions')
import runPipeline as run
from flask import Flask, redirect, url_for, request, render_template
import thread
import os
import glob

UPLOAD_FOLDER = '../../data'
ALLOWED_EXTENSIONS = 'tif'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowedFile(filename):
    return '.' in filename and filename.split('.')[1].lower() == ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if allowedFile(request.files['file'].filename):
            f = request.files['file']
            if f:
                print os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
                return render_template('analyze.html')
            else:
                return 'File does not exist.'
        else:
            return 'File Type Not Allowed'

@app.route('/analyze', methods = ['GET'])
def analyze():
    if request.method == 'GET':
        run.runPipeline()
        print "Done"
        ## TODO: FLUSH data directory
        return redirect(url_for('results'))
        ## TODO: Have form on results.html for save file or exit. Should link to finish.
        ## TODO: Have so if close window, automatically flush results.

@app.route('/results', methods = ['GET', 'POST'])
def results():
    return render_template('results.html')

@app.route('/save', methods = ['GET', 'POST'])
def finish():
    ## TODO: FLUSH results directory
    return 'Here are the results'

if __name__ == '__main__':
    app.run(debug=True, threaded = True)
