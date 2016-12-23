##
#   Created by: Deruaz Vincent
#   Core of Inphinity
#   23.10.2016
##

from hmmerScan import HmmerScan
import sys
from Bio import *
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio import Seq
from Logger import Logger
import subprocess
from multiprocessing import Pool
import uuid
from Bio import *
import multiprocessing
from tools import Tools
from time import gmtime, strftime

LOGGER = Logger()

#################################
#   This class cannot have
#   an object with side effet
#   eg. db_utilities
#################################

"""
Phase 1 - Detect Domaines
"""


class DetectDomaines():
    def __init__(self, tools, verdose=False):
        self.verdose = verdose
        self.tools = tools
        self.hmmer_scan = HmmerScan(self.tools.configuration, self.tools.io, self.tools.db, self.verdose)
        self.list_id_organismes = self.tools.db.get_id_all_bacts()

        # Fichier pour parser les seqs
        # TODO: usefull ????
        self.temp_file_pseqs = self.tools.configuration.get_path_to_core()

    # Parser les sequences multi-fasta
    def parse_sequences_prot(self, sequence):
        pid = []
        pseq = []
        text_file = open(self.tools.configuration.get_temp_file_p_seqs(), "w")
        text_file.write(sequence)
        text_file.close()

        fasta_sequences = SeqIO.parse(open(self.tools.configuration.get_temp_file_p_seqs()), 'fasta')
        for fasta in fasta_sequences:
            pid.append(fasta.id)

            # pseq.append(fasta.seq.tostring()) DEPRECATED (toSting())
            pseq.append(str(fasta.seq))

        return pid, pseq

    def seek_domaines_parallel(self, vec_id, vec_seq, id_cell, bool_bacteria):
        print(zip(vec_id, vec_seq))

        p = Pool(5)
        # domaines_returned = p.map(cmd, zip(vec_id, vec_seq))

    def get_number_of_seq_to_analyze(self):
        list_id_organismes = self.tools.db.get_id_all_phages()
        is_detailed_log = self.tools.configuration.get_detailed_logs()
        total = 0

        nbr_organismes = len(list_id_organismes)
        nbr_organismes_analyzed = 0

        for id in list_id_organismes:
            nbr_organismes_analyzed += 1
            resultats_organismes = self.tools.db.get_sequence_proteines_phage(id)
            pidss_bact, pseqss_bact = self.parse_sequences_prot(resultats_organismes[0][3])
            total += len(pidss_bact)
            LOGGER.log_detailed('%d/%d | Organisme ID: %s - %d sequences to compute' % (nbr_organismes_analyzed, nbr_organismes, id, len(pidss_bact)), is_detailed_log)

        LOGGER.log_detailed('%d sequences to compute for %d organismes' % (total, nbr_organismes), is_detailed_log)

        list_id_organismes = self.tools.db.get_id_all_bacts()
        total = 0

        nbr_organismes = len(list_id_organismes)
        nbr_organismes_analyzed = 0

        for id in list_id_organismes:
            nbr_organismes_analyzed += 1
            resultats_organismes = self.tools.db.get_sequence_proteines_bacteria(id)
            pidss_bact, pseqss_bact = self.parse_sequences_prot(resultats_organismes[0][3])
            total += len(pidss_bact)
            LOGGER.log_detailed('%d/%d | Organisme ID: %s - %d sequences to compute' % (nbr_organismes_analyzed, nbr_organismes, id, len(pidss_bact)), is_detailed_log)

        LOGGER.log_detailed('%d sequences to compute for %d organismes' % (total, nbr_organismes), is_detailed_log)

    def run(self):
        """Phages"""
        list_id_phages = self.tools.db.get_id_all_phages()

        nbr_phages = len(list_id_phages)
        nbr_phages_analyzed = 0

        for id in list_id_phages:
            LOGGER.log_normal('%d/%d phages analysed' % (nbr_phages_analyzed, nbr_phages))
            print('%d/%d phages analysed' % (nbr_phages_analyzed, nbr_phages))
            print('Organism ID: ' + str(id))
            resultats_organismes = self.tools.db.get_sequence_proteines_phage(id)
            self.analyze_organisme(resultats_organismes, id)
            nbr_phages_analyzed += 1

        self.tools.db.show_tables_of_phage_bact()

        """Bacterias"""
        list_id_bacterias = self.tools.db.get_id_all_bacts()

        nbr_bacterias = len(list_id_bacterias)
        nbr_bacterias_analyzed = 0

        for id in list_id_bacterias:
            LOGGER.log_normal('%d/%d bacteria analysed' % (nbr_bacterias_analyzed, nbr_bacterias))
            print('%d/%d bacteria analysed' % (nbr_bacterias_analyzed, nbr_bacterias))
            print('Organism ID: ' + str(id))
            resultats_organismes = self.tools.db.get_sequence_proteines_bacteria(id)
            self.analyze_organisme(resultats_organismes, id)
            nbr_bacterias_analyzed += 1

        self.tools.db.show_tables_of_phage_bact()

    def analyze_organisme(self, resultats_organismes, id):
        pidss_bact = []
        pseqss_bact = []

        pidss_bact, pseqss_bact = self.parse_sequences_prot(resultats_organismes[0][3])

        if self.tools.configuration.is_testing():
            pidss_bact = pidss_bact[:10]
            pseqss_bact = pseqss_bact[:10]

        LOGGER.log_normal('%d sequences to compute domaines!' % (len(pidss_bact)))
        print('%d sequences to compute domaines!' % (len(pidss_bact)))
        self.seek_domaines_multiprocess(zip(pidss_bact, pseqss_bact), id)

    def chunks(self, tab, n):
        return list([tab[x:x + n] for x in range(0, len(tab), n)])

    def seek_domaines_multiprocess(self, tab, id_cell):
        bool_bacteria = 0
        total_processed = 0
        pool_size = multiprocessing.cpu_count()

        print('CPU Count: %s' % multiprocessing.cpu_count())

        if self.tools.configuration.get_nbr_process() == '-1':
            print('Pool Size: %s' % pool_size)
        elif self.tools.configuration.get_nbr_process() != '0':
            pool_size = int(self.tools.configuration.get_nbr_process())
            print('Pool Size: %s' % self.tools.configuration.get_nbr_process())

        if self.tools.configuration.get_nbr_process() == '0':
            p = Pool()
        else:
            p = Pool(pool_size)

        chunk_size = pool_size * self.tools.configuration.get_chunk_size_multiplier()
        chunks = self.chunks(list(tab), chunk_size)

        for chunk in chunks:
            print('%d sequences processed!' % total_processed)
            LOGGER.log_normal('%d sequences processed!' % total_processed)
            total_processed += chunk_size
            results = p.map(self.hmmer_scan.analyze_domaines, chunk)
            print(results)

            for result in results:
                try:
                    id_prot = result[0]
                    domaines_returned = result[1]

                    self.tools.db.execute_insert_domains(id_prot, domaines_returned, id_cell, bool_bacteria, "--")
                except TypeError:
                    pass
                    # TODO: TypeError come from no results ?
                    # print('TypeError')


