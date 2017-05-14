# existing image build
FROM ubuntu:16.04

#installing pip and essentials
RUN apt-get update
RUN apt-get -y install python-setuptools python-dev python-pip build-essential

RUN pip install numpy scipy scikit-image boto3
RUN mkdir /workdirectory

WORKDIR /workdirectory
RUN mkdir data
RUN mkdir code
RUN mkdir code/functions
ADD ./code/functions ./code/functions

WORKDIR /workdirectory/code/functions
CMD ["python", "runPipeline.py"]
