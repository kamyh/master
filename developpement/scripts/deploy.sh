#!/usr/bin/env bash

git clone https://github.com/kamyh/master.git

cd ./master/developpement/dockers/core/data-hmm/
sh get_pfam_hmm.sh

cd ../../database/data/
#others .sql files are directly on the git repository
wget https://www.dropbox.com/s/mzt9pxpfnvxl3wa/bacteriaVD.sql?dl=0
mv bacteriaVD.sql?dl=0 bacteriaVD.sql

cd ../../../inphinity/v_0.3
cp config.example.ini config_v0.3.ini
sudo nano config_v0.3.ini

cd ../../compose/
sudo sh run.sh
docker ps

docker exec -it inphinity-core /bin/bash