"""
Phase 2 - Count Score Interaction
"""


class CountScoreInteraction():
    def __init__(self, tools):
        self.tools = tools
        self.fectch_list_interaction()

        # Fichier pour parser les seqs
        self.temp_file_pseqs = self.tools.configuration.get_temp_file_p_seqs()

    def run(self):

        # TODO: parallel ???
        LOGGER.log_normal("%d" % (len(self.list_nteractions)))
        for interaction in self.list_nteractions:
            lis_domains_bac = []
            lisDomainsPhage = []

            id_interaction = interaction[0]
            id_bacteria = interaction[1]
            id_phage = interaction[2]
            pos_neg_interaction = interaction[3]
            # print("Treatment of || id_interaction: %s, id_bacteria: %s, id_phage: %s" % (id_interaction, id_bacteria, id_phage))

            ids_seq_bact = self.get_ids_seq_prot(id_bacteria, 1)
            ids_seq_phage = self.get_ids_seq_prot(id_phage, 2)

            LOGGER.log_normal("interaction: id_interaction-%s, id_bacteria-%s, id_phage-%s, pos_neg_interaction-%s" % (id_interaction, id_bacteria, id_phage, pos_neg_interaction))

            for id_seq_bact in ids_seq_bact:
                lis_domains_bac = self.tools.db.get_domains_cell(id_seq_bact)

                if len(lis_domains_bac) > 0:
                    for id_seq_phage in ids_seq_phage:
                        lis_domains_phage = self.tools.db.get_domains_cell(id_seq_phage)
                        # print('%s - %s' % (len(lis_domains_phage), id_seq_phage))
                        if len(lis_domains_phage) > 0:
                            score_PPI = self.get_scores_domaines(lis_domains_bac, lis_domains_phage)

                            if score_PPI > 0:
                                LOGGER.log_normal("score_PPI: %s" % (score_PPI))

                                self.tools.db.insert_score_IPP(id_seq_bact, id_seq_phage, pos_neg_interaction, id_interaction, score_PPI)

    def fectch_list_interaction(self):
        self.list_nteractions = self.tools.db.get_all_intractions()

    # Retourne les ids de proteines d un organism
    # 1 - bacterie 2 - phage
    # Les domaines ons en relation avec l id de la protein de chaque organisme
    def get_ids_seq_prot(self, id_cell, type_of_cell):
        sequence = self.tools.db.get_sequence_proteines(id_cell, type_of_cell)
        ids_seq = self.parse_sequences_prot(sequence[0][3])
        return ids_seq

    # Parser les sequences multi-fasta
    def parse_sequences_prot(self, sequence):
        pid = []

        text_file = open(self.temp_file_pseqs, "w")
        text_file.write(sequence)
        text_file.close()

        fasta_sequences = SeqIO.parse(open(self.temp_file_pseqs), 'fasta')
        for fasta in fasta_sequences:
            pid.append(fasta.id)
        return pid

    # TODO: KEEP like that ? or file tmp ?
    def parse_sequences_prot_from_string(self, sequence):
        pid = []

        fasta_sequences = sequence.split('\n>')
        print(len(fasta_sequences))

        for fasta in fasta_sequences:
            if '\t' in fasta.split(' ')[0]:
                if '>' in fasta.split('\t')[0][1]:
                    pid.append(fasta.split('\t')[0][1:])
                    print('---> %s' % fasta.split('\t')[0][1:])
                else:
                    pid.append(fasta.split('\t')[0])
                    print('---> %s' % fasta.split('\t')[0])
            else:
                pid.append(fasta.split(' ')[0])
                print('---> %s' % fasta.split(' ')[0])
        return pid

    # Calcul le score d interaction entre toutes les paire de proteines
    # pour chaque IPP entre deux organisme va calculer le score et le retourner
    def get_scores_domaines(self, vec_dom_bac, vec_dom_pha):
        score_dom = 0

        for dom_bac in vec_dom_bac:
            new_dom_bact = self.tools.db.is_exist_other_domaines(dom_bac)

            for dom_phag in vec_dom_pha:
                # voir si pour ce domaine il en exist un actualise
                new_dom_phag = self.tools.db.is_exist_other_domaines(dom_phag)
                score_intermediate = 0
                score_intermediate_b = 0
                score_intermediate_c = 0
                score_intermediate_d = 0
                qtd_new_interact = 0.0
                # pas de new domains
                if "PF" not in new_dom_bact and "PF" not in new_dom_phag:
                    score_intermediate = self.tools.db.is_interaction_existe_dom(dom_bac, dom_phag)
                    if score_intermediate > 0:
                        qtd_new_interact = 1.0
                # new domaine only for bacteria
                if "PF" in new_dom_bact and "PF" not in new_dom_phag:
                    score_intermediate = self.tools.db.is_interaction_existe_dom(dom_bac, dom_phag)
                    score_intermediate_b = self.tools.db.is_interaction_existe_dom(new_dom_bact, dom_phag)
                    if score_intermediate > 0:
                        qtd_new_interact = 1.0
                    if score_intermediate_b > 0:
                        qtd_new_interact = qtd_new_interact + 1.0
                # new domaine only for Phages
                if "PF" not in new_dom_bact and "PF" in new_dom_phag:
                    score_intermediate = self.tools.db.is_interaction_existe_dom(dom_bac, dom_phag)
                    score_intermediate_b = self.tools.db.is_interaction_existe_dom(new_dom_bact, new_dom_phag)
                    if score_intermediate > 0:
                        qtd_new_interact = 1.0
                    if score_intermediate_b > 0:
                        qtd_new_interact = qtd_new_interact + 1.0
                # new domaine for both
                if "PF" not in new_dom_bact and "PF" in new_dom_phag:
                    score_intermediate = self.tools.db.is_interaction_existe_dom(dom_bac, dom_phag)
                    score_intermediate_b = self.tools.db.is_interaction_existe_dom(new_dom_bact, dom_phag)
                    score_intermediate_c = self.tools.db.is_interaction_existe_dom(dom_bac, new_dom_phag)
                    score_intermediate_d = self.tools.db.is_interaction_existe_dom(new_dom_bact, new_dom_phag)
                    if score_intermediate > 0:
                        qtd_new_interact = 1.0
                    if score_intermediate_b > 0:
                        qtd_new_interact = qtd_new_interact + 1.0
                    if score_intermediate_c > 0:
                        qtd_new_interact = qtd_new_interact + 1.0
                    if score_intermediate_d > 0:
                        qtd_new_interact = qtd_new_interact + 1.0

                if qtd_new_interact > 0:
                    # print "QTDINteraction: " + str(qtdNewInteract)
                    score_dom = score_dom + ((score_intermediate + score_intermediate_b + score_intermediate_c + score_intermediate_d) / qtd_new_interact)
        return score_dom


