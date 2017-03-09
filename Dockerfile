# existing image build
FROM ubuntu:16.04

#installing pip and essentials
RUN apt-get update
RUN apt-get -y install python-setuptools python-dev python-pip python-tk libglib2.0-0

#installing necessary modules
#dependencies
RUN apt-get -y install python-libtiff
RUN pip install numpy scipy matplotlib plotly scikit-image functools32 Pillow Flask Flask-SocketIO
RUN apt-get -y install libopencv-dev python-opencv

RUN cd
RUN mkdir data
RUN mkdir code
RUN mkdir code/functions
RUN mkdir code/service
RUN mkdir code/tests
#necessary code files
ADD ./code/functions ./code/functions
ADD ./code/service ./code/service
ADD ./code/tests/quality.py ./code/tests

RUN useradd -ms /bin/bash user
USER user
RUN cd ./code/service
CMD ["python", "server.py"]
