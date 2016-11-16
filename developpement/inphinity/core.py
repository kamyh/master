##
#   Created by: Deruaz Vincent
#   Core of Inphinity
#   23.10.2016
##

from hmmerScan import HmmerScan
from config import Config
from database_utilities import DBUtilties
import sys
from Bio import *
from Bio import SeqIO


class DetectDomaines():
    def __init__(self, verdose=False):
        self.verdose = verdose
        self.db = DBUtilties(self.verdose)
        self.hmmer_scan = HmmerScan(self.verdose)
        self.configuration = Config('inphinity/default.ini')
        self.list_id_organismes = self.db.get_id_all_bacts()


        #Fichier pour parser les seqs
        self.temp_file_pseqs = self.configuration.get_path_to_core()

    #Parser les sequences multi-fasta
    def parse_sequences_prot(self, sequence):
        pid = []
        pseq = []
        text_file = open(self.configuration.get_temp_file_p_seqs(), "w")
        text_file.write(sequence)
        text_file.close()

        fasta_sequences = SeqIO.parse(open(self.configuration.get_temp_file_p_seqs()),'fasta')
        for fasta in fasta_sequences:
            pid.append(fasta.id)
            pseq.append(fasta.seq.tostring())
            #new_sequence = some_function(sequence)
            #write_fasta(out_file)

        return pid, pseq

    #Recherche des domaines pour chaque Prot
    def seek_domaines(self, vec_id, vec_seq, id_cell, bool_bacteria):
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

        for id_prot, seq_prot in zip(vec_id, vec_seq):
            try:
                vec_domaines = []
                protein_exist = self.db.get_proteine_in_prot_dom(id_prot)
                print("protein_exist: %s" % protein_exist)
                if protein_exist == 0:
                    print("insert")
                    domaines_returned = self.hmmer_scan.detecter_PFAM(id_prot, seq_prot)
                    if(self.verdose):
                        print(domaines_returned)
                    self.db.execute_insert_domains(id_prot, domaines_returned, id_cell, bool_bacteria, "--")
                else:
                    print("exists")
            except:
                vec_domaines = ['--PN--']
                #executeInsertDomains(id_prot, vec_domaines, id_cell, bool_bacteria, seq_prot)

    def run(self):
        for id in self.list_id_organismes:
            print('Organism ID: ' + str(id))
            pidss_bact = []
            pseqss_bact = []

            resultats_organismes = self.db.get_sequence_proteines_bacteria(id)

            pidss_bact, pseqss_bact = self.parse_sequences_prot(resultats_organismes[0][3])

            if(self.verdose):
                print(pidss_bact)
                print(pseqss_bact)
            self.seek_domaines(pidss_bact, pseqss_bact, id, 0)

        self.db.show_tables_of_phage_bact()


class Core:
    def __init__(self):
        self.configuration = Config()

    def phase_1(self):
        self.detect_domaines = DetectDomaines()
