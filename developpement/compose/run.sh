#!/usr/bin/env bash

sudo rm -R /inphinity-data/mysql

docker-compose down

docker-compose build

#Doesn't need to run hmmer image for now
docker-compose up -d database core