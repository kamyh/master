##
#   Created by: Deruaz Vincent
#   Database tools
#   05.11.2016
##

import MySQLdb

from Logger import Logger

LOGGER = Logger()

class DBUtilties:
    def __init__(self, verbose=False):
        self.verdose = verbose
        self.db=MySQLdb.connect(host='172.25.0.102', user='admin', passwd='root', db='phage_bact')

    def load_db(self):
        self.write()

    ########################
    #   DETECT DOMAINS     #
    ########################
    def count_bacteria(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Bacteria")
        data = cursor.fetchall()
        print(data)

    def get_sequence_proteines_bacteria(self, idCellule):
        cursor = self.db.cursor()
        cursor.execute("SELECT Bacterium_id, GI, Nb_proteins, prot_seq FROM Bacteria WHERE Bacterium_id = " + str(idCellule))
        data = cursor.fetchall()
        return data

    def get_sequence_proteines_phage(self, idCellule):
        cursor = self.db.cursor()
        cursor.execute("SELECT Phage_id, GI, Nb_proteins, prot_seq FROM Phages WHERE Phage_id = " + str(idCellule))
        data = cursor.fetchall()
        return data

    #Inserer domaines d interactions d'une proteines
    def execute_insert_domains(self, id_protein, domaines, id_Cell, bool_Bacteria, seq_prot):

        domaines_no_rep = list(set(domaines))
        for dom in domaines_no_rep:
            if len(dom) >= 5:
                cursor = self.db.cursor()
                cursor.execute("INSERT INTO PROTDOM (ProtId, DomainAcc, Cell_id, Bacteria_Cell, ProtSeq) VALUES ('%s', '%s', %s, %s, '%s')" % (id_protein, dom, int(id_Cell), bool_Bacteria, seq_prot))
                self.db.commit()

        #Verifier si la seq a deja ete recherchee
    def get_proteine_in_prot_dom(self, id_protein):
        cursor = self.db.cursor()
        #TODO: replace all string concat by this technic
        rqt = "SELECT count(*) from PROTDOM WHERE ProtId = '%s'" % (id_protein)
        cursor.execute(rqt)
        data = cursor.fetchall()
        return data[0][0]

    def get_id_all_bacts(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT Bacterium_id FROM Bacteria")
        data = cursor.fetchall()
        bactsIdRet = []
        for resultat in data:
            bactsIdRet.append(resultat[0])

        return bactsIdRet[12:18] #FOR TESTING RUN PURPOSE (TODO: REMOVE)
        return bactsIdRet

    ########################
    #   Auxiliary          #
    ########################
    def show_tables_of_phage_bact(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT" +
                       "(SELECT COUNT(*) FROM Bacteria) as Bacteria,"
                       "(SELECT COUNT(*) FROM Interactions) as Interactions," +
                       "(SELECT COUNT(*) FROM PROTDOM) as PROTDOM," +
                       "(SELECT COUNT(*) FROM Phages) as Phages," +
                       "(SELECT COUNT(*) FROM Negative_Interactions) as Negative_Interactions")
        data = cursor.fetchall()
        print(data)

