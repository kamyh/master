#!/bin/bash

/bin/bash -c "/usr/bin/mysqld_safe &" && \
  sleep 5 && \
  mysql -u root -e "CREATE DATABASE phage_bact" && \
  mysql -u root -e "SHOW DATABASES;"

mysql -u root phage_bact < /tmp/db/interactionsVD.sql