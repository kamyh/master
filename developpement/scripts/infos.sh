#!/usr/bin/env bash

docker exec -it inphinity-database mysql -h inphinity-database -u admin -proot -e "use phage_bact; SELECT (SELECT count(ProtDomId) as doms_found from phage_bact.PROTDOM) as doms_found, (SELECT count(id) as sequences_done from phage_bact.progress) as sequences_done, (SELECT count(Score_Inter_Id) from phage_bact.Score_interactions) as interactions_found, (SELECT count(QS_id) from phage_bact.QtdScores) as QtdScores;"
echo '\n'
docker exec -it inphinity-core tail -5 /tmp/logs_inphinity.txt |grep NORMAL;

