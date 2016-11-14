FROM centos:latest
MAINTAINER Déruaz Vincent <vincent.deruaz@master.hes-so.ch>

# Prepare Os to packages installations
RUN yum -y clean all
RUN yum -y update

# Packages installations
RUN yum -y install epel-release
RUN yum -y install gcc gcc-c++ make wget tar gzip

# Get source code from http://hmmer.org/download.html
RUN wget http://eddylab.org/software/hmmer3/3.1b2/hmmer-3.1b2.tar.gz
RUN tar -xzvf hmmer-3.1b2.tar.gz

# Hmmer installation
WORKDIR hmmer-3.1b2
RUN ./configure
RUN make
RUN make install

EXPOSE 22

# Starting point
WORKDIR /usr/local/bin
