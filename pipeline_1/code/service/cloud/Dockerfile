FROM ubuntu:16.04
RUN apt-get update
RUN apt-get -y install python-setuptools python-dev python-pip

RUN pip install boto3
RUN mkdir workdir
RUN cd workdir
ADD ./testjob.py ./testjob.py
RUN mkdir data
