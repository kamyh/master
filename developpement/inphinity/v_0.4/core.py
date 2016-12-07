##
#   Created by: Deruaz Vincent
#   Core of Inphinity
#   23.10.2016
##

from hmmerScan import HmmerScan
from database_utilities import DBUtilties
import sys
from Bio import *
from Bio import SeqIO
from Logger import Logger
import subprocess
from multiprocessing import Pool
from config import Config
import uuid
from toolsIo import ToolsIO
from Bio import *
import multiprocessing

LOGGER = Logger()
DEBUG = True


class DetectDomaines():
    def __init__(self, configuration, db, verdose=False):
        self.configuration = configuration
        self.verdose = verdose
        self.db = db
        self.hmmer_scan = HmmerScan(self.configuration, self.verdose)
        self.list_id_organismes = self.db.get_id_all_bacts()

        # Fichier pour parser les seqs
        self.temp_file_pseqs = self.configuration.get_path_to_core()

    # Parser les sequences multi-fasta
    def parse_sequences_prot(self, sequence):
        pid = []
        pseq = []
        text_file = open(self.configuration.get_temp_file_p_seqs(), "w")
        text_file.write(sequence)
        text_file.close()

        fasta_sequences = SeqIO.parse(open(self.configuration.get_temp_file_p_seqs()), 'fasta')
        for fasta in fasta_sequences:
            pid.append(fasta.id)

            # pseq.append(fasta.seq.tostring()) DEPRECATED (toSting())
            pseq.append(str(fasta.seq))

        return pid, pseq

    def seek_domaines_parallel(self, vec_id, vec_seq, id_cell, bool_bacteria):
        print(zip(vec_id, vec_seq))

        p = Pool(5)
        # domaines_returned = p.map(cmd, zip(vec_id, vec_seq))

    def run(self):
        LOGGER.log_debug('New Run')

        ##GENERATE Fasta
        list_id_organismes = self.db.get_id_all_bacts()

        nbr_organismes = len(list_id_organismes)
        nbr_organismes_analyzed = 0

        for id in list_id_organismes:
            print('%d/%d organismes analysed' % (nbr_organismes_analyzed, nbr_organismes))
            self.analyze_organisme(id)
            nbr_organismes_analyzed += 1

        self.db.show_tables_of_phage_bact()

    def analyze_organisme(self, id):
        print('Organism ID: ' + str(id))
        pidss_bact = []
        pseqss_bact = []
        resultats_organismes = self.db.get_sequence_proteines_bacteria(id)
        pidss_bact, pseqss_bact = self.parse_sequences_prot(resultats_organismes[0][3])

        if (DEBUG):
            pidss_bact = pidss_bact[:10]
            pseqss_bact = pseqss_bact[:10]

        # seek_domaines(pidss_bact, pseqss_bact, id, 0)
        print('%d sequences to compute domaines!' % (len(pidss_bact)))
        self.seek_domaines_multiprocess(zip(pidss_bact, pseqss_bact), id)

    # TODO: check seek_domaines() original fct
    def seek_domaines_multiprocess(self, tab, id_cell):
        bool_bacteria = 0

        print('CPU Count: %s' % multiprocessing.cpu_count())
        pool_size = multiprocessing.cpu_count()
        print('Pool Size: %s' % pool_size)

        h = HmmerScan(self.configuration)

        p = Pool(pool_size)
        results = p.map(h.analyze_domaines, tab)

        print(results)

        for result in results:
            id_prot = result[0]
            domaines_returned = result[1]

            self.db.execute_insert_domains(id_prot, domaines_returned, id_cell, bool_bacteria, "--")


class Core:
    def __init__(self):
        self.configuration = Config('inphinity/v_0.4/config_v0.4.ini')
        self.db = DBUtilties(False)
        #TODO: Declare IO object here too
        self.detect_domaines = DetectDomaines(self.configuration, self.db)

    def phase_1_detect_domains(self):
        self.detect_domaines.run()

    def run(self):
        self.phase_1_detect_domains()
