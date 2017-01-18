# existing image build
FROM ubuntu
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

#installing pip
RUN apt-get update
RUN apt-get -y install python-pip

#installing necessary modules
#general dependencies
RUN pip install numpy
RUN pip install matplotlib
RUN pip install opencv-python
RUN pip install scipy
RUN pip install plotly
RUN pip install scikit-image
#tiffIO dependencies
RUN pip install functools32
RUN pip install Pillow
RUN pip install libtiff

#necessary code files
ADD ./code/functions/tiffIO.py
ADD ./code/functions/plosLib.py
ADD ./code/functions/cluster.py
ADD ./code/functions/
