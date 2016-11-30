# Master Thesis
## Architecture

![Architecture](./documents/img/Inphinity_system_design.png)

## Installations
### Docker

#### Install Docker Engine

```
$ sudo apt-get update
$ sudo apt-get install apt-transport-https ca-certificates
$ sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

$ sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'
$ sudo apt-get update
$ sudo apt-cache policy docker-engine
$ sudo apt-get install -y docker-engine
$ sudo systemctl status docker
```

You now should see:
```
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2016-11-30 01:28:41 CET; 8h ago
     Docs: https://docs.docker.com
 Main PID: 1171 (dockerd)
    Tasks: 41
   Memory: 3.7G
      CPU: 1min 18.316s
   CGroup: /system.slice/docker.service
           ├─ 1171 /usr/bin/dockerd -H fd://
           ├─ 1607 docker-containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --shim docker-con
           └─21678 docker-containerd-shim 1ed0c2cbc7dbd228de8ffd82a822df63abc6f75f3978b96a8b9e82832489a343 /var/run/d


```

Configure Docker for your loggedin user

```
$ sudo usermod -aG docker $(whoami)
```

You now have to reboot your machine.

### Install Docker-compose (1.9)

```
$ curl -L "https://github.com/docker/compose/releases/download/1.9.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
$ docker-compose --version
```

You now should see:
```
docker-compose version: 1.9.0
```



