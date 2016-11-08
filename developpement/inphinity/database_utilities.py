##
#   Created by: Deruaz Vincent
#   Database tools
#   05.11.2016
##

class DBUtilties:
    def __init__(self):
        pass

    def load_db(self):
        self.write()

    def write(self):
        file = open(r"/tmp/inphinity/out_db.txt", "w+")

        file.write("hello world in the new file")

        file.close()