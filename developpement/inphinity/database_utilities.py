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
        self.db=MySQLdb.connect(host='172.25.0.102', user='admin', passwd='root', db='phage_bact')

    def load_db(self):
        self.write()

    def count_bacteria(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Bacteria")
        self.db.close()
        data = cursor.fetchall()
        print data

    def show_tables_of_phage_bact(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT" +
                       "(SELECT COUNT(*) FROM Bacteria) as Bacteria,"
                       "(SELECT COUNT(*) FROM Interactions) as Interactions," +
                       "(SELECT COUNT(*) FROM PROTDOM) as PROTDOM," +
                       "(SELECT COUNT(*) FROM Phages) as Phages," +
                       "(SELECT COUNT(*) FROM Negative_Interactions) as Negative_Interactions")
        self.db.close()
        data = cursor.fetchall()
        print data

    def get_id_all_bacts(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT Bacterium_id FROM Bacteria")
        self.db.close()
        data = cursor.fetchall()
        bactsIdRet = []
        for resultat in data:
            bactsIdRet.append(resultat[0])
        return bactsIdRet

