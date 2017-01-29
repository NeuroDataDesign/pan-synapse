import sys
sys.path.insert(0, '../functions/')
import runPipeline as run
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import os
import glob

UPLOAD_FOLDER = '../../data'
ALLOWED_EXTENSIONS = set(['tiff'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowedFile(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if request.method == 'GET':
        return render_template('index.html')
'''
    if request.method == 'POST':
        # os.system("docker exec 'docker ps -q' )
        run.runPipeline()
        print "Done"
        return redirect('http://localhost:5000/analyze')'''

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowedFile(f):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return render_template('analyze.html')
        else:
            return 'file not found or not in correct format'

@app.route('/analyze', methods = ['GET', 'POST'])
def analyze():
    if request.method == 'GET':
        run.runPipeline()
        print "Done"
        return "Analyzing Data"

if __name__ == '__main__':
    app.run(debug=True)