"""
Phase 3 - Freq Qtd Scores
"""


class FreqQtdScores():
    def __init__(self, tools):
        self.tools = tools
        self.ids_bact = self.tools.db.get_id_all_bacts()
        self.ids_phages = self.tools.db.get_id_all_phages()
        self.bact_qtd_prots = {}
        self.phage_qtd_prots = {}

    def run(self):
        # TODO: Parallel ?
        for id_bact in self.ids_bact:
            resultats_bact = self.tools.db.get_sequence_proteines_bacteria(id_bact)
            size = self.get_number_proteins(resultats_bact[0][3])
            self.bact_qtd_prots[(int(id_bact))] = size
            # print("QTD Prot Bact: %s" % (size))

        for id_phage in self.ids_phages:
            resultats_phage = self.tools.db.get_sequence_proteines_phage(id_phage)
            size = self.get_number_proteins(resultats_phage[0][3])
            self.phage_qtd_prots[(int(id_phage))] = size
            # print("%d : QTD Prot Phage: %d" % (id_phage,size))

    def get_number_proteins(self, sequence):
        fasta_sequences = sequence.split('>')[1:]

        qtdProts = sum(1 for x in fasta_sequences)
        return qtdProts


"""
Phase 4 - Create Grades Dict
"""


class CreateGradesDict():
    def __init__(self, tools):
        self.tools = tools

    def run(self):
        pass


