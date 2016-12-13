##
#   Created by: Deruaz Vincent
#   Database tools
#   05.11.2016
##

import MySQLdb

from Logger import Logger

LOGGER = Logger()

class DBUtilties:
    def __init__(self,configuration , verbose=False):
        self.verdose = verbose
        self.configuration = configuration
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(host='172.25.0.102', user='admin', passwd='root', db='phage_bact')


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
        cursor.execute("SELECT Bacterium_id, GI, Nb_proteins, prot_seq FROM Bacteria WHERE Bacterium_id = %s" % idCellule)
        data = cursor.fetchall()
        return data

    def get_sequence_proteines_phage(self, idCellule):
        cursor = self.db.cursor()
        cursor.execute("SELECT Phage_id, GI, Nb_proteins, prot_seq FROM Phages WHERE Phage_id = %s" % idCellule)
        data = cursor.fetchall()
        return data

    # Inserer domaines d interactions d'une proteines
    # TODO: can we remove ProtSeq column ???
    def execute_insert_domains(self, id_protein, domaines, id_Cell, bool_Bacteria, seq_prot):
        domaines_no_rep = list(set(domaines))
        for dom in domaines_no_rep:
            if len(dom) >= 5:
                cursor = self.db.cursor()
                rqt = "INSERT INTO PROTDOM (ProtId, DomainAcc, Cell_id, Bacteria_Cell, ProtSeq) VALUES ('%s', '%s', %s, %s, '%s')" % (id_protein, dom, int(id_Cell), bool_Bacteria, seq_prot)
                cursor.execute(rqt)
                self.db.commit()

                # Verifier si la seq a deja ete recherchee

    def get_proteine_in_prot_dom(self, id_protein):
        cursor = self.db.cursor()
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

        if self.configuration.is_testing():
            return bactsIdRet[17:18]
        return bactsIdRet

    ################################################
    #   3_F1 countScoreInteraction                 #
    ################################################

    # Obtenir les ID de toutes les interactions
    def get_all_intractions(self):
        list_interaction_pos = []
        list_interaction_neg = []
        list_interactions = []
        list_interaction_pos = self.get_interactions_positives()
        list_interaction_neg = self.get_interactions_negatives()
        list_interactions = list_interaction_pos + list_interaction_neg
        return list_interactions

    # Obtenir les ID de toutes les interactions positives
    def get_interactions_positives(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * from Interactions")
        data = cursor.fetchall()
        return data

    # Obtenir les ID de toutes les interactions negatives
    def get_interactions_negatives(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * from Negative_Interactions")
        data = cursor.fetchall()
        return data

    # Retourne la seq proteique des proteines
    # (1 = Bacteria; 2 = Phage)
    def get_sequence_proteines(self, id_cellule, tipe_cell):
        if tipe_cell == 1:
            query = 'SELECT Bacterium_id, GI, Nb_proteins, prot_seq FROM Bacteria WHERE Bacterium_id = %s' % id_cellule
        else:
            query = 'SELECT Phage_id, GI, Nb_proteins, prot_seq FROM Phages WHERE Phage_id = %s' % id_cellule
        cursor = self.db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    # Obtenir les domaines d une protein d un organisme
    # boolBact 1 - bact 0 - phage
    def get_domains_cell(self, id_prot):
        list_return_doms = []
        list_doms = self.get_domaines_by_id_cell_offline(id_prot)
        for dom in list_doms:
            if len(dom[0]) > 2 and "NA" not in dom[0]:
                list_return_doms.append(dom[0])
        return list_return_doms

    # consulte la db pour obtenir les domains
    # boolbact 1 - bacterie 0 - phage
    def get_domaines_by_id_cell_offline(self, id_prot):

        cursor = self.db.cursor()
        cursor.execute("SELECT DomainAcc FROM PROTDOM WHERE ProtId ='%s'" % id_prot)
        data = cursor.fetchall()
        return data

    # Verifier si le domaine n a pas ete actualiser
    # Si oui retourne le nouveau domaine
    def is_exist_other_domaines(self, domaine):
        try:
            query = "SELECT NewDomain FROM PFAM WHERE DomainAcc='%s'" % domaine
            cursor = self.db.cursor()
            cursor.execute(query)
            new_domaine = cursor.fetchone()
            if "PF" in new_domaine[0]:
                return new_domaine[0]
            return ""
        except:
            return "--"

    # Obtenir le scor d interaction entre deux domaines
    def is_interaction_existe_dom(self, domaine_1, domaine_2):
        query = "SELECT * from INTERACTION WHERE Domain1='%s' and Domain2='%s'" % (domaine_1, domaine_2)
        cursor = self.db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        qtd_registre = data.rowcount
        if qtd_registre == 0:
            query = "SELECT * from INTERACTION WHERE Domain1='%s' and Domain2='%s'" % (domaine_2, domaine_1)
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        qtd_registre = data.rowcount
        if qtd_registre == 1:
            aux = data.fetchone()
            return sum(aux[2:16])
        return -1

    # Inserer le scor de l IPP dans le tableau Score_interactions
    def insert_score_IPP(self, id_prot_bact, id_prot_phage, positiv_interaction, interaction_id, score):
        query = "INSERT INTO Score_interactions (ProtBactId, ProtPhageId, Positiv_Interaction, Interaction_Id, Score_result) VALUES (%s, %s, %s, %s, %s)" % (id_prot_bact, id_prot_phage, positiv_interaction, interactionId, float(score))
        cursor = self.db.cursor()
        cursor.execute(query)

    ################################################
    #   4_F1 FreqQtdScores                         #
    ################################################

    ################################################
    #   5_F1 createGradesDict                      #
    ################################################

    ################################################
    #   6_F1 GenerateDS                            #
    ################################################

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
                       "(SELECT COUNT(*) FROM Negative_Interactions) as Negative_Interactions," +
                       "(SELECT COUNT(*) FROM Score_interactions) as Score_interactions")
        data = cursor.fetchall()
        print('Database State: Bacteria:%s | Interactions:%s | PROTDOM:%s | Phages:%s | Negative_Interactions:%s | Score_interactions:%s' % (data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5]))

    def reset_db(self):
        cursor = self.db.cursor()
        cursor.execute("TRUNCATE TABLE PROTDOM")

    def get_number_of_organismes(self):
        count = 0
        cursor = self.db.cursor()
        cursor.execute("SELECT count(Bacterium_id) FROM Bacteria")
        data = cursor.fetchall()
        count += int(data[0][0])

        cursor = self.db.cursor()
        cursor.execute("SELECT count(Phage_id) FROM Phages")
        data = cursor.fetchall()
        count += int(data[0][0])
        return count
