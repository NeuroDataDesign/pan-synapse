# existing image build
FROM ubuntu:16.04
#installing pip and essentials
RUN apt-get update
RUN apt-get -y install python-setuptools python-dev python-pip build-essential

#installing necessary modules
#dependencies
#RUN apt-get -y install python-libtiff
#RUN pip install numpy scipy matplotlib plotly scikit-image functools32 Pillow Flask Flask-SocketIO
#RUN apt-get -y install libopencv-dev python-opencv

RUN apt-get -y install git
RUN apt-get -y install cmake
RUN apt-get -y install gcc
RUN apt-get -y install g++
RUN apt-get -y install zlib1g-dev
RUN git clone git://github.com/stnava/ANTs.git /ANTs && cd /ANTs
RUN mkdir antsbin && cd antsbin
RUN cmake -D SuperBuild_ANTS_USE_GIT_PROTOC=OFF ../ANTs
RUN rm antsbin/ITKv4-build/CMakeCache.txt
RUN make -j 4

RUN cp /ANTs/Scripts/* /antsbin/bin/
ENV ANTSPATH /antsbin/bin

RUN cd
RUN mkdir data
RUN mkdir results
RUN mkdir code
RUN mkdir code/functions
#RUN mkdir code/service
#necessary code files
ADD ./code/functions ./code/functions
#ADD ./code/service ./code/service

RUN useradd -ms /bin/bash user
USER user
RUN cd ./code/service

#CMD ["python", "server.py"]
