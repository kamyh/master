FROM ubuntu:16.04
MAINTAINER Déruaz Vincent <vincent.deruaz@master.hes-so.ch>

# avoid needing -y instal option
ENV DEBIAN_FRONTEND noninteractive

# Packages installations
RUN echo 'deb http://archive.ubuntu.com/ubuntu xenial multiverse' >> /etc/apt/sources.list \
	 	 && apt-get update \
		 && apt-get upgrade -y --force-yes \
		 && apt-get install -y --force-yes \
        build-essential \
        git \
        python3-numpy \
        wget \
        gcc \
        g++ \
        python3-dev \
        unzip \
        make \
        python3-matplotlib \
        python3-reportlab \
        python3-pip r-base \
        clustalw \
        fasttree \
        t-coffee python3-pil \
        bwa \
        ncbi-blast+ \
        emboss \
        clustalo \
        phylip \
        mafft \
        muscle \
        samtools \
        phyml \
        wise \
        raxml \
        language-pack-en \
        paml \
        probcons \
        python3-pandas \
        python3.5-dev \
        libxft-dev \
        && apt-get clean

# Installing some Bio-lib and cython using pip3
RUN pip3 install rdflib --upgrade \
    && pip3 install cython --upgrade \
    && pip3 install numpy --upgrade \
    && pip3 install Pillow --upgrade \
    && pip3 install matplotlib --upgrade \
    && pip3 install pandas --upgrade

#Biopython
RUN git clone https://github.com/biopython/biopython.git
WORKDIR /biopython
RUN python3.5 setup.py install

# Copy bio python test script
RUN mkdir /src
RUN mkdir /src/biopython_alone
COPY /src/biopython_alone/* ./src/biopython_alone/
WORKDIR /src/biopython_alone

#set default python version to 3.5
RUN touch ~/.bash_aliases \
	  && echo alias python=\'python3.5\' > ~/.bash_aliases