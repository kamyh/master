FROM centos:latest
MAINTAINER Déruaz Vincent <vincent.deruaz@master.hes-so.ch>

# Packages installations
RUN yum install -y wget unzip zip tar git nano
RUN yum install -y git gcc-c++

# Python and Cython installations
RUN yum install -y python-setuptools python3-pip Cython python3-dev \
	python-genshi epydoc \
	python-matplotlib numpy scipy

# Copy first simple example
RUN mkdir simple_example
COPY simple_example/* ./simple_example/
WORKDIR simple_example

# Copy benchmark
RUN mkdir benchmark
COPY benchmark/* ./benchmark/
WORKDIR benchmark