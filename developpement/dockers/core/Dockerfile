FROM debian:jessie
MAINTAINER Déruaz Vincent <vincent.deruaz@master.hes-so.ch>

RUN apt-get update
RUN apt-get install -y build-essential python-dev libmysqlclient-dev
RUN apt-get install -y python-mysqldb

ADD run.sh run.sh

RUN mkdir /tmp/inphinity
RUN chmod 0777 /tmp/inphinity

USER root
