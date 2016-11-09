##
#   Created by: Deruaz Vincent
#   Database tools
#   05.11.2016
##

import _mysql

class DBUtilties:
    def __init__(self):
        self.db=_mysql.connect(host="database",port=3306,passwd="SecretPasswordInphinity",db="test")

    def load_db(self):
        self.write()

    def write(self):
        file = open("/inphinity/out/out_db.txt", "w+")

        file.write("hello world in the new fdddile")

        file.close()