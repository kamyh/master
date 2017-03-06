## Execution

```
$ docker exec -it inphinity-core /bin/bash
$ python3 inphinity/v_0.5/app.py
```

### Know issues

#### 1. Error response from daemon: client is newer than server (client API version: 1.24, server API version: 1.22)

This append if your linux system is not a Debian Jessie. This is due to server/client dockers API missmatch.

To fix it run the following command in the "inphinity-core" container:

```
$ export DOCKER_API_VERSION=1.22
```

## Usefull commands

docker exec -it inphinity-database mysql -h phage_bact -u admin -proot -e "SELECT count(ProtDomId) as doms_found from phage_bact.PROTDOM;"

docker exec -it inphinity-database mysql -h phage_bact -u admin -proot -e "SELECT (SELECT count(ProtDomId) as doms_found from phage_bact.PROTDOM) as doms_found, (SELECT count(Score_Inter_Id) as interactions_found from phage_bact.Score_interactions) as interactions_found;"
