import sys
sys.path.insert(0, '../functions/')
import pipeline as pipe
import mouseVis as mv
import plotly.offline as py
import cv2
import glob
import os

#This library is designed to act as the driver for the docker and the web service
def runPipeline(myID):
    if len(glob.glob('../../data/*.tif')) != 0:
        fileList =  glob.glob('../service/static/data/' + str(myID) + '_*.tif')
    else:
        sys.exit("FILE NOT FOUND")

    print "Starting Pipeline"
    results = pipe.pipeline(fileList)
