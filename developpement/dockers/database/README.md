# Build

$ docker build -t tm/database .

# Run

$ docker run -d -e MYSQL_ROOT_PASSWORD=passwordInphinity tm/database

# Connect to mysql

$ mysql -u root -ppasswordInphinity