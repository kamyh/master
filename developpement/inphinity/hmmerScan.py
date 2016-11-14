##
#   Created by: Deruaz Vincent
#   wrapper of hmmer scan calls from a docker container
#   03.10.2016
##

from subprocess import Popen, PIPE
import os
from io import IO
import uuid
from config import Config


class HmmerScan:
    def __init__(self):
        print("HmmerScan wrapper tool initialization")
        self.io = IO()

    ##
    #   Display the output of 'docker ps' command
    ##
    def docker_ps(self):
        p = Popen(["docker", "ps"])
        output = p.communicate()[0]
        print(output)

    def ls(self):
        p = Popen(["ls"])
        output = p.communicate()[0]
        print(output)

    ##
    #   Display the output of the scan hmmer command
    #   docker run --rm --privileged -v $PWD/data:/data tm/hmmer hmmsearch --tblout /data/hits.txt /data/Pfam-A.hmm /data/test_data.fasta
    #   docker run --rm --privileged -v /data-hmm:/data-hmm inphinity-hmmer hmmsearch --tblout /data-hmm/results/hits.txt /data-hmm/Pfam-A.hmm /data-hmm/fasta/test_data.fasta
    ##


    #TODO: test
    def get_results_domaine(self, filename):
        self.results = self.io.read_results(filename)
        print self.results

    def compute_domaine_from_host(self, fasta_filename, results_filename):
        c = Config('inphinity/default.ini')
        #To solve conext dependent issue qith docker.sock linking
        path_to_core = c.get_path_to_core()

        p = Popen([
            "docker",
            "run",
            "--rm",
            "--privileged",
            "-v",
            path_to_core + "/data-hmm:/data-hmm",
            "inphinity-hmmer",
            "hmmsearch",
            "--tblout",
            results_filename,
            "/data-hmm/Pfam-A.hmm",
            fasta_filename
        ])
        output = p.communicate()[0]
        print(output)

    def detecter_PFAM(self, info_prot, seq_prot):
        fasta = '>' + info_prot + '\n' + seq_prot + '\n'
        fasta_filename = '/data-hmm/tmp/' + str(uuid.uuid4()) + '.fasta'
        results_filename = '/data-hmm/tmp/' + str(uuid.uuid4()) + '.txt'

        self.io.write(fasta_filename, fasta)
        self.compute_domaine_from_host(fasta_filename, results_filename)

        print '##### RESULTS #####\n'
        self.get_results_domaine(results_filename)

        p = Popen([
            "rm",
            results_filename
        ])

        p = Popen([
            "rm",
            fasta_filename
        ])

        #TODO: parse results
