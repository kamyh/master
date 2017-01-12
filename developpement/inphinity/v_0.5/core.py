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
import pickle
import numpy as np
import csv
import time
import datetime

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
        if self.tools.configuration.do_phage():
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

        if self.tools.configuration.do_bacteria():
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
        pool_size = multiprocessing.cpu_count() - 1

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

            for prot in chunk:
                self.tools.db.analyze_done(prot[0], 1)

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
        LOGGER.log_normal("Number of interactions: %d" % (len(self.list_interactions)))
        for interaction in self.list_interactions:
            if not self.tools.db.interaction_has_been_done(interaction[0]):
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
                    # print(lis_domains_bac)

                    if len(lis_domains_bac) > 0:
                        for id_seq_phage in ids_seq_phage:

                            lis_domains_phage = self.tools.db.get_domains_cell(id_seq_phage)
                            # print(lis_domains_phage)
                            # print('%s - %s' % (len(lis_domains_phage), id_seq_phage))
                            if len(lis_domains_phage) > 0:
                                score_PPI = self.get_scores_domaines(lis_domains_bac, lis_domains_phage)

                                if score_PPI > 0:
                                    # LOGGER.log_normal("score_PPI: %s" % (score_PPI))

                                    self.tools.db.insert_score_IPP(id_seq_bact, id_seq_phage, pos_neg_interaction, id_interaction, score_PPI)

                self.tools.db.interaction_analyze_done(interaction[0], 1)

    def fectch_list_interaction(self):
        self.list_interactions = self.tools.db.get_all_intractions()

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
            # print(dom_bac)

            for dom_phag in vec_dom_pha:
                # voir si pour ce domaine il en exist un actualise
                new_dom_phag = self.tools.db.is_exist_other_domaines(dom_phag)
                score_intermediate = 0
                score_intermediate_b = 0
                score_intermediate_c = 0
                score_intermediate_d = 0
                qtd_new_interact = 0.0

                '''
                if dom_bac == 'PF00270':
                    print("dom_bac: %s | dom_phag: %s" % (dom_bac,dom_phag))

                if dom_bac == 'PF00270' and dom_phag == 'PF00271':
                    print("-dom_bac: %s | dom_phag: %s" % (dom_bac,dom_phag))
                    score_intermediate = self.tools.db.is_interaction_existe_dom(dom_bac, dom_phag)
                    print(score_intermediate)

                if dom_bac == 'PF00271' and dom_phag == 'PF00270':
                    print("dom_bac: %s | dom_phag: %s" % (dom_bac,dom_phag))
                '''
                # pas de new domains
                if "PF" not in new_dom_bact and "PF" not in new_dom_phag:
                    # print("dom_bac: %s | dom_phag: %s" % (dom_bac,dom_phag))
                    score_intermediate = self.tools.db.is_interaction_existe_dom(dom_bac, dom_phag)
                    # print("score_intermediate: %s" % (score_intermediate))
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
                    # print("QTDINteraction: %d" % (qtd_new_interact))
                    score_dom = score_dom + ((score_intermediate + score_intermediate_b + score_intermediate_c + score_intermediate_d) / qtd_new_interact)
        return score_dom


"""
Phase 3 - Freq Qtd Scores
"""


class FreqQtdScores():
    def __init__(self, tools):
        self.tools = tools
        self.list_interact = self.tools.db.get_all_intractions()
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

        # TODO: Parallel ?
        for id_phage in self.ids_phages:
            resultats_phage = self.tools.db.get_sequence_proteines_phage(id_phage)
            size = self.get_number_proteins(resultats_phage[0][3])
            self.phage_qtd_prots[(int(id_phage))] = size
            # print("%d : QTD Prot Phage: %d" % (id_phage,size))

        self.scoring()

    def scoring(self):
        sum_qtd = 0
        qtd_of_zeros = 0
        for interact in self.list_interact:
            sum_qtd = 0
            qtd_of_zeros = 0

            id_interaction = interact[0]
            id_bacteria = interact[1]
            id_phage = interact[2]
            type_class = interact[3]

            LOGGER.log_normal("Scoring of interaction (id): %s" % id_interaction)

            all_scores = self.get_all_scores_by_id_inter_class(id_interaction, type_class)
            for Score in all_scores:
                qtd_scors = self.tools.db.get_qtd_scores(id_interaction, type_class, Score)
                self.tools.db.insert_qtds_scores(id_interaction, type_class, Score, qtd_scors)
                sum_qtd = sum_qtd + qtd_scors
            # Le nombre de fois qu apparait 0 est equivalant au nombre d IPP moin la freq des autres scores
            qtd_of_zeros = (self.bact_qtd_prots[(int(id_bacteria))] * self.phage_qtd_prots[(int(id_phage))]) - sum_qtd
            self.tools.db.insert_qtds_scores(id_interaction, type_class, 0, qtd_of_zeros)

    def get_number_proteins(self, sequence):
        fasta_sequences = sequence.split('>')[1:]

        qtd_prots = sum(1 for x in fasta_sequences)
        return qtd_prots

    def get_all_scores_by_id_inter_class(self, id_interaction, positiv_class):
        aux = self.tools.db.get_results_by_int_class_db(id_interaction, positiv_class)
        results = []
        for rst in aux:
            results.append(rst[0])
        return results


