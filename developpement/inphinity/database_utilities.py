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
        self.db=MySQLdb.connect(port=3306, host='database', user='root', db='phage_bact')

    def load_db(self):
        self.write()

    def write(self):
        file = open("/inphinity/out/out_db.txt", "w+")

        file.write("hello world in the new fdddile")

        file.close()