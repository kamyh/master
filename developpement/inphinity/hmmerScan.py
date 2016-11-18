##
#   Created by: Deruaz Vincent
#   wrapper of hmmer scan calls from a docker container
#   03.10.2016
##

from subprocess import Popen, PIPE
import sys
from toolsIo import ToolsIO
import uuid
from Logger import Logger

LOGGER = Logger()

class HmmerScan:
    def __init__(self,configuration, verbose=False):
        self.configuration=configuration
        self.verdose = verbose
        print("HmmerScan wrapper tool initialization")
        self.io = ToolsIO()

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


    def compute_domaine_from_host(self, fasta_filename, results_filename):
        #To solve conext dependent issue qith docker.sock linking
        path_to_core = self.configuration.get_path_to_core()
        print("Starting HmmerScan container for: %s" % fasta_filename)
        LOGGER.log_debug('HmmerScan: %s ' % fasta_filename)

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
        self.wait()

        print("Ending HmmerScan container for: %s" % fasta_filename)

    def wait(self):
        from docker import Client
        cli = Client(base_url='unix://var/run/docker.sock')
        wait = True
        while wait:
            wait = False
            for c in cli.containers():
                if(c['Image'] == 'inphinity-hmmer'):
                    wait = True

    def speparer_domaines(domaines_pass):
        p_f_dom = []
        domaines_vec = domaines_pass.split(' ')
        domaines_vec = domaines_vec[:-1]
        if len(domaines_vec) != 0:
            for dom in domaines_vec:
                #print "DOM: " + dom
                p_f_dom.append(dom.split('.')[0])
        else:
            p_f_dom = ["--NA--"]
        return p_f_dom

    def detecter_PFAM(self, info_prot, seq_prot):
        fasta = '>' + info_prot + '\n' + seq_prot + '\n'
        fasta_filename = '/data-hmm/tmp/' + str(uuid.uuid4()) + '.fasta'
        results_filename = '/data-hmm/tmp/' + str(uuid.uuid4()) + '.txt'

        self.io.write(fasta_filename, fasta)
        self.compute_domaine_from_host(fasta_filename, results_filename)

        #TODO: cut code here ??
        #1. Generate all hmmscan hits
        #2. rest of the execution

        print('##### RESULTS: %s #####\n' % info_prot)
        LOGGER.log_debug('RESULTS: %s ' % info_prot)

        results = self.io.read_results(results_filename, self.configuration.get_detailed_logs())

        if(self.verdose):
            print(results)

        returned_domains=[]

        for result in results:
            result_tab = result.split(' ')
            result_tab = list(filter(None, result_tab))

            best_1_domain=result_tab[2]
            num_domain=result_tab[3].split('.')[0]
            e_value=result_tab[4]
            score=result_tab[5]
            biais=result_tab[6]

            returned_domains.append(num_domain)

            #TODO: not take all ???

            #LOGGER.log_detailed('RESULTS PARSED: %s - %s - %s - %s - %s' % (best_1_domain,num_domain,e_value,score,biais), self.configuration.get_detailed_logs())

        LOGGER.log_debug('Domains: %s' % returned_domains)

        p = Popen([
            "rm",
            results_filename
        ])

        p = Popen([
            "rm",
            fasta_filename
        ])

        return returned_domains



























