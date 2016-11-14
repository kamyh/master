##
#   Created by: Deruaz Vincent
#   Database tools
#   05.11.2016
##

import MySQLdb

class DBUtilties:
    def __init__(self):
        pass

    def connection(self):
        self.db=MySQLdb.connect(host='172.25.0.102', user='admin', passwd='root', db='phage_bact')

    def load_db(self):
        self.write()

    def count_bacteria(self):
        self.connection()
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Bacteria")
        self.db.close()
        data = cursor.fetchall()
        print data

    def get_sequence_proteines_bacteria(self, idCellule):
        self.connection()
        cursor = self.db.cursor()
        cursor.execute("SELECT Bacterium_id, GI, Nb_proteins, prot_seq FROM Bacteria WHERE Bacterium_id = " + str(idCellule))
        self.db.close()
        data = cursor.fetchall()
        return data

    def get_sequence_proteines_phage(self, idCellule):
        self.connection()
        cursor = self.db.cursor()
        cursor.execute("SELECT Phage_id, GI, Nb_proteins, prot_seq FROM Phages WHERE Phage_id = " + str(idCellule))
        self.db.close()
        data = cursor.fetchall()
        return data

    def show_tables_of_phage_bact(self):
        self.connection()
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
        self.connection()
        cursor = self.db.cursor()
        cursor.execute("SELECT Bacterium_id FROM Bacteria")
        self.db.close()
        data = cursor.fetchall()
        bactsIdRet = []
        for resultat in data:
            bactsIdRet.append(resultat[0])
        return bactsIdRet

