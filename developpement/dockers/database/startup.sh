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

	# For 1_F1 DetectDomains.py
	echo "CREATE DATABASE phage_bact" | mysql
	mysql phage_bact < /tmp/db/phagesVD.sql
	mysql phage_bact < /tmp/db/bacteriaVD.sql
	mysql phage_bact < /tmp/db/interactionsVD.sql
	mysql phage_bact < /tmp/db/neg_interactionsVD.sql
	mysql phage_bact < /tmp/db/protdom_create.sql
	mysql phage_bact < /tmp/db/progress_create.sql
	mysql phage_bact < /tmp/db/progress_interaction_create.sql

    # For 3_F1 countScoreInteraction.py
	mysql phage_bact < /tmp/db/score_interactions_create.sql

	echo "CREATE DATABASE domine" | mysql
    mysql domine < /tmp/db/domTGo.sql
    mysql domine < /tmp/db/domPfam.sql
    mysql domine < /tmp/db/domPgmap.sql
    mysql domine < /tmp/db/domTInteract.sql

    # For 4_F1 FreqQtdScores.py
	mysql phage_bact < /tmp/db/qtd_scores_create.sql

	killall mysqld
	sleep 10s
fi

/usr/bin/mysqld_safe



#while true; do sleep 2; done