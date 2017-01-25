# existing image build
FROM ubuntu:16.04

#installing pip and essentials
RUN apt-get update
RUN apt-get -y install python-setuptools python-dev python-pip python-tk libglib2.0-0

#installing necessary modules
#dependencies
RUN cd /
RUN apt-get -y install python-libtiff
RUN pip install numpy scipy matplotlib plotly scikit-image functools32 Pillow
RUN apt-get -y install libopencv-dev python-opencv

RUN mkdir data
RUN mkdir code
RUN mkdir code/functions
#necessary code files
ADD ./code/functions ./code/functions
