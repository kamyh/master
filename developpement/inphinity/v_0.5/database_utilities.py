##
#   Created by: Deruaz Vincent
#   Database tools
#   05.11.2016
##

import MySQLdb

from Logger import Logger

LOGGER = Logger()


class DBUtilties:
    def __init__(self, configuration, verbose=False):
        self.verdose = verbose
        self.configuration = configuration
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(host='172.25.0.102', user='admin', passwd='root', db='phage_bact')

    def disconnect(self):
        self.db.close()

    ########################
    #   DETECT DOMAINS     #
    ########################
    def count_bacteria(self):
        query = "SELECT COUNT(*) FROM Bacteria"
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            self.count_bacteria()
        print(data)

    def get_sequence_proteines_bacteria(self, id_cellule):
        query = "SELECT Bacterium_id, GI, Nb_proteins, prot_seq FROM Bacteria WHERE Bacterium_id = %s" % id_cellule
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_sequence_proteines_bacteria(id_cellule)
        return data

    def get_sequence_proteines_phage(self, id_cellule):
        query = "SELECT Phage_id, GI, Nb_proteins, prot_seq FROM Phages WHERE Phage_id = %s" % id_cellule
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_sequence_proteines_phage(id_cellule)
        return data

    # Inserer domaines d interactions d'une proteines
    # TODO: can we remove ProtSeq column ???
    def execute_insert_domains(self, id_protein, domaines, id_Cell, bool_Bacteria, seq_prot):
        domaines_no_rep = list(set(domaines))
        for dom in domaines_no_rep:
            if len(dom) >= 5:
                query = "INSERT INTO PROTDOM (ProtId, DomainAcc, Cell_id, Bacteria_Cell, ProtSeq) VALUES ('%s', '%s', %s, %s, '%s')" % (
                    id_protein, dom, int(id_Cell), bool_Bacteria, seq_prot)
                try:
                    cursor = self.db.cursor()
                    cursor.execute(query)
                    self.db.commit()
                except MySQLdb.OperationalError:
                    self.connect()
                    return self.execute_insert_domains(id_protein, domaines, id_Cell, bool_Bacteria, seq_prot)

                    # TODO: Verifier si la seq a deja ete recherchee

    def get_proteine_in_prot_dom(self, id_protein):
        query = "SELECT count(*) from PROTDOM WHERE ProtId = '%s'" % (id_protein)
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_proteine_in_prot_dom(id_protein)
        return data[0][0]

    def get_id_all_bacts(self):
        query = "SELECT Bacterium_id FROM Bacteria"
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_id_all_bacts()
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
        query = "SELECT * from Interactions"
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_interactions_positives()
        return data

    # Obtenir les ID de toutes les interactions negatives
    def get_interactions_negatives(self):
        query = "SELECT * from Negative_Interactions"
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_interactions_negatives()
        return data

    # Retourne la seq proteique des proteines
    # (1 = Bacteria; 2 = Phage)
    def get_sequence_proteines(self, id_cellule, tipe_cell):
        if tipe_cell == 1:
            query = 'SELECT Bacterium_id, GI, Nb_proteins, prot_seq FROM Bacteria WHERE Bacterium_id = %s' % id_cellule
        else:
            query = 'SELECT Phage_id, GI, Nb_proteins, prot_seq FROM Phages WHERE Phage_id = %s' % id_cellule
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_sequence_proteines(id_cellule, tipe_cell)
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
        query = "SELECT DomainAcc FROM PROTDOM WHERE ProtId ='%s'" % id_prot
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_domaines_by_id_cell_offline(id_prot)
        return data

    # Verifier si le domaine n a pas ete actualiser
    # Si oui retourne le nouveau domaine
    def is_exist_other_domaines(self, domaine):
        try:
            query = "SELECT NewDomain FROM PFAM WHERE DomainAcc='%s'" % domaine
            try:
                cursor = self.db.cursor()
                cursor.execute(query)
                new_domaine = cursor.fetchone()
            except MySQLdb.OperationalError:
                self.connect()
                return self.is_exist_other_domaines(domaine)
            if "PF" in new_domaine[0]:
                return new_domaine[0]
            return ""
        except:
            return "--"

    # Obtenir le scor d interaction entre deux domaines
    def is_interaction_existe_dom(self, domaine_1, domaine_2):
        query = "SELECT * from INTERACTION WHERE Domain1='%s' and Domain2='%s'" % (domaine_1, domaine_2)
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.is_interaction_existe_dom(domaine_1, domaine_2)

        qtd_registre = data.rowcount
        if qtd_registre == 0:
            query = "SELECT * from INTERACTION WHERE Domain1='%s' and Domain2='%s'" % (domaine_1, domaine_2)
            try:
                cursor = self.db.cursor()
                cursor.execute(query)
                data = cursor.fetchall()
            except MySQLdb.OperationalError:
                self.connect()
                return self.is_interaction_existe_dom(domaine_1, domaine_2)
        qtd_registre = data.rowcount
        if qtd_registre == 1:
            aux = data.fetchone()
            return sum(aux[2:16])
        return -1

    # Inserer le scor de l IPP dans le tableau Score_interactions
    def insert_score_IPP(self, id_prot_bact, id_prot_phage, positiv_interaction, interaction_id, score):
        query = "INSERT INTO Score_interactions (ProtBactId, ProtPhageId, Positiv_Interaction, Interaction_Id, Score_result) VALUES (%s, %s, %s, %s, %s)" % (
            id_prot_bact, id_prot_phage, positiv_interaction, interaction_id, float(score))

        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            self.insert_score_IPP(id_prot_bact, id_prot_phage, positiv_interaction, interaction_id, score)

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
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT" +
                           "(SELECT COUNT(*) FROM Bacteria) as Bacteria,"
                           "(SELECT COUNT(*) FROM Interactions) as Interactions," +
                           "(SELECT COUNT(*) FROM PROTDOM) as PROTDOM," +
                           "(SELECT COUNT(*) FROM Phages) as Phages," +
                           "(SELECT COUNT(*) FROM Negative_Interactions) as Negative_Interactions," +
                           "(SELECT COUNT(*) FROM Score_interactions) as Score_interactions")
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            self.show_tables_of_phage_bact()
        print(
            'Database State: Bacteria:%s | Interactions:%s | PROTDOM:%s | Phages:%s | Negative_Interactions:%s | Score_interactions:%s' % (
                data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5]))

    def reset_db(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("TRUNCATE TABLE PROTDOM")

        except MySQLdb.OperationalError:
            self.connect()
            self.reset_db()

    def get_number_of_organismes(self):
        count = 0

        query = "SELECT count(Bacterium_id) FROM Bacteria"
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_number_of_organismes()
        count += int(data[0][0])

        query = "SELECT count(Phage_id) FROM Phages"
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.OperationalError:
            self.connect()
            return self.get_number_of_organismes()
        count += int(data[0][0])
        return count