"""
Phase 4 - Create Grades Dict
"""


class CreateGradesDict():
    def __init__(self, tools):
        self.tools = tools
        self.vec_id, self.vec_cla, self.vec_scor, self.vec_qtd = self.get_infos_in_vectors()
        self.grades_file_pseqs = self.tools.configuration.get_grades_file_pseqs()

    def run(self):
        LOGGER.log_normal("Create Grades Dict")
        f = open(self.grades_file_pseqs, 'wb')  # Pickle file is newly created where foo1.py is
        # TODO: test with python3
        pickle.dump([self.vec_id, self.vec_cla, self.vec_scor, self.vec_qtd], f)  # dump data to f
        f.close()

    # retourne 4 vecteurs contenant id classe score et frequence
    def get_infos_in_vectors(self):
        infos = self.tools.db.get_all_infos_scores()
        vec_id_inter = []
        vec_class_inter = []
        vec_score_inter = []
        vec_qtd_score_inter = []
        for info in infos:
            # print "Information: " + str(info[0])
            vec_id_inter.append(int(info[1]))
            vec_class_inter.append(int(info[2]))
            vec_score_inter.append(int(info[3]))
            vec_qtd_score_inter.append(int(info[4]))
        return vec_id_inter, vec_class_inter, vec_score_inter, vec_qtd_score_inter


"""
Phase 5 - Generate DS
"""


