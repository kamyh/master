#!/bin/bash

#/bin/bash -c "/usr/bin/mysqld_safe &" && \
    #sleep 5 && \
    #mysql -u root -e "CREATE DATABASE phage_bact" && \
    #mysql -u root -e "SHOW DATABASES;" && \

    #echo "phagesVD.sql" && \
    #mysql -u root phage_bact < /tmp/db/phagesVD.sql && \
    #echo "bacteriaVD.sql" && \
    #mysql -u root phage_bact < /tmp/db/bacteriaVD.sql && \
    #echo "interactionsVD.sql" && \
    #mysql -u root phage_bact < /tmp/db/interactionsVD.sql && \
    #echo "neg_interactionsVD.sql" && \
    #mysql -u root phage_bact < /tmp/db/neg_interactionsVD.sql && \
    #echo "Protdom table creation" && \
    #mysql -u root phage_bact < /tmp/protdom_create.sql

if [ ! -f /var/lib/mysql/ibdata1 ]; then

	mysql_install_db

	/usr/bin/mysqld_safe &
	sleep 10s

	echo "GRANT ALL ON *.* TO admin@'%' IDENTIFIED BY 'root' WITH GRANT OPTION; FLUSH PRIVILEGES" | mysql
	echo "CREATE DATABASE phage_bact" | mysql

	killall mysqld
	sleep 10s
fi

/usr/bin/mysqld_safe



#while true; do sleep 2; done