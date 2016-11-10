import MySQLdb

if __name__ == '__main__':
    db=MySQLdb.connect(port=3306, host='database', user='root', db='phage_bact')