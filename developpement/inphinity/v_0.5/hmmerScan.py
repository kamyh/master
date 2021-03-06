##
#   Created by: Deruaz Vincent
#   wrapper of hmmer scan calls from a docker container
#   03.10.2016
##

import subprocess
import sys
from toolsIo import ToolsIO
import uuid
from Logger import Logger
from config import Config
from time import gmtime, strftime
import MySQLdb

LOGGER = Logger()


class HmmerScan:
    def __init__(self, configuration, io, db, verbose=False):
        self.io = io
        self.configuration = configuration
        self.verdose = verbose

    ##
    #   Display the output of 'docker ps' command
    ##
    def docker_ps(self):
        p = Popen(["docker", "ps"])
        output = p.communicate()[0]
        print(output)

    ##
    #   Display the output of 'ls' command
    ##
    def ls(self):
        p = Popen(["ls"])
        output = p.communicate()[0]
        print(output)

    ##
    # beacuase of side-effect limitation due to multiprocess
    # we cannot use database_utilities classe
    # TODO: solve ?
    ##
    def get_proteine_in_prot_dom(self, id_protein):
        db = MySQLdb.connect(host='172.25.0.102', user='admin', passwd='root', db='phage_bact')
        cursor = db.cursor()
        rqt = "SELECT count(*) from PROTDOM WHERE ProtId = '%s'" % (id_protein)
        cursor.execute(rqt)
        data = cursor.fetchall()

        db.close()
        return data[0][0]

    def has_been_done(self, prot_id):
        db = MySQLdb.connect(host='172.25.0.102', user='admin', passwd='root', db='phage_bact')
        cursor = db.cursor()
        query = "SELECT count(*) from progress WHERE prot_id = '%s'" % (prot_id)
        cursor.execute(query)
        data = cursor.fetchall()

        db.close()
        return data[0][0] > 0

    ##
    #   Use <<inphinity-hmmer>> docker container
    #   to analyze domain in protein sequences
    ##
    def analyze_domaines(self, values_tab):
        proteinExist = 0
        proteinExist = self.has_been_done(values_tab[0]) or self.get_proteine_in_prot_dom(values_tab[0])

        if proteinExist == 0:
            start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            path_to_core = self.configuration.get_path_to_core()

            fasta = '>' + values_tab[0] + '\n' + values_tab[1] + '\n'
            fasta_filename = '/data-hmm/tmp/' + str(uuid.uuid4()) + '.fasta'
            self.io.write(fasta_filename, fasta)

            results_filename = "/data-hmm/results/hits_test_" + str(uuid.uuid4()) + ".txt"

            p = subprocess.Popen([
                "docker " +
                "run " +
                "--rm " +
                "--privileged " +
                "-v " +
                path_to_core + "/data-hmm:/data-hmm " +
                "inphinity-hmmer " +
                "hmmsearch " +
                "--tblout " +
                results_filename + " " +
                "/data-hmm/Pfam-A.hmm " +
                fasta_filename
            ], stdout=subprocess.PIPE, shell=True)

            (output, err) = p.communicate()

            # This makes the wait possible
            p_status = p.wait()

            end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            results = self.io.read_results(results_filename, self.configuration.get_detailed_logs())

            returned_domains = []

            for result in results:
                has_to_be_returned = True
                result_tab = result.split(' ')
                result_tab = list(filter(None, result_tab))

                best_1_domain = result_tab[2]
                num_domain = result_tab[3].split('.')[0]
                e_value = result_tab[4]
                score = result_tab[5]
                biais = result_tab[6]

                # E-VALUE
                if self.configuration.is_use_e_value_selection():
                    min_e_value = self.configuration.get_min_e_value()
                    max_e_value = self.configuration.get_max_e_value()

                    if min_e_value > e_value > max_e_value:
                        has_to_be_returned = False

                # SCORE
                if self.configuration.is_use_score_selection():
                    min_score = self.configuration.get_min_score()
                    max_score = self.configuration.get_max_score()

                    if min_score > score > max_score:
                        has_to_be_returned = False

                # BIAIS
                if self.configuration.is_use_biais_selection():
                    min_biais = self.configuration.get_min_biais()
                    max_biais = self.configuration.get_max_biais()

                    if min_biais > biais > max_biais:
                        has_to_be_returned = False

                if has_to_be_returned:
                    returned_domains.append(num_domain)

            p = subprocess.Popen([
                "rm",
                results_filename
            ])
            p.communicate()
            p_status = p.wait()

            p = subprocess.Popen([
                "rm",
                fasta_filename
            ])
            p.communicate()
            p_status = p.wait()

            return [values_tab[0], returned_domains, [start_time, end_time]]

        else:
            return 'ALREADY PROCESSED'
