FROM debian:jessie
MAINTAINER Déruaz Vincent <vincent.deruaz@master.hes-so.ch>

RUN apt-get update

USER root

# Install all OS dependencies for fully functional notebook server
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -yq --no-install-recommends \
    git \
    vim \
    jed \
    emacs \
    wget \
    build-essential \
    python-dev \
    ca-certificates \
    bzip2 \
    unzip \
    libsm6 \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    sudo \
    locales \
    libxrender1 \
    nano \
    openssh-server \
    mysql-server mysql-client libmysqlclient-dev \
    python-pip

RUN apt-get install -y python3-pip r-base

RUN pip3 install numpy --upgrade
RUN pip3 install biopython
RUN pip3 install mysqlclient
RUN pip3 install docker-py

RUN mysqld &
RUN service mysql start

RUN apt-get install -y build-essential python-dev libmysqlclient-dev
RUN apt-get install -y python-mysqldb

RUN apt-get install -y python-pip
RUN pip install mysql-connector

RUN mkdir /tmp/inphinity
RUN chmod 0777 /tmp/inphinity

RUN apt-get install -y curl
RUN curl -fsSL https://get.docker.com/ | sh

WORKDIR /