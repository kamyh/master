import MySQLdb

if __name__ == '__main__':
    db=MySQLdb.connect(host='172.25.0.102', user='admin', passwd='root', db='phage_bact')
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")
    db.close()
    data = cursor.fetchall()
    print data