# existing image build
FROM ubuntu:16.04
#installing pip and essentials
RUN apt-get update
RUN apt-get -y install python-setuptools python-dev python-pip build-essential

#installing necessary modules
#dependencies
RUN apt-get -y install python-libtiff
RUN pip install numpy scipy matplotlib plotly scikit-image functools32 Pillow nibabel nipype medpy
RUN apt-get -y install libopencv-dev python-opencv

RUN apt-get -y install git
RUN apt-get -y install cmake
RUN apt-get -y install gcc
RUN apt-get -y install g++
RUN apt-get -y install zlib1g-dev

RUN mkdir /ANTS
RUN mkdir /workdirectory
WORKDIR ANTS
RUN git clone git://github.com/stnava/ANTs.git
RUN mkdir antsbin
WORKDIR /ANTS/antsbin
RUN cmake ../ANTs
RUN make -j 7

RUN cp /ANTS/ANTs/Scripts/* /ANTS/antsbin/bin/
ENV ANTSPATH ANTS/antsbin/bin

WORKDIR /workdirectory
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

#CMD ["python", "server.py"]