class GenerateDS():
    def __init__(self, tools):
        self.tools = tools
        self.max_score = -1
        self.max_score_norm = -1

        self.vec_ids_ds = []
        self.vec_type_class = []
        self.vec_qtd_proteins = []
        self.vec_result_final = []
        self.vec_result_normal = []

        self.vec_qtd_scores_histo_results = []
        self.vec_seq_histo_results = []

        self.aux = 0
        # vec avec id des bins qui est utilise pour la premiere ligne des datasets
        self.aux_vec = []

        # TODO: ask diogo if it's the right file
        self.path_file_pickle = self.tools.configuration.get_grades_file_pseqs()
        # TODO: ask diogo wich extension file
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        self.path_file_save = "%s%s_%s.ds" % (self.tools.configuration.get_ds_dir(),self.tools.path_to_config.split('.')[0],st)

    def run(self):
        f = open(self.path_file_pickle, 'rb')
        self.vec_id, self.vec_cla, self.vec_score, self.vec_qtd = pickle.load(f)
        f.close()

        self.max_score = max(self.vec_score)

        type_data_set = self.tools.configuration.normalisation()
        if type_data_set == 1:
            # normaliser les donnes en accord avec le nombre d'IPP
            self.max_score_norm, self.min_score = self.get_max_score_normalized()

        self.bins_config, self.type_config = self.get_user_config_binds(self.max_score, self.max_score_norm, type_data_set)

        # creer les bins et retourne l intervalle de chacun d eux et les frequence
        vec_qtd_scores_histo_results, vec_seq_histo_results = self.create_vec_n_bins(type_data_set)

        # vec avec qtd interaction
        self.qtd_interactions_all = self.create_vec_size(vec_qtd_scores_histo_results)

        # num de bins
        vec_num_bins = len(vec_qtd_scores_histo_results[0])

        while (self.aux < vec_num_bins):
            self.aux_vec.append(self.aux)
            self.aux = self.aux + 1

        # Ecrire le dataset
        self.write_file_ds(vec_qtd_scores_histo_results, self.aux_vec, self.vec_ids_ds, self.vec_type_class, self.path_file_save, 0)

    # normaliser les scores
    def get_max_score_normalized(self):
        inter_id_preced = self.vec_id[0]
        max_score = 0.00000000001
        min_final_score = 1.0
        qtd_score_tot = 0
        position = 0
        vec_aux_scores = []

        for id_inter in self.vec_id:
            if inter_id_preced != id_inter:
                print(qtd_score_tot)
                for score in vec_aux_scores:
                    score_normal = score / qtd_score_tot

                    if score_normal < min_final_score and score_normal != 0.0:
                        min_final_score = score_normal
                    if score_normal > max_score:
                        max_score = score_normal
                vec_aux_scores = []
                qtd_score_tot = 0
                inter_id_preced = id_inter

            qtd_score_tot = qtd_score_tot + self.vec_qtd[position]

            vec_aux_scores.append(self.vec_score[position])

            position = position + 1
        return max_score, min_final_score

    # TODO: How to put those input into config file ????
    # demander a l utilisateur les configurations des bins
    def get_user_config_binds(self, max_score_doms, max_score_norm_doms, type_data_set):
        type_bins = self.tools.configuration.get_type_bins()

        if (type_bins == 1):
            number_of_bins = self.tools.configuration.get_number_of_bins()

            if (number_of_bins < 0 and number_of_bins > max_score_doms):
                LOGGER.log_error("Number of bins to high, set at maximum automatically!")
                number_of_bins = max_score_doms
            return number_of_bins, 1
        if (type_bins == 2):
            aux = 1
            max_value_autoriz = 0
            aux_min_score = 0

            if type_data_set == 0:
                aux_min_score = 0
                max_value_autoriz = max_score_doms
                x = self.tools.configuration.get_space_between_bins()
            else:
                # aux_min_score = maxScoreNormDoms/100
                max_value_autoriz = max_score_norm_doms

                # valueMinScore = format(aux_min_score, '.15f')
                value_max_score = format(max_score_norm_doms, '.15f')
                #x = float(input("Space Between bins ( >0.0 [Min. founded: " + str(self.min_score) + " ] - " + str(value_max_score) + " ) :"))
                x = self.tools.configuration.get_space_between_bins()
                aux_min_score = 0

            if (x < aux_min_score and x > max_value_autoriz):
                LOGGER.log_error("Number of bins to high, set at maximum automatically!")
                x = max_value_autoriz

            if type_data_set == 1:
                max_score_doms = max_score_norm_doms
            vec_bins = []
            while (aux < max_score_doms):
                vec_bins.append(aux)
                aux = aux + x
            if aux >= max_score_doms:
                vec_bins.append(max_score_doms)

            return vec_bins, 2

    # creation de vecteurs
    def create_vec_n_bins(self, bool_normalize_data_set):
        qtd_scores_histo = []
        sep_histo = []
        vecnormal_values = []
        vec_qtd_scores_histo = []
        vec_seq_histo = []
        inter_id_preced = self.vec_id[0]
        vec_results_prov = []
        position = 0

        for id_inter in self.vec_id:

            if inter_id_preced != id_inter:
                LOGGER.log_detailed("Interaction Proceed (id): %d" % (inter_id_preced), self.tools.configuration.get_detailed_logs())

                self.vec_ids_ds.append(inter_id_preced)
                self.vec_type_class.append(self.vec_cla[position])
                inter_id_preced = id_inter

                if bool_normalize_data_set == True:
                    qtd_values = len(vec_results_prov)
                    qtd_values = qtd_values + 0.0
                    for value_inter in vec_results_prov:
                        aux_score = value_inter / qtd_values
                        vecnormal_values.append(aux_score)
                    qtd_scores_histo, sep_histo = np.histogram(vecnormal_values, bins=self.bins_config)
                else:
                    qtd_scores_histo, sep_histo = np.histogram(vec_results_prov, bins=self.bins_config)
                vec_qtd_scores_histo.append(qtd_scores_histo)
                vec_seq_histo.append(sep_histo)
                # print qtd_scores_histo
                # print sep_histo
                vec_results_prov = []
                vecnormal_values = []
            qtd_scores = self.vec_qtd[position]
            aux = 0
            while aux < qtd_scores:
                vec_results_prov.append(self.vec_score[position])
                aux = aux + 1
            position = position + 1
        # a l epoque j ai eu des problemes avec la derniere ligne et j ai pas trop perdu de temps avec
        # le probleme se trouve dans le premier cycle for dans les conditions IF

        position = position - 1
        self.vec_ids_ds.append(inter_id_preced)
        self.vec_type_class.append(self.vec_cla[position])

        if bool_normalize_data_set == True:
            qtd_values = len(vec_results_prov)
            qtd_values = qtd_values + 0.0
            for value_inter in vec_results_prov:
                aux_score = value_inter / qtd_values
                vecnormal_values.append(aux_score)
            qtd_scores_histo, sep_histo = np.histogram(vecnormal_values, bins=self.bins_config)
        else:
            qtd_scores_histo, sep_histo = np.histogram(vec_results_prov, bins=self.bins_config)
            vec_qtd_scores_histo.append(qtd_scores_histo)
            vec_seq_histo.append(sep_histo)

        return vec_qtd_scores_histo, vec_seq_histo

    # retourne un vec avec qtd interactions
    def create_vec_size(self, mat_values):
        qtd_interactions = []
        for nm_interactions in mat_values:
            qtd_interactions.append(sum(nm_interactions))
        return qtd_interactions

    # Ecrire le fichier
    def write_file_ds(self, n, bins_list, vec_id, vec_cla, path_file, bool_normalize):
        LOGGER.log_normal("Writting Dataset: %s" % path_file)
        position = 0
        bins_list_r = [round(i, 5) for i in bins_list]

        if bool_normalize == 1:
            bins_list_r = [format(i, '.8f') for i in bins_list_r]

        bins_list_r.insert(0, "ID_interaction")
        bins_list_r.append("Class_interactions")

        with open(path_file, 'w') as out_csv:
            writer = csv.writer(out_csv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow(bins_list_r)
            for id_interact, type_class, list_histo in zip(vec_id, vec_cla, n):
                list_aux = list_histo.tolist()
                list_aux.append(type_class)
                list_aux.insert(0, id_interact)

                list_aux_b = self.control_number_interactions_only_one(list_aux, position)
                writer.writerow(list_aux_b)
                position = position + 1

    # Controle que la freq de tout les scores est egale a la qtd d IPP
    def control_number_interactions_only_one(self, vec_list_qtd_inter, position):
        qtd_interaction_int = []
        only_zeros = 0
        for i in vec_list_qtd_inter:
            qtd_interaction_int.append(int(i))
            if i == self.qtd_interactions_all[position]:
                only_zeros = 1
        if only_zeros == 1 and self.type_config == 1:
            qtd_interaction_int = [0] * (len(vec_list_qtd_inter) - 3)
            qtd_interaction_int.insert(0, vec_list_qtd_inter[0])
            aux_size = len(vec_list_qtd_inter) - 1
            qtd_interaction_int.insert(1, self.qtd_interactions_all[position])
            qtd_interaction_int.append(vec_list_qtd_inter[aux_size])
        return qtd_interaction_int


class Core:
    def __init__(self, config_file):
        self.tools = Tools(config_file)
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
        LOGGER.log_normal('Config file: %s' % self.tools.path_to_config)

        if self.tools.configuration.is_reset_db_at_start():
            print('Rest DB starting...')
            self.tools.db.reset_db()
            self.tools.db.show_tables_of_phage_bact()
            print('Rest DB done')

        phases_to_run = self.tools.configuration.get_phases_to_run()

        if '1' in phases_to_run:
            LOGGER.log_normal('Run phase 1')
            self.phase_1_detect_domains()
        if '2' in phases_to_run:
            LOGGER.log_normal('Run phase 2')
            self.phase_2_count_score_interaction()
        if '3' in phases_to_run:
            LOGGER.log_normal('Run phase 3')
            self.phase_3_freq_qtd_scores()
        if '4' in phases_to_run:
            LOGGER.log_normal('Run phase 4')
            self.phase_4_create_grades_dict()
        if '5' in phases_to_run:
            LOGGER.log_normal('Run phase 5')
            self.phase_5_generate_ds()

        end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        LOGGER.log_normal("Starting:%s | Ending:%s" % (start_time, end_time))
