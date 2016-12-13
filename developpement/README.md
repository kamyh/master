## Process

1. core code
    - supervision by host ???
    - supervision by a container ???
2. start docker hmmer --> run hmmscan
3. 


docker exec -it inphinity-database mysql -h phage_bact -u admin -proot -e "SELECT count(ProtDomId) as doms_found from phage_bact.PROTDOM;"

docker exec -it inphinity-database mysql -h phage_bact -u admin -proot -e "SELECT (SELECT count(ProtDomId) as doms_found from phage_bact.PROTDOM) as doms_found, (SELECT count(Score_Inter_Id) as interactions_found from phage_bact.Score_interactions) as interactions_found;"