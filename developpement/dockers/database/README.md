# Build

$ docker build -t tm/database .

# Run

$ docker run -d -e MYSQL_ROOT_PASSWORD=passwordInphinity -p 3306:3306 tm/database

# Connect to mysql

$ docker exec -d tm/database /bin/bash
$ mysql -u root -ppasswordInphinity