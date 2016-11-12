##
#   Created by: Deruaz Vincent
#   Database tools
#   05.11.2016
##

import MySQLdb

class DBUtilties:
    def __init__(self):
        import time
        time.sleep(5)
        self.db=MySQLdb.connect(port=3306, host='localhost', user='inphinity', passwd='SecretPasswordInphinity', db='phage_bact')

    def load_db(self):
        self.write()

    def count(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Bacteria")
        self.db.close()
        data = cursor.fetchall()
        print data

    def write(self):
        file = open("/inphinity/out/out_db.txt", "w+")

        file.write("hello world in the new fdddile")

        file.close()