"""
Phase 5 - Generate DS
"""


class GenerateDS():
    def __init__(self, tools):
        self.tools = tools

    def run(self):
        pass


class Core:
    def __init__(self):
        self.tools = Tools('inphinity/v_0.5/config.ini')
        self.detect_domaines = DetectDomaines(self.tools)
        self.count_score_interaction = CountScoreInteraction(self.tools)
        self.freq_qtd_scores = FreqQtdScores(self.tools)
        self.create_grades_dict = CreateGradesDict(self.tools)
        self.generate_ds = GenerateDS(self.tools)

    def phase_1_detect_domains(self):
        # Only for developpement purpose!
        self.detect_domaines.get_number_of_seq_to_analyze()
        self.detect_domaines.run()

    def phase_2_count_score_interaction(self):
        self.count_score_interaction.run()

    def phase_3_freq_qtd_scores(self):
        self.freq_qtd_scores.run()

    def phase_4_create_grades_dict(self):
        self.create_grades_dict.run()

    def phase_5_generate_ds(self):
        self.generate_ds.run()

    def run(self):
        start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        LOGGER.log_normal('New run at: %s' % start_time)

        if self.tools.configuration.is_reset_db_at_start():
            print('Rest DB starting...')
            self.tools.db.reset_db()
            self.tools.db.show_tables_of_phage_bact()
            print('Rest DB done')

        self.phase_1_detect_domains()
        self.phase_2_count_score_interaction()
        self.phase_3_freq_qtd_scores()

        end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        print("Starting:%s | Ending:%s" % (start_time, end_time))
